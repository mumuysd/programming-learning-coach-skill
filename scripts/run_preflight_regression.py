#!/usr/bin/env python3
"""Run three isolated Codex sessions and verify the lesson-preflight contract."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Scenario:
    name: str
    prompt: str
    state: str
    review_queue: str | None = None


SCENARIOS = (
    Scenario(
        name="start",
        prompt="Start today's programming learning session about dictionary basics.",
        state="Next topic: learn dictionary basics with one small project value.\n",
    ),
    Scenario(
        name="debug",
        prompt="Start a learning-oriented debugging session for pandas KeyError: 'status'.",
        state="Next topic: debug one pandas column lookup error.\n",
    ),
    Scenario(
        name="review",
        prompt="Start a review session for Python functions and return values.",
        state="Next topic: review a previously learned function concept.\n",
        review_queue="# Review: function-return\n\n## Prompt\nPredict what a small function returns.\n",
    ),
)


def write_fixture(workspace: Path, scenario: Scenario) -> None:
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "CURRENT_LEARNING_STATE.md").write_text(scenario.state, encoding="utf-8")
    if scenario.review_queue:
        queue_dir = workspace / "review-queue"
        queue_dir.mkdir()
        (queue_dir / "function-return.md").write_text(scenario.review_queue, encoding="utf-8")


def first_nonempty_line(response: str) -> str:
    for line in response.splitlines():
        if line.strip():
            return line.strip()
    raise AssertionError("Agent response is empty")


def verify_artifacts(workspace: Path, response: str) -> dict:
    first_line = first_nonempty_line(response)
    prefix = "学习资料已生成："
    if not first_line.startswith(prefix):
        raise AssertionError(f"First response line must start with {prefix!r}: {first_line!r}")
    lesson_path = Path(first_line.removeprefix(prefix).strip()).expanduser().resolve()
    lessons_dir = (workspace / "lessons").resolve()
    if lessons_dir not in lesson_path.parents or not lesson_path.is_file():
        raise AssertionError(f"Reported lesson is missing or outside fixture: {lesson_path}")
    lesson_html = lesson_path.read_text(encoding="utf-8")
    required = (
        "<h2>Goal</h2>",
        "<h2>Session Contract</h2>",
        "<h2>Before You Run</h2>",
        "<h2>Exercise Steps</h2>",
    )
    forbidden = ("<pre>", "<code>", "Answer Key", "Final Answer", "完整答案")
    if any(marker not in lesson_html for marker in required):
        raise AssertionError(f"Lesson is missing required sections: {lesson_path}")
    if any(marker in lesson_html for marker in forbidden):
        raise AssertionError(f"Lesson contains answer-like markup: {lesson_path}")
    index = json.loads((workspace / "lesson-index.json").read_text(encoding="utf-8"))
    matching = [entry for entry in index["lessons"] if entry["path"] == str(lesson_path.relative_to(workspace))]
    if (
        len(matching) != 1
        or matching[0]["status"] != "prepared"
        or matching[0].get("independent_level") not in {"unassessed", "0", "1", "2", "3"}
        or not matching[0].get("minimum_version")
    ):
        raise AssertionError(f"Lesson index is missing the prepared entry: {lesson_path}")
    if "```" in response:
        raise AssertionError("First teaching response must not include a code block")
    return {"lesson_path": str(lesson_path), "first_line": first_line}


def run_scenario(codex_bin: str, root: Path, scenario: Scenario, timeout_seconds: int) -> dict:
    workspace = root / scenario.name
    response_path = workspace / "agent-last-message.txt"
    write_fixture(workspace, scenario)
    prompt = (
        f"Use $programming-learning-coach. The learning workspace for this session is {workspace}. "
        "Do not use any other workspace. "
        f"{scenario.prompt}"
    )
    command = [
        codex_bin,
        "-a",
        "never",
        "exec",
        "--ephemeral",
        "--skip-git-repo-check",
        "--sandbox",
        "workspace-write",
        "-C",
        str(workspace),
        "-o",
        str(response_path),
        prompt,
    ]
    try:
        completed = subprocess.run(
            command, text=True, capture_output=True, timeout=timeout_seconds
        )
    except subprocess.TimeoutExpired as error:
        raise AssertionError(
            f"Codex timed out for {scenario.name} after {timeout_seconds}s. "
            "Check Codex authentication, approval policy, and model availability."
        ) from error
    if completed.returncode != 0:
        raise AssertionError(f"Codex failed for {scenario.name}: {completed.stderr.strip()}")
    if not response_path.is_file():
        raise AssertionError(f"Codex wrote no final response for {scenario.name}")
    result = verify_artifacts(workspace, response_path.read_text(encoding="utf-8"))
    result["scenario"] = scenario.name
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-bin", default="codex", help="Codex CLI command")
    parser.add_argument("--report", type=Path, help="Optional JSON report path")
    parser.add_argument(
        "--timeout-seconds", type=int, default=90, help="Maximum duration per isolated session"
    )
    args = parser.parse_args()
    try:
        with tempfile.TemporaryDirectory(prefix="programming-learning-coach-regression-") as temp_dir:
            root = Path(temp_dir)
            results = [
                run_scenario(args.codex_bin, root, scenario, args.timeout_seconds)
                for scenario in SCENARIOS
            ]
    except AssertionError as error:
        report = {"status": "failed", "error": str(error)}
        rendered = json.dumps(report, ensure_ascii=False, indent=2)
        if args.report:
            args.report.write_text(rendered + "\n", encoding="utf-8")
        print(rendered)
        return 1
    report = {"status": "passed", "scenarios": results}
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
