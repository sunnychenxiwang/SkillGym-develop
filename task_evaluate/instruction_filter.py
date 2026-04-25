#!/usr/bin/env python3
"""Score instruction.md files for clarity, testability, and naturalness."""

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
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence


DIMENSIONS = (
    "goal_clarity",
    "input_clarity",
    "constraint_completeness",
    "referential_clarity",
    "verifiability_uniqueness",
    "human_likeness",
)

WEIGHTS = {
    "goal_clarity": 0.15,
    "input_clarity": 0.15,
    "constraint_completeness": 0.15,
    "referential_clarity": 0.10,
    "verifiability_uniqueness": 0.20,
    "human_likeness": 0.20,
}

FORMULA = (
    "0.15*goal_clarity + 0.15*input_clarity + "
    "0.15*constraint_completeness + 0.10*referential_clarity + "
    "0.20*verifiability_uniqueness + 0.20*human_likeness"
)

REVIEW_FILE_NAME = "instruction_review.json"


class InstructionFilterError(RuntimeError):
    """Raised when input, provider output, or API calls cannot be processed."""


@dataclass(frozen=True)
class InstructionCandidate:
    task_id: str
    instruction_path: Path
    task_root: Path


def read_text(path: Path, max_chars: int) -> str:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise InstructionFilterError(f"Could not read {path}: {exc}") from exc
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
            raise InstructionFilterError(f"Invalid .env line {line_number}: {raw_line}")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise InstructionFilterError(f"Invalid .env line {line_number}: {raw_line}")
        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {"'", '"'}
        ):
            value = value[1:-1]
        os.environ.setdefault(key, value)


def discover_instructions(roots: Sequence[Path]) -> List[InstructionCandidate]:
    candidates: List[InstructionCandidate] = []
    seen: set[Path] = set()
    for raw_root in roots:
        root = raw_root.resolve()
        if root.is_file():
            if root.name != "instruction.md":
                raise InstructionFilterError(f"File input must be instruction.md: {root}")
            add_candidate(candidates, seen, root.parent, root, root.parent.name)
            continue
        if not root.exists():
            raise InstructionFilterError(f"Input path does not exist: {root}")
        if (root / "instruction.md").is_file():
            add_candidate(candidates, seen, root, root / "instruction.md", root.name)
            continue

        skip_names = {
            ".git",
            ".idea",
            "__pycache__",
            "node_modules",
            "review",
            "review_0413",
            "review_0414",
            "review_0415",
            "review_test",
            "task_review_output",
            "instruction_filter_output",
        }
        for current, dirnames, filenames in os.walk(root):
            current_path = Path(current)
            dirnames[:] = [
                name
                for name in sorted(dirnames)
                if name not in skip_names and not name.startswith(".tmp")
            ]
            if "instruction.md" not in filenames:
                continue
            instruction_path = current_path / "instruction.md"
            try:
                rel = current_path.resolve().relative_to(root)
            except ValueError:
                rel = Path(current_path.name)
            rel_parts = rel.parts if rel.parts else (current_path.name,)
            task_id = "__".join((root.name, *rel_parts))
            add_candidate(candidates, seen, current_path, instruction_path, task_id)
            dirnames[:] = []
    candidates.sort(key=lambda item: item.task_id)
    return candidates


def add_candidate(
    candidates: List[InstructionCandidate],
    seen: set[Path],
    task_root: Path,
    instruction_path: Path,
    task_id: str,
) -> None:
    resolved = instruction_path.resolve()
    if resolved in seen:
        return
    seen.add(resolved)
    candidates.append(
        InstructionCandidate(
            task_id=safe_task_id(task_id),
            instruction_path=resolved,
            task_root=task_root.resolve(),
        )
    )


def safe_task_id(value: str) -> str:
    value = value.strip().replace("\\", "__").replace("/", "__")
    value = re.sub(r"[^A-Za-z0-9_. -]+", "_", value)
    value = re.sub(r"\s+", "_", value)
    return value.strip("._ ") or "instruction"


