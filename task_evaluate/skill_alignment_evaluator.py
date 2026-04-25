#!/usr/bin/env python3
"""Evaluate whether a task instruction can reasonably use every bundled skill.

Expected task layout:
    task_root/
      instruction.md
      environment/
        skills/
          skill_name/
            skill.md

The evaluator reads only instruction.md and environment/skills/*/skill.md.
It does not inspect tests, solution files, or input fixtures.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence


REVIEW_FILE_NAME = "skill_review.json"


class SkillReviewError(RuntimeError):
    """Raised when task input, provider output, or API calls cannot be processed."""


@dataclass(frozen=True)
class TaskCandidate:
    root: Path
    task_id: str
    source_label: str

    @property
    def instruction_path(self) -> Path:
        return self.root / "instruction.md"

    @property
    def skills_dir(self) -> Path:
        return self.root / "environment" / "skills"


@dataclass(frozen=True)
class SkillFile:
    name: str
    path: Path
    relative_path: str
    content: str


@dataclass(frozen=True)
class TaskContent:
    task_id: str
    task_root: Path
    instruction_path: Path
    skills_dir: Path
    instruction: str
    skills: Sequence[SkillFile]


def read_text(path: Path, max_chars: int) -> str:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise SkillReviewError(f"Could not read {path}: {exc}") from exc
    text = raw.decode("utf-8", errors="replace")
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    head_len = max_chars // 2
    tail_len = max_chars - head_len
    omitted = len(text) - max_chars
    return (
        text[:head_len]
        + f"\n\n[... truncated {omitted} characters from middle ...]\n\n"
        + text[-tail_len:]
    )


def write_json(path: Path, data: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def load_env_file(path: Path) -> None:
    """Load KEY=VALUE pairs from .env without overriding existing env vars."""
    if not path.is_file():
        return
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            raise SkillReviewError(f"Invalid .env line {line_number}: {raw_line}")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise SkillReviewError(f"Invalid .env line {line_number}: empty key")
        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {"'", '"'}
        ):
            value = value[1:-1]
        os.environ.setdefault(key, value)


def discover_tasks(roots: Sequence[Path]) -> List[TaskCandidate]:
    tasks: List[TaskCandidate] = []
    seen: set[Path] = set()
    for raw_root in roots:
        search_root = raw_root.resolve()
        if search_root.is_file():
            if search_root.name.lower() != "instruction.md":
                raise SkillReviewError(f"File input must be instruction.md: {search_root}")
            task_root = search_root.parent.resolve()
            add_task(tasks, seen, task_root, task_root.name, task_root.parent.name)
            continue
        if not search_root.exists():
            raise SkillReviewError(f"Input path does not exist: {search_root}")
        if is_task_like_root(search_root):
            add_task(tasks, seen, search_root, search_root.name, search_root.parent.name)
            continue

        for current, dirnames, filenames in os.walk(search_root):
            current_path = Path(current)
            dirnames[:] = [
                name
                for name in sorted(dirnames)
                if name
                not in {
                    ".git",
                    ".idea",
                    "__pycache__",
                    "node_modules",
                    "jobs",
                    "review",
                    "review_0413",
                    "review_0414",
                    "review_0415",
                    "review_test",
                    "instruction_review_test",
                    "skill_review_output",
                    "task_review_output",
                }
                and not name.startswith(".tmp")
            ]
            if "instruction.md" not in filenames:
                continue
            resolved = current_path.resolve()
            if resolved in seen:
                dirnames[:] = []
                continue
            try:
                rel = resolved.relative_to(search_root)
            except ValueError:
                rel = Path(resolved.name)
            task_id = "__".join(rel.parts) if rel.parts else resolved.name
            add_task(tasks, seen, resolved, task_id, search_root.name)
            dirnames[:] = []

    tasks = disambiguate_task_ids(tasks)
    tasks.sort(key=lambda item: item.task_id)
    return tasks


def is_task_like_root(path: Path) -> bool:
    return (path / "instruction.md").is_file()


def add_task(
    tasks: List[TaskCandidate],
    seen: set[Path],
    root: Path,
    task_id: str,
    source_label: str,
) -> None:
    resolved = root.resolve()
    if resolved in seen:
        return
    seen.add(resolved)
    tasks.append(
        TaskCandidate(
            root=resolved,
            task_id=safe_task_id(task_id),
            source_label=safe_task_id(source_label),
        )
    )


def disambiguate_task_ids(tasks: Sequence[TaskCandidate]) -> List[TaskCandidate]:
    counts = Counter(task.task_id for task in tasks)
    output: List[TaskCandidate] = []
    for task in tasks:
        if counts[task.task_id] <= 1:
            output.append(task)
            continue
        output.append(
            TaskCandidate(
                root=task.root,
                task_id=safe_task_id(f"{task.source_label}__{task.task_id}"),
                source_label=task.source_label,
            )
        )
    return output


def safe_task_id(value: str) -> str:
    value = value.strip().replace("\\", "__").replace("/", "__")
    value = re.sub(r"[^A-Za-z0-9_. -]+", "_", value)
    value = re.sub(r"\s+", "_", value)
    return value.strip("._ ") or "task"


class CompatibleSkillProvider:
    """OpenAI-compatible chat completions provider."""

    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout_seconds: int = 120,
        temperature: float = 0.0,
        max_retries: int = 1,
        max_tokens: Optional[int] = None,
        json_retries: int = 2,
    ) -> None:
        self.model = model
        self.api_key = (
            api_key
            or os.environ.get("SKILL_REVIEW_API_KEY")
            or os.environ.get("TASK_REVIEW_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
        )
        if not self.api_key:
            raise SkillReviewError(
                "API key is required. Set SKILL_REVIEW_API_KEY, "
                "TASK_REVIEW_API_KEY, OPENAI_API_KEY, or pass --api-key."
            )
        self.base_url = normalize_base_url(
            base_url
            or os.environ.get("SKILL_REVIEW_BASE_URL")
            or os.environ.get("TASK_REVIEW_BASE_URL")
            or os.environ.get("OPENAI_BASE_URL")
            or "https://api.openai.com/v1"
        )
        self.timeout_seconds = timeout_seconds
        self.temperature = temperature
        self.max_retries = max(1, max_retries)
        self.max_tokens = max_tokens
        self.json_retries = max(1, json_retries)

    def review(self, content: TaskContent) -> Dict[str, Any]:
        last_error: Optional[SkillReviewError] = None
        expected_skill_names = [skill.name for skill in content.skills]
        for _ in range(self.json_retries):
            try:
                response_text = self._chat(build_prompt(content))
                parsed = parse_json_object(response_text)
                return normalize_output(parsed, expected_skill_names)
            except SkillReviewError as exc:
                last_error = exc
        raise last_error or SkillReviewError("Provider failed to return valid JSON")

    def _chat(self, prompt: str) -> str:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an expert evaluator of task-skill alignment. "
                        "Return only valid JSON. Do not include markdown fences."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": self.temperature,
        }
        if self.max_tokens is not None and self.max_tokens > 0:
            payload["max_tokens"] = self.max_tokens

        body = ""
        for attempt in range(1, self.max_retries + 1):
            request = urllib.request.Request(
                f"{self.base_url}/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(
                    request, timeout=self.timeout_seconds
                ) as response:
                    body = response.read().decode("utf-8")
                break
            except urllib.error.HTTPError as exc:
                details = exc.read().decode("utf-8", errors="replace")
                raise SkillReviewError(
                    f"Compatible API HTTP error: {details}"
                ) from exc
            except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
                if attempt >= self.max_retries:
                    raise SkillReviewError(
                        "Compatible API request timed out or failed after "
                        f"{attempt} attempt(s). Increase "
                        "SKILL_REVIEW_TIMEOUT_SECONDS, reduce --max-skill-chars, "
                        "or check provider/model availability. "
                        f"Last error: {exc}"
                    ) from exc
                time.sleep(min(2 * attempt, 10))

        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as exc:
            preview = body[:500].replace("\n", "\\n")
            raise SkillReviewError(
                "Compatible API returned a non-JSON response. Check "
                "SKILL_REVIEW_BASE_URL or TASK_REVIEW_BASE_URL points to a "
                f"/v1 Chat Completions base URL. Response preview: {preview!r}"
            ) from exc
        try:
            return str(parsed["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise SkillReviewError(
                f"Unexpected chat completion response: {body}"
            ) from exc


def normalize_base_url(value: str) -> str:
    base = value.strip().rstrip("/")
    suffix = "/chat/completions"
    if base.endswith(suffix):
        base = base[: -len(suffix)].rstrip("/")
    return base


def build_prompt(content: TaskContent) -> str:
    skill_blocks = []
    for skill in content.skills:
        skill_blocks.append(
            f"""### Skill: {skill.name}
