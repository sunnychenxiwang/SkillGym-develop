#!/usr/bin/env python3
"""Review, optionally repair, and re-review_0413 task tests against instructions.

Expected task layout:
    task_root/
      instruction.md
      task.toml
      solution/solve.sh
      tests/test_outputs.py

This version intentionally evaluates only instruction/test alignment. It does
not inspect or score solution/solve.sh. The only decisions are:
    keep, repair, discard
"""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import os
import re
import shutil
import socket
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence


DIMENSIONS = (
    "alignment_with_instruction",
    "coverage_depth",
    "assertion_justifiability",
    "edge_case_coverage",
    "determinism_stability",
    "anti_cheating_strength",
    "brittleness",
)

ISSUE_TAGS = {
    "missing_edge_cases",
    "low_coverage_depth",
    "weak_anti_cheating",
    "brittle_assertion",
    "flaky_tests",
    "tests_only_check_existence",
    "tests_depend_on_solution_internals",
    "instruction_test_mismatch",
    "hidden_requirement_in_tests",
    "overly_strict_equivalence",
    "unverifiable_requirement",
    "test_leaks_expected_answer",
    "test_hardcodes_fixture_answer",
}

DECISIONS = {"keep", "repair", "discard"}
REVIEW_FILE_NAME = "review_result.json"


class ReviewError(RuntimeError):
    """Raised when provider output or task input cannot be processed."""


@dataclass(frozen=True)
class TaskCandidate:
    root: Path
    task_id: str


@dataclass(frozen=True)
class TaskContent:
    task_id: str
    root: Path
    instruction: str
    test_outputs: str

    @classmethod
    def load(cls, task: TaskCandidate, max_file_chars: int) -> "TaskContent":
        return cls(
            task_id=task.task_id,
            root=task.root,
            instruction=read_text(task.root / "instruction.md", max_file_chars),
            test_outputs=read_text(
                task.root / "tests" / "test_outputs.py", max_file_chars
            ),
        )


def read_text(path: Path, max_chars: int) -> str:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ReviewError(f"Could not read {path}: {exc}") from exc
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
            raise ReviewError(f"Invalid .env line {line_number}: {raw_line}")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ReviewError(f"Invalid .env line {line_number}: empty key")
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
    for search_root in roots:
        search_root = search_root.resolve()
        if is_task_root(search_root):
            if search_root not in seen:
                tasks.append(TaskCandidate(root=search_root, task_id=search_root.name))
                seen.add(search_root)
            continue
        for current, dirnames, filenames in os.walk(search_root):
            current_path = Path(current)
            dirnames[:] = [
                name
                for name in dirnames
                if name not in {"jobs", ".git", "__pycache__", "task_review_output"}
            ]
            if "instruction.md" not in filenames or not is_task_root(current_path):
                continue
            resolved = current_path.resolve()
            if resolved in seen:
                continue
            rel = resolved.relative_to(search_root)
            tasks.append(TaskCandidate(root=resolved, task_id="__".join(rel.parts)))
            seen.add(resolved)
            dirnames[:] = []
    tasks.sort(key=lambda item: item.task_id)
    return tasks


def is_task_root(path: Path) -> bool:
    return (
        (path / "instruction.md").is_file()
        and (path / "tests" / "test_outputs.py").is_file()
    )