class CompatibleInstructionProvider:
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
            or os.environ.get("INSTRUCTION_FILTER_API_KEY")
            or os.environ.get("TASK_REVIEW_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
        )
        if not self.api_key:
            raise InstructionFilterError(
                "API key is required. Set INSTRUCTION_FILTER_API_KEY, "
                "TASK_REVIEW_API_KEY, OPENAI_API_KEY, or pass --api-key."
            )
        self.base_url = normalize_base_url(
            base_url
            or os.environ.get("INSTRUCTION_FILTER_BASE_URL")
            or os.environ.get("TASK_REVIEW_BASE_URL")
            or os.environ.get("OPENAI_BASE_URL")
            or "https://api.openai.com/v1"
        )
        self.timeout_seconds = timeout_seconds
        self.temperature = temperature
        self.max_retries = max(1, max_retries)
        self.max_tokens = max_tokens
        self.json_retries = max(1, json_retries)

    def review(self, task_id: str, instruction: str) -> Dict[str, Any]:
        last_error: Optional[InstructionFilterError] = None
        for _ in range(self.json_retries):
            try:
                response_text = self._chat(build_prompt(task_id, instruction))
                return normalize_output(parse_json_object(response_text))
            except InstructionFilterError as exc:
                last_error = exc
        raise last_error or InstructionFilterError("Provider failed to return valid JSON")

    def _chat(self, prompt: str) -> str:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an expert evaluator of task instructions. "
                        "Return only valid JSON. Do not include markdown fences."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": self.temperature,
        }
        if self.max_tokens is not None and self.max_tokens > 0:
            payload["max_tokens"] = self.max_tokens

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
                raise InstructionFilterError(
                    f"Compatible API HTTP error: {details}"
                ) from exc
            except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
                if attempt >= self.max_retries:
                    raise InstructionFilterError(
                        "Compatible API request timed out or failed after "
                        f"{attempt} attempt(s). Increase "
                        "INSTRUCTION_FILTER_TIMEOUT_SECONDS, reduce "
                        "--max-file-chars, or check provider/model availability. "
                        f"Last error: {exc}"
                    ) from exc
                time.sleep(min(2 * attempt, 10))

        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as exc:
            preview = body[:500].replace("\n", "\\n")
            raise InstructionFilterError(
                "Compatible API returned a non-JSON response. Check "
                "INSTRUCTION_FILTER_BASE_URL or TASK_REVIEW_BASE_URL points to "
                f"a /v1 Chat Completions base URL. Response preview: {preview!r}"
            ) from exc
        try:
            return str(parsed["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise InstructionFilterError(
                f"Unexpected chat completion response: {body}"
            ) from exc


def normalize_base_url(value: str) -> str:
    base = value.strip().rstrip("/")
    suffix = "/chat/completions"
    if base.endswith(suffix):
        base = base[: -len(suffix)].rstrip("/")
    return base


def build_prompt(task_id: str, instruction: str) -> str:
    return f"""
You are an expert evaluator of task instructions. Your job is to score a given task instruction across several dimensions of clarity, testability, and naturalness.

Evaluate the instruction on the following 6 dimensions, each on a scale from 0 to 10:

1. Goal Clarity
Definition: Whether the task objective is explicit, concrete, and unambiguous rather than vague.
Common problems:
- vague action verbs
- missing deliverable specification
- undefined success criteria
- ambiguous scope
Scoring guide:
- 0-2: objective is highly vague or unclear
- 3-4: major ambiguity remains
- 5-6: partially clear but still underspecified
- 7-8: mostly clear and actionable
- 9-10: highly specific, concrete, and unambiguous

2. Input Clarity
Definition: Whether the required input, source material, system, file, version, or reference is clearly specified.
Common problems:
- unspecified data source, file, system, or version
- ambiguous qualifiers such as "latest"
- unclear which input should be used
Scoring guide:
- 0-2: essential input is missing or unclear
- 3-4: major input ambiguity
- 5-6: input is partially defined
- 7-8: input is mostly clear
- 9-10: input is fully and precisely specified

3. Constraint Completeness
Definition: Whether the instruction clearly specifies constraints, thresholds, filters, limits, timelines, exclusion criteria, formatting rules, and precision requirements.
Common problems:
- missing thresholds or limits
- missing timeline or deadline
- missing exclusions or filters
- vague precision requirements
Scoring guide:
- 0-2: constraints are largely missing
- 3-4: many important constraints are absent
- 5-6: some constraints are present but incomplete
- 7-8: constraints are mostly complete
- 9-10: constraints are comprehensive and precise

4. Referential Clarity
Definition: Whether all entities, actors, recipients, tools, pronouns, and domain references are clearly identifiable.
Common problems:
- missing actor or recipient
- referent ambiguity ("it", "they", "this")
- unclear tool, platform, or domain context
Scoring guide:
- 0-2: severe referential ambiguity
- 3-4: major confusion about actors or references
- 5-6: some ambiguity remains
- 7-8: mostly clear references
- 9-10: all references are explicit and unambiguous

5. Verifiability / Uniqueness of Evaluation
Definition: Whether the task output can be objectively and uniquely verified, ideally through deterministic checks such as unit tests, exact-match criteria, structured validation, or clearly bounded correctness conditions.
This is the most important dimension.
Key principle:
- High score: there is a clearly testable correct/incorrect criterion, or a tightly bounded expected output.
- Low score: the task is open-ended, subjective, creative, or allows many equally valid outputs.
Examples:
- High verifiability: "Write a Python function that returns the Fibonacci number for input n and passes the following pytest tests..."
- Low verifiability: "Summarize this article", "Write a persuasive email", "Brainstorm product ideas"
Scoring guide:
- 0-2: not objectively verifiable; highly open-ended
- 3-4: weak verification; many acceptable outputs
- 5-6: partially verifiable but still broad
- 7-8: mostly testable with limited ambiguity
- 9-10: strongly and uniquely verifiable with deterministic or near-deterministic evaluation

6. Human-Likeness of the Instruction
Definition: Whether the instruction sounds like something a real human would naturally ask, rather than an artificial, awkward, or machine-generated prompt.
Focus on:
- semantic coherence
- natural task logic
- realistic human intent
- normal phrasing and instruction style
Scoring guide:
- 0-2: highly unnatural or nonsensical
- 3-4: noticeably artificial
- 5-6: somewhat plausible but awkward
- 7-8: mostly natural and human-like
- 9-10: very natural, realistic, and human-like

Weighting:
Use the following weights when computing the final weighted average score:
- Goal Clarity: 0.15
- Input Clarity: 0.15
- Constraint Completeness: 0.15
- Referential Clarity: 0.10
- Verifiability / Uniqueness of Evaluation: 0.20
- Human-Likeness of the Instruction: 0.20

Instructions for evaluation:
- Be strict and discriminative in scoring.
- Do not give high scores unless the instruction truly deserves them.
- Penalize any ambiguity that would prevent a model or programmer from executing or validating the task reliably.
- For verifiability, prioritize whether the output can be uniquely checked, ideally by code, tests, schemas, exact criteria, or tightly constrained expectations.
- If the task is inherently open-ended, subjective, or admits many reasonable outputs, score verifiability low even if the instruction is otherwise clear.

Return your answer in the following JSON format only:

{{
  "goal_clarity": {{
    "score": <0-10>,
    "reason": "<brief explanation>"
  }},
  "input_clarity": {{
    "score": <0-10>,
    "reason": "<brief explanation>"
  }},
  "constraint_completeness": {{
    "score": <0-10>,
    "reason": "<brief explanation>"
  }},
  "referential_clarity": {{
    "score": <0-10>,
    "reason": "<brief explanation>"
  }},
  "verifiability_uniqueness": {{
    "score": <0-10>,
    "reason": "<brief explanation>"
  }},
  "human_likeness": {{
    "score": <0-10>,
    "reason": "<brief explanation>"
  }},
  "weighted_average": {{
    "score": <0-10>,
    "formula": "{FORMULA}"
  }}
}}

Task id: {task_id}

Now evaluate the following instruction:

--- instruction.md ---
{instruction}
--- end instruction.md ---
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
            raise InstructionFilterError(f"Provider did not return JSON: {text[:500]}")
        try:
            parsed = json.loads(match.group(0))
        except json.JSONDecodeError as fallback_exc:
            preview = stripped[:1200].replace("\n", "\\n")
            raise InstructionFilterError(
                "Provider returned malformed JSON. Increase "
                "INSTRUCTION_FILTER_MAX_TOKENS or reduce --max-file-chars. "
                f"Response preview: {preview!r}"
            ) from fallback_exc
    if not isinstance(parsed, dict):
        raise InstructionFilterError("Provider JSON response must be an object")
    return parsed


def normalize_output(raw: Mapping[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for name in DIMENSIONS:
        item = raw.get(name)
        if not isinstance(item, Mapping):
            raise InstructionFilterError(f"Judge response missing object: {name}")
        score = clamp_score(item.get("score"))
        reason = str(item.get("reason", "")).strip()
        normalized[name] = {"score": score, "reason": reason}

    weighted = compute_weighted_average(
        {name: normalized[name]["score"] for name in DIMENSIONS}
    )
    normalized["weighted_average"] = {
        "score": weighted,
        "formula": FORMULA,
    }
    return normalized


def clamp_score(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise InstructionFilterError(f"Expected numeric score, got {value!r}") from exc
    return round(min(10.0, max(0.0, number)), 2)


def compute_weighted_average(scores: Mapping[str, float]) -> float:
    return round(sum(WEIGHTS[name] * scores[name] for name in DIMENSIONS), 2)


def process_instruction(
    candidate: InstructionCandidate,
    provider: CompatibleInstructionProvider,
    output_root: Path,
    max_file_chars: int,
    skip_existing: bool = False,
) -> Dict[str, Any]:
    task_output_dir = output_root / candidate.task_id
    review_path = task_output_dir / REVIEW_FILE_NAME
    if skip_existing and review_path.is_file():
        return json.loads(review_path.read_text(encoding="utf-8"))

    instruction = read_text(candidate.instruction_path, max_file_chars)
    judge_output = provider.review(candidate.task_id, instruction)
    result = {
        "task_id": candidate.task_id,
        "instruction_path": str(candidate.instruction_path),
        "weighted_average": judge_output["weighted_average"]["score"],
        "judge_output": judge_output,
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
        "weighted_average",
        "goal_clarity",
        "input_clarity",
        "constraint_completeness",
        "referential_clarity",
        "verifiability_uniqueness",
        "human_likeness",
        "instruction_path",
    ]
    with (output_root / "summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(summary_row(result))


def summary_row(result: Mapping[str, Any]) -> Dict[str, Any]:
    output = result.get("judge_output", {})
    return {
        "task_id": result.get("task_id", ""),
        "weighted_average": result.get("weighted_average", ""),
        "goal_clarity": dimension_score(output, "goal_clarity"),
        "input_clarity": dimension_score(output, "input_clarity"),
        "constraint_completeness": dimension_score(output, "constraint_completeness"),
        "referential_clarity": dimension_score(output, "referential_clarity"),
        "verifiability_uniqueness": dimension_score(output, "verifiability_uniqueness"),
        "human_likeness": dimension_score(output, "human_likeness"),
        "instruction_path": result.get("instruction_path", ""),
    }


def dimension_score(output: Any, name: str) -> Any:
    if not isinstance(output, Mapping):
        return ""
    item = output.get(name, {})
    if not isinstance(item, Mapping):
        return ""
    return item.get("score", "")


def first_env(*names: str, default: Optional[str] = None) -> Optional[str]:
    for name in names:
        value = os.environ.get(name)
        if value is not None and value.strip():
            return value
    return default


def make_provider(args: argparse.Namespace) -> CompatibleInstructionProvider:
    provider_name = (
        args.provider
        or first_env("INSTRUCTION_FILTER_PROVIDER", "TASK_REVIEW_PROVIDER")
        or "compatible"
    )
    if provider_name not in {"compatible", "openai"}:
        raise InstructionFilterError(f"Unknown provider: {provider_name}")

    model = args.model or first_env("INSTRUCTION_FILTER_MODEL", "TASK_REVIEW_MODEL")
    if not model:
        raise InstructionFilterError(
            "A model is required. Pass --model or set INSTRUCTION_FILTER_MODEL "
            "or TASK_REVIEW_MODEL in .env."
        )
    timeout_seconds = args.timeout_seconds
    if timeout_seconds is None:
        timeout_seconds = int(
            first_env(
                "INSTRUCTION_FILTER_TIMEOUT_SECONDS",
                "TASK_REVIEW_TIMEOUT_SECONDS",
                default="120",
            )
        )
    temperature = args.temperature
    if temperature is None:
        temperature = float(
            first_env(
                "INSTRUCTION_FILTER_TEMPERATURE",
                "TASK_REVIEW_TEMPERATURE",
                default="0",
            )
        )
    max_retries = args.max_retries
    if max_retries is None:
        max_retries = int(
            first_env(
                "INSTRUCTION_FILTER_MAX_RETRIES",
                "TASK_REVIEW_MAX_RETRIES",
                default="1",
            )
        )
    max_tokens = args.max_tokens
    if max_tokens is None:
        raw_max_tokens = first_env(
            "INSTRUCTION_FILTER_MAX_TOKENS",
            "TASK_REVIEW_MAX_TOKENS",
            default="",
        )
        max_tokens = int(raw_max_tokens) if raw_max_tokens else None
    json_retries = args.json_retries
    if json_retries is None:
        json_retries = int(
            first_env(
                "INSTRUCTION_FILTER_JSON_RETRIES",
                "TASK_REVIEW_JSON_RETRIES",
                default="2",
            )
        )
    return CompatibleInstructionProvider(
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
        description="Score instruction.md files for clarity, testability, and naturalness."
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
        default=Path("instruction_filter_output"),
        help="Output directory for instruction_review.json and summaries.",
    )
    parser.add_argument(
        "--provider",
        choices=("compatible", "openai"),
        default=None,
        help=(
            "Provider. Defaults to INSTRUCTION_FILTER_PROVIDER, "
            "TASK_REVIEW_PROVIDER, or compatible."
        ),
    )
    parser.add_argument("--model", default=None, help="OpenAI-compatible model.")
    parser.add_argument(
        "--api-key",
        default=None,
        help=(
            "API key. Defaults to INSTRUCTION_FILTER_API_KEY, "
            "TASK_REVIEW_API_KEY, or OPENAI_API_KEY."
        ),
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help=(
            "Base URL. Defaults to INSTRUCTION_FILTER_BASE_URL, "
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
            "INSTRUCTION_FILTER_MAX_RETRIES, TASK_REVIEW_MAX_RETRIES, or 1."
        ),
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help=(
            "Optional response token cap. Defaults to INSTRUCTION_FILTER_MAX_TOKENS "
            "or TASK_REVIEW_MAX_TOKENS if set."
        ),
    )
    parser.add_argument(
        "--json-retries",
        type=int,
        default=None,
        help=(
            "Retry count for malformed/missing-field model JSON. Defaults to "
            "INSTRUCTION_FILTER_JSON_RETRIES, TASK_REVIEW_JSON_RETRIES, or 2."
        ),
    )
    parser.add_argument(
        "--max-file-chars",
        type=int,
        default=60000,
        help="Maximum characters read from instruction.md before middle truncation.",
    )
    parser.add_argument("--limit", type=int, default=0, help="0 means no limit.")
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help=(
            "If output/<task_id>/instruction_review.json already exists, reuse it "
            "and skip model calls for that task."
        ),
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        load_env_file(args.env_file)
        provider = make_provider(args)
        candidates = discover_instructions(args.roots)
        if args.limit and args.limit > 0:
            candidates = candidates[: args.limit]
        if not candidates:
            raise InstructionFilterError("No instruction.md files found.")

        results: List[Mapping[str, Any]] = []
        for index, candidate in enumerate(candidates, start=1):
            print(f"[{index}/{len(candidates)}] scoring {candidate.task_id}", flush=True)
            result = process_instruction(
                candidate,
                provider,
                args.output,
                max_file_chars=args.max_file_chars,
                skip_existing=args.skip_existing,
            )
            results.append(result)
        write_summaries(args.output, results)
        print(
            f"Scored {len(results)} instruction(s). Output: {args.output.resolve()}",
            flush=True,
        )
        return 0
    except InstructionFilterError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