Path: {skill.relative_path}

--- skill.md ---
{skill.content}
--- end skill.md ---"""
        )

    return f"""
You are evaluating whether the task instruction naturally requires or can reasonably use every skill bundled with the task.

Inputs:
- instruction.md
- every environment/skills/*/skill.md file

Important scope:
- Evaluate only whether the listed skills are usable for the instruction.
- Do not evaluate tests, solution quality, task value, or missing skills.
- Do not include a missing_skill_risk field.

Usage levels:
- essential: The task strongly depends on this skill; without it, the task is difficult or unnatural to complete.
- useful: The task can be completed without this skill, but this skill is a natural and clearly helpful choice.
- weak: The skill has only indirect, marginal, or keyword-level relevance.
- irrelevant: The instruction does not naturally call for this skill.

Score guide for relevance_score:
- 9-10: essential, directly required by the instruction.
- 7-8: useful, clearly helpful and naturally triggered.
- 5-6: weak, some relation exists but it is not a natural main tool.
- 0-4: irrelevant or very forced.

Decision rules:
- keep: every skill has relevance_score >= 7.
- review: no skill is <= 4, but at least one skill is 5-6.
- drop_or_fix_skills: at least one skill has relevance_score <= 4.
- invalid_skill_set: use only if skill data is missing or impossible to judge.

Evaluation rules:
- Do not mark a skill useful just because a keyword overlaps with the instruction.
- Do not mark a very broad/general skill useful unless the instruction naturally calls for it.
- If two skills overlap, both may be useful, but explain their distinct roles.
- Evidence must come from the instruction text, not from assumptions about hidden files.
- matched_skill_capabilities must come from the skill.md content.
- Return each expected skill exactly once.
- Recompute the final decision from the per-skill scores using the rules above.

Return JSON only, in this exact shape:
{{
  "decision": "keep | review | drop_or_fix_skills | invalid_skill_set",
  "all_skills_usable": true,
  "skill_alignment_score": 8.2,
  "skills": [
    {{
      "skill_name": "skill_name",
      "relevance_score": 8,
      "usage_level": "useful",
      "evidence_from_instruction": ["brief evidence from instruction.md"],
      "matched_skill_capabilities": ["brief capability from skill.md"],
      "risk": "brief uncertainty or empty string",
      "recommendation": "keep | review | remove_or_replace"
    }}
  ],
  "redundant_skills": [],
  "weak_skills": [],
  "summary": "brief task-level conclusion"
}}

Expected skills, exactly once:
{json.dumps([skill.name for skill in content.skills], ensure_ascii=False)}

Task id: {content.task_id}

--- instruction.md ---
{content.instruction}
--- end instruction.md ---

--- skills ---
{chr(10).join(skill_blocks)}
--- end skills ---
""".strip()


def parse_json_object(text: str) -> Dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", stripped, flags=re.S)
        if not match:
            raise SkillReviewError(f"Provider did not return JSON: {text[:500]}")
        try:
            parsed = json.loads(match.group(0))
        except json.JSONDecodeError as fallback_exc:
            preview = stripped[:1200].replace("\n", "\\n")
            raise SkillReviewError(
                "Provider returned malformed JSON. Increase "
                "SKILL_REVIEW_MAX_TOKENS or reduce --max-skill-chars. "
                f"Response preview: {preview!r}"
            ) from fallback_exc
    if not isinstance(parsed, dict):
        raise SkillReviewError("Provider JSON response must be an object")
    return parsed


def normalize_output(
    raw: Mapping[str, Any], expected_skill_names: Sequence[str]
) -> Dict[str, Any]:
    raw_skills = raw.get("skills")
    if not isinstance(raw_skills, list):
        raise SkillReviewError("Judge response missing skills list")

    by_name: Dict[str, Mapping[str, Any]] = {}
    for item in raw_skills:
        if not isinstance(item, Mapping):
            raise SkillReviewError("Each skills item must be an object")
        name = str(item.get("skill_name", "")).strip()
        if name:
            by_name[name] = item

    normalized_skills: List[Dict[str, Any]] = []
    for index, expected_name in enumerate(expected_skill_names):
        item: Optional[Mapping[str, Any]] = by_name.get(expected_name)
        if item is None and len(raw_skills) == len(expected_skill_names):
            fallback = raw_skills[index]
            item = fallback if isinstance(fallback, Mapping) else None
        if item is None:
            raise SkillReviewError(f"Judge response missing skill: {expected_name}")

        score = clamp_score(item.get("relevance_score"))
        normalized_skills.append(
            {
                "skill_name": expected_name,
                "relevance_score": score,
                "usage_level": score_to_usage_level(score),
                "evidence_from_instruction": string_list(
                    item.get("evidence_from_instruction")
                ),
                "matched_skill_capabilities": string_list(
                    item.get("matched_skill_capabilities")
                ),
                "risk": str(item.get("risk", "")).strip(),
                "recommendation": recommendation_for_score(score),
            }
        )

    scores = [float(skill["relevance_score"]) for skill in normalized_skills]
    decision = decision_for_scores(scores)
    return {
        "decision": decision,
        "all_skills_usable": bool(scores) and all(score >= 7 for score in scores),
        "skill_alignment_score": round(sum(scores) / len(scores), 2) if scores else 0.0,
        "skills": normalized_skills,
        "redundant_skills": [
            skill["skill_name"]
            for skill in normalized_skills
            if float(skill["relevance_score"]) <= 4
        ],
        "weak_skills": [
            skill["skill_name"]
            for skill in normalized_skills
            if 5 <= float(skill["relevance_score"]) < 7
        ],
        "summary": str(raw.get("summary", "")).strip(),
    }


def clamp_score(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise SkillReviewError(f"Expected numeric relevance_score, got {value!r}") from exc
    return round(min(10.0, max(0.0, number)), 2)


def score_to_usage_level(score: float) -> str:
    if score >= 9:
        return "essential"
    if score >= 7:
        return "useful"
    if score >= 5:
        return "weak"
    return "irrelevant"


def recommendation_for_score(score: float) -> str:
    if score >= 7:
        return "keep"
    if score >= 5:
        return "review"
    return "remove_or_replace"


def decision_for_scores(scores: Sequence[float]) -> str:
    if not scores:
        return "invalid_skill_set"
    if all(score >= 7 for score in scores):
        return "keep"
    if any(score <= 4 for score in scores):
        return "drop_or_fix_skills"
    return "review"


def string_list(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value is None:
        return []
    text = str(value).strip()
    return [text] if text else []


def load_task_content(
    task: TaskCandidate,
    max_instruction_chars: int,
    max_skill_chars: int,
) -> TaskContent:
    instruction = read_text(task.instruction_path, max_instruction_chars)
    skills = load_skill_files(task, max_skill_chars)
    return TaskContent(
        task_id=task.task_id,
        task_root=task.root,
        instruction_path=task.instruction_path,
        skills_dir=task.skills_dir,
        instruction=instruction,
        skills=skills,
    )


def load_skill_files(task: TaskCandidate, max_skill_chars: int) -> List[SkillFile]:
    skills_dir = task.skills_dir
    if not skills_dir.is_dir():
        raise SkillReviewError(f"Missing skills directory: {skills_dir}")

    skill_files: List[SkillFile] = []
    skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    if not skill_dirs:
        raise SkillReviewError(f"No skill directories found: {skills_dir}")

    for skill_dir in skill_dirs:
        skill_path = find_skill_md(skill_dir)
        if skill_path is None:
            raise SkillReviewError(f"Missing skill.md in {skill_dir}")
        try:
            relative_path = skill_path.relative_to(task.root).as_posix()
        except ValueError:
            relative_path = str(skill_path)
        skill_files.append(
            SkillFile(
                name=skill_dir.name,
                path=skill_path,
                relative_path=relative_path,
                content=read_text(skill_path, max_skill_chars),
            )
        )
    return skill_files


def find_skill_md(skill_dir: Path) -> Optional[Path]:
    direct = skill_dir / "skill.md"
    if direct.is_file():
        return direct
    for child in skill_dir.iterdir():
        if child.is_file() and child.name.lower() == "skill.md":
            return child
    return None


def invalid_result(task: TaskCandidate, error: str) -> Dict[str, Any]:
    return {
        "task_id": task.task_id,
        "task_root": str(task.root),
        "instruction_path": str(task.instruction_path),
        "skills_dir": str(task.skills_dir),
        "decision": "invalid_skill_set",
        "all_skills_usable": False,
        "skill_alignment_score": 0.0,
        "skills": [],
        "redundant_skills": [],
        "weak_skills": [],
        "summary": error,
    }


def process_task(
    task: TaskCandidate,
    provider: CompatibleSkillProvider,
    output_root: Path,
    max_instruction_chars: int,
    max_skill_chars: int,
    skip_existing: bool = False,
) -> Dict[str, Any]:
    task_output_dir = output_root / task.task_id
    review_path = task_output_dir / REVIEW_FILE_NAME
    if skip_existing and review_path.is_file():
        return json.loads(review_path.read_text(encoding="utf-8"))

    try:
        content = load_task_content(task, max_instruction_chars, max_skill_chars)
    except SkillReviewError as exc:
        result = invalid_result(task, str(exc))
        write_json(review_path, result)
        return result

    judge_output = provider.review(content)
    skill_paths = {skill.name: str(skill.path) for skill in content.skills}
    enriched_skills = []
    for skill_result in judge_output["skills"]:
        skill_name = str(skill_result["skill_name"])
        enriched = dict(skill_result)
        enriched["skill_path"] = skill_paths.get(skill_name, "")
        enriched_skills.append(enriched)

    result = {
        "task_id": task.task_id,
        "task_root": str(task.root),
        "instruction_path": str(content.instruction_path),
        "skills_dir": str(content.skills_dir),
        "decision": judge_output["decision"],
        "all_skills_usable": judge_output["all_skills_usable"],
        "skill_alignment_score": judge_output["skill_alignment_score"],
        "skills": enriched_skills,
        "redundant_skills": judge_output["redundant_skills"],
        "weak_skills": judge_output["weak_skills"],
        "summary": judge_output["summary"],
    }
    write_json(review_path, result)
    return result


def write_summaries(output_root: Path, results: Sequence[Mapping[str, Any]]) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    with (output_root / "summary.jsonl").open("w", encoding="utf-8") as handle:
        for result in results:
            handle.write(json.dumps(result, ensure_ascii=False, sort_keys=False) + "\n")

    fieldnames = [
        "task_id",
        "decision",
        "all_skills_usable",
        "skill_alignment_score",
        "skill_count",
        "essential_count",
        "useful_count",
        "weak_count",
        "irrelevant_count",
        "redundant_skills",
        "weak_skills",
        "summary",
        "task_root",
        "instruction_path",
        "skills_dir",
    ]
    with (output_root / "summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(summary_row(result))


def summary_row(result: Mapping[str, Any]) -> Dict[str, Any]:
    skills = result.get("skills", [])
    if not isinstance(skills, list):
        skills = []
    level_counts = Counter(
        str(skill.get("usage_level", ""))
        for skill in skills
        if isinstance(skill, Mapping)
    )
    return {
        "task_id": result.get("task_id", ""),
        "decision": result.get("decision", ""),
        "all_skills_usable": result.get("all_skills_usable", ""),
        "skill_alignment_score": result.get("skill_alignment_score", ""),
        "skill_count": len(skills),
        "essential_count": level_counts.get("essential", 0),
        "useful_count": level_counts.get("useful", 0),
        "weak_count": level_counts.get("weak", 0),
        "irrelevant_count": level_counts.get("irrelevant", 0),
        "redundant_skills": ";".join(string_list(result.get("redundant_skills"))),
        "weak_skills": ";".join(string_list(result.get("weak_skills"))),
        "summary": result.get("summary", ""),
        "task_root": result.get("task_root", ""),
        "instruction_path": result.get("instruction_path", ""),
        "skills_dir": result.get("skills_dir", ""),
    }


def first_env(*names: str, default: Optional[str] = None) -> Optional[str]:
    for name in names:
        value = os.environ.get(name)
        if value is not None and value.strip():
            return value
    return default


def run_tasks(
    tasks: Sequence[TaskCandidate],
    provider: CompatibleSkillProvider,
    args: argparse.Namespace,
) -> List[Mapping[str, Any]]:
    workers = resolve_workers(args)
    if workers <= 1:
        results: List[Mapping[str, Any]] = []
        for index, task in enumerate(tasks, start=1):
            print(f"[{index}/{len(tasks)}] reviewing {task.task_id}", flush=True)
            result = process_task(
                task,
                provider,
                args.output,
                max_instruction_chars=args.max_instruction_chars,
                max_skill_chars=args.max_skill_chars,
                skip_existing=args.skip_existing,
            )
            results.append(result)
        return results

    print(f"Reviewing {len(tasks)} task(s) with {workers} workers", flush=True)
    ordered_results: List[Optional[Mapping[str, Any]]] = [None] * len(tasks)
    completed = 0
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_index = {
            executor.submit(
                process_task,
                task,
                provider,
                args.output,
                args.max_instruction_chars,
                args.max_skill_chars,
                args.skip_existing,
            ): index
            for index, task in enumerate(tasks)
        }
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            task = tasks[index]
            try:
                ordered_results[index] = future.result()
            except Exception as exc:
                for pending in future_to_index:
                    pending.cancel()
                if isinstance(exc, SkillReviewError):
                    raise exc
                raise SkillReviewError(f"Failed while reviewing {task.task_id}: {exc}") from exc
            completed += 1
            print(
                f"[{completed}/{len(tasks)}] reviewed {task.task_id}",
                flush=True,
            )

    return [result for result in ordered_results if result is not None]


def resolve_workers(args: argparse.Namespace) -> int:
    workers = args.workers
    if workers is None:
        raw_workers = first_env(
            "SKILL_REVIEW_WORKERS",
            "TASK_REVIEW_WORKERS",
            default="1",
        )
        workers = int(raw_workers or "1")
    return max(1, workers)


def make_provider(args: argparse.Namespace) -> CompatibleSkillProvider:
    provider_name = (
        args.provider
        or first_env("SKILL_REVIEW_PROVIDER", "TASK_REVIEW_PROVIDER")
        or "compatible"
    )
    if provider_name not in {"compatible", "openai"}:
        raise SkillReviewError(f"Unknown provider: {provider_name}")

    model = args.model or first_env("SKILL_REVIEW_MODEL", "TASK_REVIEW_MODEL")
    if not model:
        raise SkillReviewError(
            "A model is required. Pass --model or set SKILL_REVIEW_MODEL "
            "or TASK_REVIEW_MODEL in .env."
        )
    timeout_seconds = args.timeout_seconds
    if timeout_seconds is None:
        timeout_seconds = int(
            first_env(
                "SKILL_REVIEW_TIMEOUT_SECONDS",
                "TASK_REVIEW_TIMEOUT_SECONDS",
                default="120",
            )
        )
    temperature = args.temperature
    if temperature is None:
        temperature = float(
            first_env(
                "SKILL_REVIEW_TEMPERATURE",
                "TASK_REVIEW_TEMPERATURE",
                default="0",
            )
        )
    max_retries = args.max_retries
    if max_retries is None:
        max_retries = int(
            first_env(
                "SKILL_REVIEW_MAX_RETRIES",
                "TASK_REVIEW_MAX_RETRIES",
                default="1",
            )
        )
    max_tokens = args.max_tokens
    if max_tokens is None:
        raw_max_tokens = first_env(
            "SKILL_REVIEW_MAX_TOKENS",
            "TASK_REVIEW_MAX_TOKENS",
            default="",
        )
        max_tokens = int(raw_max_tokens) if raw_max_tokens else None
    json_retries = args.json_retries
    if json_retries is None:
        json_retries = int(
            first_env(
                "SKILL_REVIEW_JSON_RETRIES",
                "TASK_REVIEW_JSON_RETRIES",
                default="2",
            )
        )
    return CompatibleSkillProvider(
        model=model,
        api_key=args.api_key,
        base_url=args.base_url,
        timeout_seconds=timeout_seconds,
        temperature=temperature,
        max_retries=max_retries,
        max_tokens=max_tokens,
        json_retries=json_retries,
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate whether instruction.md naturally uses every "
            "environment/skills/*/skill.md file."
        )
    )
    parser.add_argument(
        "roots",
        nargs="+",
        type=Path,
        help="Task root(s), parent directory/directories, or instruction.md file(s).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("skill_review_output"),
        help="Output directory for skill_review.json and summaries.",
    )
    parser.add_argument(
        "--provider",
        choices=("compatible", "openai"),
        default=None,
        help=(
            "Provider. Defaults to SKILL_REVIEW_PROVIDER, "
            "TASK_REVIEW_PROVIDER, or compatible."
        ),
    )
    parser.add_argument("--model", default=None, help="OpenAI-compatible model.")
    parser.add_argument(
        "--api-key",
        default=None,
        help=(
            "API key. Defaults to SKILL_REVIEW_API_KEY, "
            "TASK_REVIEW_API_KEY, or OPENAI_API_KEY."
        ),
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help=(
            "Base URL. Defaults to SKILL_REVIEW_BASE_URL, "
            "TASK_REVIEW_BASE_URL, OPENAI_BASE_URL, or OpenAI."
        ),
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=Path(".env"),
        help="Path to .env config file. Existing environment variables are not overwritten.",
    )
    parser.add_argument("--timeout-seconds", type=int, default=None)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument(
        "--max-retries",
        type=int,
        default=None,
        help=(
            "Retry count for timeout/network failures. Defaults to "
            "SKILL_REVIEW_MAX_RETRIES, TASK_REVIEW_MAX_RETRIES, or 1."
        ),
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help=(
            "Optional response token cap. Defaults to SKILL_REVIEW_MAX_TOKENS "
            "or TASK_REVIEW_MAX_TOKENS if set."
        ),
    )
    parser.add_argument(
        "--json-retries",
        type=int,
        default=None,
        help=(
            "Retry count for malformed/missing-field model JSON. Defaults to "
            "SKILL_REVIEW_JSON_RETRIES, TASK_REVIEW_JSON_RETRIES, or 2."
        ),
    )
    parser.add_argument(
        "--max-instruction-chars",
        type=int,
        default=60000,
        help="Maximum characters read from instruction.md before middle truncation.",
    )
    parser.add_argument(
        "--max-skill-chars",
        type=int,
        default=30000,
        help="Maximum characters read from each skill.md before middle truncation.",
    )
    parser.add_argument("--limit", type=int, default=0, help="0 means no limit.")
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help=(
            "If output/<task_id>/skill_review.json already exists, reuse it "
            "and skip model calls for that task."
        ),
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help=(
            "Number of task reviews to run concurrently. Defaults to "
            "SKILL_REVIEW_WORKERS, TASK_REVIEW_WORKERS, or 1."
        ),
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        load_env_file(args.env_file)
        provider = make_provider(args)
        tasks = discover_tasks(args.roots)
        if args.limit and args.limit > 0:
            tasks = tasks[: args.limit]
        if not tasks:
            raise SkillReviewError("No instruction.md files found.")

        results = run_tasks(tasks, provider, args)
        write_summaries(args.output, results)
        print(f"Reviewed {len(results)} task(s). Output: {args.output.resolve()}", flush=True)
        return 0
    except SkillReviewError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