def clamp_score(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ReviewError(f"Expected numeric score, got {value!r}") from exc
    return min(100.0, max(0.0, number))


def compute_score(dimensions: Mapping[str, float]) -> float:
    return round(
        0.30 * dimensions["alignment_with_instruction"]
        + 0.25 * dimensions["coverage_depth"]
        + 0.20 * dimensions["assertion_justifiability"]
        + 0.10 * dimensions["determinism_stability"]
        + 0.05 * dimensions["edge_case_coverage"]
        + 0.05 * dimensions["anti_cheating_strength"]
        + 0.05 * (100 - dimensions["brittleness"]),
        2,
    )


def normalize_judge_output(raw: Mapping[str, Any]) -> Dict[str, Any]:
    raw_dimensions = raw.get("dimensions")
    if not isinstance(raw_dimensions, Mapping):
        raise ReviewError("Judge response must contain a dimensions object")

    dimensions: Dict[str, float] = {}
    for name in DIMENSIONS:
        if name not in raw_dimensions:
            raise ReviewError(f"Judge response missing dimension: {name}")
        dimensions[name] = clamp_score(raw_dimensions[name])

    issue_tags = [
        tag for tag in normalize_string_list(raw.get("issue_tags", [])) if tag in ISSUE_TAGS
    ]
    fatal_issues = normalize_fatal_issues(raw.get("fatal_issues", []))
    repairability = clamp_score(raw.get("repairability", 0))
    repair_actions = normalize_string_list(raw.get("repair_actions", []))

    return {
        "dimensions": dimensions,
        "issue_tags": issue_tags,
        "fatal_issues": fatal_issues,
        "repairability": repairability,
        "repair_actions": repair_actions,
        "score": compute_score(dimensions),
    }


def normalize_string_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if not isinstance(value, list):
        return []
    result: List[str] = []
    for item in value:
        if item is None:
            continue
        text = str(item).strip()
        if text:
            result.append(text)
    return dedupe(result)


def normalize_fatal_issues(value: Any) -> List[Dict[str, str]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ReviewError("fatal_issues must be a list")
    normalized: List[Dict[str, str]] = []
    for item in value:
        if isinstance(item, str):
            issue_type = item.strip() or "unknown"
            description = issue_type
        elif isinstance(item, Mapping):
            issue_type = str(item.get("type", "unknown")).strip() or "unknown"
            description = str(item.get("description", issue_type)).strip()
        else:
            continue
        normalized.append({"type": issue_type, "description": description})
    return normalized


def dedupe(values: Iterable[str]) -> List[str]:
    result: List[str] = []
    seen: set[str] = set()
    for value in values:
        if value in seen:
            continue
        result.append(value)
        seen.add(value)
    return result


class ReviewProvider:
    def review(self, content: TaskContent) -> Dict[str, Any]:
        raise NotImplementedError

    def repair(self, content: TaskContent, review_result: Mapping[str, Any]) -> Dict[str, str]:
        raise NotImplementedError


class CompatibleReviewProvider(ReviewProvider):
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
        repair_max_tokens: Optional[int] = None,
        json_retries: int = 2,
    ) -> None:
        self.model = model
        self.api_key = (
            api_key
            or os.environ.get("TASK_REVIEW_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
        )
        self.base_url = (
            base_url
            or os.environ.get("TASK_REVIEW_BASE_URL")
            or os.environ.get("OPENAI_BASE_URL")
            or "https://api.openai.com/v1"
        ).rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.temperature = temperature
        self.max_retries = max(1, max_retries)
        self.max_tokens = max_tokens
        self.repair_max_tokens = repair_max_tokens
        self.json_retries = max(1, json_retries)
        if not self.api_key:
            raise ReviewError(
                "TASK_REVIEW_API_KEY or OPENAI_API_KEY is required for the "
                "compatible provider. Use --provider heuristic for an offline smoke test."
            )

    def review(self, content: TaskContent) -> Dict[str, Any]:
        last_error: Optional[ReviewError] = None
        for _ in range(self.json_retries):
            try:
                response_text = self._chat(build_review_prompt(content))
                return normalize_judge_output(parse_json_object(response_text))
            except ReviewError as exc:
                last_error = exc
        raise last_error or ReviewError("Provider failed to return a valid review_0413 JSON")

    def repair(self, content: TaskContent, review_result: Mapping[str, Any]) -> Dict[str, str]:
        response_text = self._chat(
            build_repair_prompt(content, review_result),
            max_tokens_override=self.repair_max_tokens,
        )
        parsed = parse_json_object(response_text)
        files = parsed.get("files", [])
        if not isinstance(files, list):
            raise ReviewError("Repair response must contain files: []")
        replacements: Dict[str, str] = {}
        for item in files:
            if not isinstance(item, Mapping):
                continue
            rel_path = str(item.get("path", "")).replace("\\", "/").strip()
            content_text = item.get("content")
            if not rel_path or not isinstance(content_text, str):
                continue
            if rel_path != "tests/test_outputs.py":
                raise ReviewError(f"Repair attempted to modify disallowed file: {rel_path}")
            replacements[rel_path] = content_text
        return replacements

    def _chat(self, prompt: str, max_tokens_override: Optional[int] = None) -> str:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a rigorous instruction-test alignment reviewer. "
                        "Return only valid JSON. Do not include markdown fences."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": self.temperature,
        }
        max_tokens = max_tokens_override if max_tokens_override is not None else self.max_tokens
        if max_tokens is not None and max_tokens > 0:
            payload["max_tokens"] = max_tokens

        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        body = ""
        for attempt in range(1, self.max_retries + 1):
            try:
                with urllib.request.urlopen(
                    request, timeout=self.timeout_seconds
                ) as response:
                    body = response.read().decode("utf-8")
                break
            except urllib.error.HTTPError as exc:
                details = exc.read().decode("utf-8", errors="replace")
                raise ReviewError(f"Compatible API HTTP error: {details}") from exc
            except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
                if attempt >= self.max_retries:
                    raise ReviewError(
                        "Compatible API request timed out or failed after "
                        f"{attempt} attempt(s). Increase TASK_REVIEW_TIMEOUT_SECONDS, "
                        "reduce --max-file-chars, or check provider/model availability. "
                        f"Last error: {exc}"
                    ) from exc
                time.sleep(min(2 * attempt, 10))

        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as exc:
            preview = body[:500].replace("\n", "\\n")
            raise ReviewError(
                "Compatible API returned a non-JSON response. Check "
                "TASK_REVIEW_BASE_URL points to a /v1 Chat Completions base URL. "
                f"Response preview: {preview!r}"
            ) from exc
        try:
            return str(parsed["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise ReviewError(f"Unexpected chat completion response: {body}") from exc


class HeuristicReviewProvider(ReviewProvider):
    """Offline smoke-test provider. Do not use for final-quality review_0413."""

    def review(self, content: TaskContent) -> Dict[str, Any]:
        tests_text = content.test_outputs
        assert_count = len(re.findall(r"\bassert\b", tests_text))
        has_only_exists = assert_count <= 3 and bool(
            re.search(r"exists|isfile|isdir|getsize", tests_text, re.I)
        )
        brittle = 65 if re.search(r"==\s*['\"]|count\s*==\s*\d+", tests_text) else 35
        leaks_answer = bool(
            re.search(r"expected (?:result|answer|count)|count\s*==\s*\d+", tests_text, re.I)
        )
        issue_tags: List[str] = []
        if assert_count < 8:
            issue_tags.append("low_coverage_depth")
        if assert_count < 10:
            issue_tags.append("missing_edge_cases")
        if has_only_exists:
            issue_tags.append("tests_only_check_existence")
        if brittle > 55:
            issue_tags.append("brittle_assertion")
        if leaks_answer:
            issue_tags.append("test_hardcodes_fixture_answer")
        if assert_count < 6 or leaks_answer:
            issue_tags.append("weak_anti_cheating")

        raw = {
            "dimensions": {
                "alignment_with_instruction": 72,
                "coverage_depth": 35 if has_only_exists else min(85, 50 + assert_count),
                "assertion_justifiability": 58 if leaks_answer else 72,
                "edge_case_coverage": 45 if assert_count < 10 else 70,
                "determinism_stability": 82,
                "anti_cheating_strength": 35 if leaks_answer else 55 + min(25, assert_count),
                "brittleness": brittle,
            },
            "issue_tags": issue_tags,
            "fatal_issues": [
                {
                    "type": "test_hardcodes_fixture_answer",
                    "description": "tests appear to hardcode the fixture answer",
                }
            ]
            if leaks_answer
            else [],
            "repairability": 75 if issue_tags else 25,
            "repair_actions": [
                "replace hardcoded expected answers with independent validation",
                "add edge cases and anti-cheating assertions",
                "relax unnecessary exact-match assertions",
            ]
            if issue_tags
            else [],
        }
        return normalize_judge_output(raw)

    def repair(self, content: TaskContent, review_result: Mapping[str, Any]) -> Dict[str, str]:
        return {}


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
            raise ReviewError(f"Provider did not return JSON: {text[:500]}")
        try:
            parsed = json.loads(match.group(0))
        except json.JSONDecodeError as fallback_exc:
            preview = stripped[:1200].replace("\n", "\\n")
            raise ReviewError(
                "Provider returned malformed JSON. This often happens when a "
                "repair response is truncated by max_tokens or includes unescaped "
                "file content. Increase TASK_REVIEW_REPAIR_MAX_TOKENS or reduce "
                f"--max-file-chars. Response preview: {preview!r}"
            ) from fallback_exc
    if not isinstance(parsed, dict):
        raise ReviewError("Provider JSON response must be an object")
    return parsed


def build_review_prompt(content: TaskContent) -> str:
    return f"""
Task id: {content.task_id}

Evaluate only whether tests/test_outputs.py is aligned with instruction.md.
Do not evaluate wrapper scripts or solution/solve.sh. Treat instruction.md as
the source of truth for the task contract. Score every dimension from 0 to 100.

Important calibration rules:
- Many tasks are fixed-input benchmark tasks. For these tasks, tests may check
  exact expected values derived from the fixed input files.
- Do not penalize exact numeric/string constants merely because those constants
  are not written in instruction.md or because you cannot inspect the input
  files in this prompt.
- Treat an assertion as justified if it checks the required output contract or
  a value plausibly derived from the named task inputs.
- Do not require synthetic edge cases unless instruction.md asks for reusable
  general behavior, a library/API, or tests claim broad generality.
- Anti-cheating is secondary. A fixed expected answer is not automatically weak
  anti-cheating. Penalize anti-cheating mainly when tests only check existence,
  schema, or loose plausibility without validating substantive results.
- Mark fatal_issues only for direct contradictions with instruction.md,
  impossible or unrelated checks, missing/unavailable required inputs, flaky
  external dependencies, or tests that cannot meaningfully validate the task.

Dimensions:
- alignment_with_instruction: tests validate the required artifact, path, format, and core task goal
- coverage_depth: tests cover key output fields, formats, calculations, and final results
- assertion_justifiability: assertions are justified by instruction.md or plausibly by fixed task inputs
- edge_case_coverage: tests cover important boundaries when the task contract calls for general behavior
- determinism_stability: tests avoid flaky randomness, current time, network, or brittle environment state
- anti_cheating_strength: tests validate substantive output rather than only existence, schema, or loose plausibility
- brittleness: reverse item; higher means over-strict exact strings/order/format/implementation details not required by the task

Allowed issue_tags:
{json.dumps(sorted(ISSUE_TAGS), ensure_ascii=False)}

Issue tag calibration:
- Use test_hardcodes_fixture_answer only when constants are arbitrary,
  contradictory, unrelated to fixed inputs, or replace the required task
  contract with unjustified values.
- Use test_leaks_expected_answer only when the test exposes answers in a way
  that materially weakens validation beyond normal fixed-input ground truth
  checking.
- Use hidden_requirement_in_tests only when a requirement is neither stated in
  instruction.md nor plausibly implied by the fixed inputs and output contract.

fatal_issues format:
[
  {{"type": "short_machine_type", "description": "brief reason"}}
]

Return only this JSON object shape:
{{
  "dimensions": {{
    "alignment_with_instruction": 0,
    "coverage_depth": 0,
    "assertion_justifiability": 0,
    "edge_case_coverage": 0,
    "determinism_stability": 0,
    "anti_cheating_strength": 0,
    "brittleness": 0
  }},
  "issue_tags": [],
  "fatal_issues": [],
  "repairability": 0,
  "repair_actions": []
}}

Files:
{format_files([
    ("instruction.md", content.instruction),
    ("tests/test_outputs.py", content.test_outputs),
])}
""".strip()


def build_repair_prompt(content: TaskContent, review_result: Mapping[str, Any]) -> str:
    return f"""
Task id: {content.task_id}

Repair tests/test_outputs.py only. Do not modify instruction.md. Do not inspect
or rely on wrapper scripts or solution/solve.sh. Use instruction.md as the only
source of truth.

Allowed paths:
["tests/test_outputs.py"]

Rules:
- Do not introduce requirements that instruction.md does not state or imply.
- Do not weaken core checks just to reduce brittleness.
- Do not bind tests to solution internals.
- Keep fixed expected values when they plausibly validate ground truth for a
  fixed-input benchmark task.
- If fixed expected values are changed or added, they must be derivable from
  the fixed task inputs and instruction.
- Prefer structural/equivalence checks when instruction allows multiple valid outputs.

Review result:
{json.dumps(review_result, ensure_ascii=False, indent=2)}

Current files:
{format_files([
    ("instruction.md", content.instruction),
    ("tests/test_outputs.py", content.test_outputs),
])}

Return only this JSON object:
{{
  "files": [
    {{"path": "tests/test_outputs.py", "content": "full replacement file content"}}
  ]
}}

If no safe targeted test repair is possible, return:
{{"files": []}}
""".strip()


def format_files(files: Sequence[tuple[str, str]]) -> str:
    blocks = []
    for path, content in files:
        blocks.append(f"\n--- {path} ---\n{content}\n--- end {path} ---")
    return "\n".join(blocks)


def decide(score: float, judge_output: Mapping[str, Any]) -> str:
    dimensions = judge_output["dimensions"]
    repairability = float(judge_output["repairability"])
    if (
        score >= 75
        and not judge_output.get("fatal_issues")
        and dimensions["alignment_with_instruction"] >= 70
        and dimensions["coverage_depth"] >= 60
        and dimensions["assertion_justifiability"] >= 65
    ):
        return "keep"
    if score >= 50 and repairability >= 50:
        return "repair"
    return "discard"


def should_accept_repair(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
) -> bool:
    before_dims = before["judge_output_before"]["dimensions"]
    after_dims = after["judge_output_after"]["dimensions"]
    return (
        after["score_after"] >= before["score_before"] + 5
        and after["score_after"] >= 70
        and after_dims["alignment_with_instruction"]
        >= before_dims["alignment_with_instruction"]
        and after_dims["assertion_justifiability"]
        >= before_dims["assertion_justifiability"]
        and after_dims["coverage_depth"] >= before_dims["coverage_depth"] - 2
        and after_dims["anti_cheating_strength"]
        >= before_dims["anti_cheating_strength"] - 2
    )


def process_task(
    task: TaskCandidate,
    provider: ReviewProvider,
    output_root: Path,
    max_file_chars: int,
    apply_repair: bool,
    force_repair: bool = False,
    skip_existing: bool = False,
) -> Dict[str, Any]:
    task_output_dir = output_root / task.task_id
    result_path = task_output_dir / REVIEW_FILE_NAME
    if skip_existing and result_path.is_file():
        try:
            existing = json.loads(result_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ReviewError(f"Existing result is not valid JSON: {result_path}") from exc
        if not isinstance(existing, dict):
            raise ReviewError(f"Existing result is not a JSON object: {result_path}")
        existing.setdefault("task_id", task.task_id)
        return existing

    content = TaskContent.load(task, max_file_chars)
    try:
        judge_before = provider.review(content)
    except ReviewError as exc:
        result = {
            "task_id": task.task_id,
            "review_error": str(exc),
            "initial_decision": "discard",
            "final_decision": "discard",
        }
        write_json(task_output_dir / REVIEW_FILE_NAME, result)
        return result
    score_before = float(judge_before["score"])
    initial_decision = decide(score_before, judge_before)

    result: Dict[str, Any] = {
        "task_id": task.task_id,
        "score_before": score_before,
        "judge_output_before": strip_internal_score(judge_before),
        "initial_decision": initial_decision,
    }

    should_repair = force_repair or (apply_repair and initial_decision == "repair")
    if not should_repair:
        result["final_decision"] = initial_decision
        write_json(task_output_dir / REVIEW_FILE_NAME, result)
        return result

    result["repair_plan"] = {
        "targets": ["tests"],
        "actions": judge_before.get("repair_actions", []),
    }
    if force_repair:
        result["forced_repair"] = True

    try:
        replacements = provider.repair(content, result)
    except ReviewError as exc:
        result["repair_error"] = str(exc)
        result["final_decision"] = "repair"
        write_json(task_output_dir / REVIEW_FILE_NAME, result)
        return result

    if not replacements:
        result["final_decision"] = "repair"
        write_json(task_output_dir / REVIEW_FILE_NAME, result)
        return result

    patched_root = task_output_dir / "patched"
    materialize_minimal_task(task.root, patched_root)
    apply_replacements(patched_root, replacements)
    write_diff(task.root, patched_root, replacements.keys(), task_output_dir / "diff.patch")

    patched_candidate = TaskCandidate(root=patched_root, task_id=task.task_id)
    patched_content = TaskContent.load(patched_candidate, max_file_chars)
    try:
        judge_after = provider.review(patched_content)
    except ReviewError as exc:
        result["rereview_error"] = str(exc)
        result["final_decision"] = "repair"
        write_json(task_output_dir / REVIEW_FILE_NAME, result)
        return result

    score_after = float(judge_after["score"])
    after_result = {
        "score_after": score_after,
        "judge_output_after": strip_internal_score(judge_after),
        "delta_score": round(score_after - score_before, 2),
    }
    result.update(after_result)
    result["final_decision"] = "keep" if should_accept_repair(result, after_result) else "discard"
    write_json(task_output_dir / REVIEW_FILE_NAME, result)
    return result


def strip_internal_score(judge_output: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "dimensions": judge_output["dimensions"],
        "issue_tags": judge_output["issue_tags"],
        "fatal_issues": judge_output["fatal_issues"],
        "repairability": judge_output["repairability"],
        "repair_actions": judge_output["repair_actions"],
    }


def materialize_minimal_task(source_root: Path, patched_root: Path) -> None:
    if patched_root.exists():
        shutil.rmtree(patched_root)
    patched_root.mkdir(parents=True, exist_ok=True)
    for file_name in ("instruction.md", "task.toml"):
        src = source_root / file_name
        if src.exists():
            shutil.copy2(src, patched_root / file_name)
    src_tests = source_root / "tests"
    if src_tests.exists():
        shutil.copytree(src_tests, patched_root / "tests")


def apply_replacements(patched_root: Path, replacements: Mapping[str, str]) -> None:
    root = patched_root.resolve()
    for rel_path, content in replacements.items():
        if rel_path != "tests/test_outputs.py":
            raise ReviewError(f"Replacement attempted disallowed file: {rel_path}")
        target = (patched_root / rel_path).resolve()
        if not is_relative_to(target, root):
            raise ReviewError(f"Replacement escapes patched task root: {rel_path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="")


def write_diff(
    original_root: Path,
    patched_root: Path,
    changed_paths: Iterable[str],
    diff_path: Path,
) -> None:
    diff_lines: List[str] = []
    for rel_path in sorted(changed_paths):
        original_path = original_root / rel_path
        patched_path = patched_root / rel_path
        original = (
            original_path.read_text(encoding="utf-8", errors="replace").splitlines(
                keepends=True
            )
            if original_path.exists()
            else []
        )
        patched = patched_path.read_text(
            encoding="utf-8", errors="replace"
        ).splitlines(keepends=True)
        diff_lines.extend(
            difflib.unified_diff(
                original,
                patched,
                fromfile=f"a/{rel_path}",
                tofile=f"b/{rel_path}",
            )
        )
    diff_path.parent.mkdir(parents=True, exist_ok=True)
    diff_path.write_text("".join(diff_lines), encoding="utf-8")


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def write_summary(output_root: Path, results: Sequence[Mapping[str, Any]]) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    with (output_root / "summary.jsonl").open("w", encoding="utf-8") as handle:
        for result in results:
            handle.write(json.dumps(summary_row(result), ensure_ascii=False) + "\n")

    fieldnames = [
        "task_id",
        "score_before",
        "alignment_with_instruction",
        "coverage_depth",
        "assertion_justifiability",
        "edge_case_coverage",
        "determinism_stability",
        "anti_cheating_strength",
        "brittleness",
        "repairability",
        "initial_decision",
        "final_decision",
        "issue_tags",
        "fatal_issue_count",
        "score_after",
        "delta_score",
    ]
    with (output_root / "summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(summary_row(result))


def summary_row(result: Mapping[str, Any]) -> Dict[str, Any]:
    output = result.get("judge_output_before", {})
    dimensions = output.get("dimensions", {}) if isinstance(output, Mapping) else {}
    issue_tags = output.get("issue_tags", []) if isinstance(output, Mapping) else []
    fatal_issues = output.get("fatal_issues", []) if isinstance(output, Mapping) else []
    return {
        "task_id": result.get("task_id", ""),
        "score_before": result.get("score_before", ""),
        "alignment_with_instruction": dimensions.get("alignment_with_instruction", ""),
        "coverage_depth": dimensions.get("coverage_depth", ""),
        "assertion_justifiability": dimensions.get("assertion_justifiability", ""),
        "edge_case_coverage": dimensions.get("edge_case_coverage", ""),
        "determinism_stability": dimensions.get("determinism_stability", ""),
        "anti_cheating_strength": dimensions.get("anti_cheating_strength", ""),
        "brittleness": dimensions.get("brittleness", ""),
        "repairability": output.get("repairability", ""),
        "initial_decision": result.get("initial_decision", ""),
        "final_decision": result.get("final_decision", ""),
        "issue_tags": ";".join(issue_tags),
        "fatal_issue_count": len(fatal_issues),
        "score_after": result.get("score_after", ""),
        "delta_score": result.get("delta_score", ""),
    }


def run_tasks(
    tasks: Sequence[TaskCandidate],
    provider: ReviewProvider,
    args: argparse.Namespace,
) -> List[Mapping[str, Any]]:
    workers = resolve_workers(args)
    if workers <= 1:
        results: List[Mapping[str, Any]] = []
        for index, task in enumerate(tasks, start=1):
            print(f"[{index}/{len(tasks)}] reviewing {task.task_id}", file=sys.stderr)
            results.append(
                process_task(
                    task=task,
                    provider=provider,
                    output_root=args.output,
                    max_file_chars=args.max_file_chars,
                    apply_repair=args.repair,
                    force_repair=args.force_repair,
                    skip_existing=args.skip_existing,
                )
            )
        return results

    print(
        f"Reviewing {len(tasks)} task(s) with {workers} workers",
        file=sys.stderr,
    )
    ordered_results: List[Optional[Mapping[str, Any]]] = [None] * len(tasks)
    completed = 0
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_index = {
            executor.submit(
                process_task,
                task,
                provider,
                args.output,
                args.max_file_chars,
                args.repair,
                args.force_repair,
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
                if isinstance(exc, ReviewError):
                    raise exc
                raise ReviewError(f"Failed while reviewing {task.task_id}: {exc}") from exc
            completed += 1
            print(
                f"[{completed}/{len(tasks)}] reviewed {task.task_id}",
                file=sys.stderr,
            )

    return [result for result in ordered_results if result is not None]


def resolve_workers(args: argparse.Namespace) -> int:
    workers = args.workers
    if workers is None:
        raw_workers = os.environ.get("TASK_REVIEW_WORKERS", "1").strip()
        try:
            workers = int(raw_workers or "1")
        except ValueError as exc:
            raise ReviewError(
                f"TASK_REVIEW_WORKERS must be an integer, got {raw_workers!r}"
            ) from exc
    return max(1, workers)


def make_provider(args: argparse.Namespace) -> ReviewProvider:
    provider_name = args.provider or os.environ.get("TASK_REVIEW_PROVIDER", "compatible")
    if provider_name == "heuristic":
        return HeuristicReviewProvider()
    if provider_name in {"compatible", "openai"}:
        model = args.model or os.environ.get("TASK_REVIEW_MODEL")
        if not model:
            raise ReviewError(
                "A model is required for the compatible provider. "
                "Pass --model or set TASK_REVIEW_MODEL in .env."
            )
        timeout_seconds = args.timeout_seconds
        if timeout_seconds is None:
            timeout_seconds = int(os.environ.get("TASK_REVIEW_TIMEOUT_SECONDS", "120"))
        temperature = args.temperature
        if temperature is None:
            temperature = float(os.environ.get("TASK_REVIEW_TEMPERATURE", "0"))
        max_retries = args.max_retries
        if max_retries is None:
            max_retries = int(os.environ.get("TASK_REVIEW_MAX_RETRIES", "1"))
        max_tokens = args.max_tokens
        if max_tokens is None:
            raw_max_tokens = os.environ.get("TASK_REVIEW_MAX_TOKENS", "").strip()
            max_tokens = int(raw_max_tokens) if raw_max_tokens else None
        repair_max_tokens = args.repair_max_tokens
        if repair_max_tokens is None:
            raw_repair_max_tokens = os.environ.get(
                "TASK_REVIEW_REPAIR_MAX_TOKENS", ""
            ).strip()
            repair_max_tokens = (
                int(raw_repair_max_tokens) if raw_repair_max_tokens else max_tokens
            )
        json_retries = args.json_retries
        if json_retries is None:
            json_retries = int(os.environ.get("TASK_REVIEW_JSON_RETRIES", "2"))
        return CompatibleReviewProvider(
            model=model,
            api_key=args.api_key,
            base_url=args.base_url,
            timeout_seconds=timeout_seconds,
            temperature=temperature,
            max_retries=max_retries,
            max_tokens=max_tokens,
            repair_max_tokens=repair_max_tokens,
            json_retries=json_retries,
        )
    raise ReviewError(f"Unknown provider: {provider_name}")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Review task tests against instruction.md and optionally repair tests."
    )
    parser.add_argument(
        "roots",
        nargs="+",
        type=Path,
        help="Task root(s) or parent directory/directories containing task roots.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("task_review_output"),
        help="Output directory for per-task review_result.json and summaries.",
    )
    parser.add_argument(
        "--provider",
        choices=("compatible", "openai", "heuristic"),
        default=None,
        help=(
            "Judge provider. Defaults to TASK_REVIEW_PROVIDER from .env, "
            "or compatible. Use heuristic only for offline smoke tests."
        ),
    )
    parser.add_argument("--model", default=None, help="OpenAI-compatible model.")
    parser.add_argument(
        "--api-key",
        default=None,
        help="API key. Defaults to TASK_REVIEW_API_KEY or OPENAI_API_KEY.",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Base URL. Defaults to TASK_REVIEW_BASE_URL, OPENAI_BASE_URL, or OpenAI.",
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
        help="Retry count for timeout/network failures. Defaults to TASK_REVIEW_MAX_RETRIES or 1.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Optional response token cap. Defaults to TASK_REVIEW_MAX_TOKENS if set.",
    )
    parser.add_argument(
        "--repair-max-tokens",
        type=int,
        default=None,
        help=(
            "Optional response token cap for repair calls. Defaults to "
            "TASK_REVIEW_REPAIR_MAX_TOKENS or --max-tokens."
        ),
    )
    parser.add_argument(
        "--json-retries",
        type=int,
        default=None,
        help="Retry count for malformed/missing-field model JSON. Defaults to TASK_REVIEW_JSON_RETRIES or 2.",
    )
    parser.add_argument(
        "--max-file-chars",
        type=int,
        default=60000,
        help="Maximum characters read per fixed task file before middle truncation.",
    )
    parser.add_argument(
        "--repair",
        action="store_true",
        help="For tasks initially marked repair, request test repairs and re-review_0413.",
    )
    parser.add_argument(
        "--force-repair",
        action="store_true",
        help="Attempt test repair regardless of the initial keep/repair/discard decision.",
    )
    parser.add_argument("--limit", type=int, default=0, help="0 means no limit.")
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help=(
            "If output/<task_id>/review_result.json already exists, reuse it "
            "and skip model calls for that task."
        ),
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help=(
            "Number of task reviews to run concurrently. Defaults to "
            "TASK_REVIEW_WORKERS or 1."
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
        if args.limit:
            tasks = tasks[: args.limit]
        if not tasks:
            raise ReviewError("No task roots discovered.")

        args.output.mkdir(parents=True, exist_ok=True)
        started_at = time.time()
        results = run_tasks(tasks, provider, args)
        write_summary(args.output, results)
        elapsed = time.time() - started_at
        print(
            f"Reviewed {len(results)} task(s) in {elapsed:.1f}s. "
            f"Output: {args.output.resolve()}",
            file=sys.stderr,
        )
        return 0
    except ReviewError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
