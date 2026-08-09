#!/usr/bin/env python3
"""Run isolated Agent sessions against the public lesson-preflight contract."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Scenario:
    name: str
    prompt: str
    needs_teaching_block: bool


SCENARIOS = (
    Scenario("start", "Teach a new Python lesson on choosing direct dictionary lookup or get. Use the registered source and create the lesson before coaching.", True),
    Scenario("debug", "Start a learning-oriented debugging session for Python KeyError: 'status'. Do not give a full fix first.", False),
)


def write_fixture(workspace: Path) -> None:
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "CURRENT_LEARNING_STATE.md").write_text("# Current Learning State\n\nNo active lesson.\n", encoding="utf-8")
    (workspace / "RESOURCES.md").write_text(
        "# Programming Resources\n\n- [Python dict documentation](https://docs.python.org/3/library/stdtypes.html#dict)\n  Covers: dictionary lookup behavior. Use for: direct indexing and get.\n",
        encoding="utf-8",
    )


def first_nonempty_line(response: str) -> str:
    return next((line.strip() for line in response.splitlines() if line.strip()), "")


def normalized_path(value: str) -> Path:
    markdown = re.fullmatch(r"\[[^\]]+\]\(([^)]+)\)", value)
    path = markdown.group(1) if markdown else value.strip("`")
    if path.startswith("/var/"):
        path = "/private" + path
    return Path(path).expanduser().resolve()


def verify(workspace: Path, response: str, scenario: Scenario) -> dict:
    first = first_nonempty_line(response)
    prefix = "学习资料已生成："
    if not first.startswith(prefix):
        raise AssertionError(f"first response line must start with {prefix!r}: {first!r}")
    lesson = normalized_path(first.removeprefix(prefix).strip())
    lessons = (workspace / "lessons").resolve()
    if lessons not in lesson.parents or not lesson.is_file():
        raise AssertionError(f"reported lesson is missing or outside fixture: {lesson}")
    content = lesson.read_text(encoding="utf-8")
    required = ("Session Contract", "Before You Run", "Exercise Steps")
    if any(marker not in content for marker in required):
        raise AssertionError(f"lesson missing core sections: {lesson}")
    if any(marker in content for marker in ("<pre>", "Answer Key", "Final Answer", "完整答案")):
        raise AssertionError(f"lesson leaked answer-like markup: {lesson}")
    if scenario.needs_teaching_block:
        for marker in ("New Knowledge", "Core Explanations", "Decision Rule", "Contrasting Cases", "How It Works"):
            if marker not in content:
                raise AssertionError(f"new-knowledge lesson missing {marker}: {lesson}")
    index = json.loads((workspace / "lesson-index.json").read_text(encoding="utf-8"))
    entries = [entry for entry in index["lessons"] if entry["path"] == str(lesson.relative_to(workspace.resolve()))]
    if len(entries) != 1 or entries[0]["status"] != "prepared":
        raise AssertionError("lesson index lacks a prepared entry")
    if scenario.needs_teaching_block and len(entries[0].get("teaching_content", {}).get("explanations", [])) < 2:
        raise AssertionError("lesson index lacks substantive teaching metadata")
    if "```" in response:
        raise AssertionError("first teaching response must not include a code block")
    return {"scenario": scenario.name, "lesson_path": str(lesson), "first_line": first}


def run_scenario(codex_bin: str, root: Path, scenario: Scenario, timeout: int) -> dict:
    workspace = root / scenario.name
    write_fixture(workspace)
    output = workspace / "agent-last-message.txt"
    prompt = f"Use $programming-learning-coach. The learning workspace is {workspace}. Do not use any other workspace. {scenario.prompt}"
    completed = subprocess.run(
        [codex_bin, "-a", "never", "exec", "--ignore-user-config", "--ephemeral", "--skip-git-repo-check", "--sandbox", "workspace-write", "-C", str(workspace), "-o", str(output), prompt],
        text=True, capture_output=True, stdin=subprocess.DEVNULL, timeout=timeout,
    )
    if completed.returncode:
        raise AssertionError(f"Codex failed for {scenario.name}: {completed.stderr.strip()}")
    if not output.is_file():
        raise AssertionError(f"Codex wrote no response for {scenario.name}")
    return verify(workspace, output.read_text(encoding="utf-8"), scenario)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--timeout-seconds", type=int, default=420)
    parser.add_argument("--scenario", action="append", choices=[scenario.name for scenario in SCENARIOS])
    args = parser.parse_args()
    selected = [scenario for scenario in SCENARIOS if not args.scenario or scenario.name in args.scenario]
    try:
        with tempfile.TemporaryDirectory(prefix="programming-learning-coach-regression-") as temp:
            report = {"status": "passed", "scenarios": [run_scenario(args.codex_bin, Path(temp), scenario, args.timeout_seconds) for scenario in selected]}
    except (AssertionError, subprocess.TimeoutExpired) as error:
        report = {"status": "failed", "error": str(error)}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
