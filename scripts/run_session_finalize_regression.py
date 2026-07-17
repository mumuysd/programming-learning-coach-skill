#!/usr/bin/env python3
"""Regression checks for evidence-bearing session finalization."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
CREATE_LESSON = SCRIPT_DIR / "create_lesson.py"
FINALIZE_SESSION = SCRIPT_DIR / "finalize_session.py"


def run(command: list[str], expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if expect_success and result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)
    if not expect_success and result.returncode == 0:
        raise AssertionError("Command unexpectedly succeeded")
    return result


def make_workspace(root: Path, include_plan: bool = True) -> Path:
    workspace = root / "workspace"
    workspace.mkdir()
    (workspace / "CURRENT_LEARNING_STATE.md").write_text(
        "# Current Learning State\n\nLast updated: 2026-01-01\n",
        encoding="utf-8",
    )
    plan = {
        "version": 1,
        "current_checkpoint": "checkpoint-one",
        "checkpoints": [
            {
                "id": "checkpoint-one",
                "title": "First",
                "status": "in-progress",
                "next_checkpoint": "checkpoint-two",
            },
            {
                "id": "checkpoint-two",
                "title": "Second",
                "status": "pending",
                "next_checkpoint": None,
            },
        ],
    }
    if include_plan:
        (workspace / "LEARNING_PLAN.json").write_text(
            json.dumps(plan, indent=2) + "\n", encoding="utf-8"
        )
    create_command = [
        sys.executable,
        str(CREATE_LESSON),
        "--workspace",
        str(workspace),
        "--topic",
        "Test lesson",
        "--slug",
        "test-lesson",
        "--goal",
        "Practice one small ability.",
        "--concept",
        "loop",
        "--input",
        "A short list.",
        "--process",
        "Iterate over each item.",
        "--output",
        "The observed values.",
        "--prediction",
        "Predict the first value.",
        "--step",
        "Run locally.",
        "--independent-level",
        "1",
        "--time-box",
        "20 minutes",
        "--minimum-version",
        "One local run.",
        "--not-today",
        "No extra feature.",
        "--required-evidence",
        "Prediction, local run, and IPO.",
    ]
    if include_plan:
        create_command.extend(["--plan-checkpoint", "checkpoint-one"])
    run(create_command)
    return workspace


def finalize_command(workspace: Path, status: str, include_plan: bool = True) -> list[str]:
    command = [
        sys.executable,
        str(FINALIZE_SESSION),
        "--workspace",
        str(workspace),
        "--lesson",
        "0001",
        "--status",
        status,
        "--record-date",
        "2026-01-02",
        "--record-slug",
        "test-progress",
        "--record-title",
        "Test progress",
        "--practiced-ability",
        "Read and explain a loop.",
        "--baseline-level",
        "1",
        "--resulting-level",
        "1",
        "--support-needed",
        "one hint",
        "--user-run-result",
        "The learner ran the file and inspected the first value.",
        "--learned",
        "The learner connected the loop variable to the current item.",
        "--can-run",
        "yes",
        "--result-correct",
        "yes",
        "--tests-sufficient",
        "pending" if status == "in-progress" else "yes",
        "--meets-floor",
        "no" if status == "in-progress" else "yes",
        "--current-gap",
        "A complete IPO explanation is still pending." if status == "in-progress" else "None.",
        "--next-target",
        "Explain IPO." if status == "in-progress" else "Start checkpoint two.",
        "--evidence-summary",
        "Learner prediction and local run evidence.",
    ]
    if include_plan:
        command.extend(["--checkpoint", "checkpoint-one"])
    if status == "complete":
        command.extend(
            [
                "--prediction",
                "The first value will be alpha.",
                "--ipo",
                "Input is a list; process iterates; output is each value.",
            ]
        )
    return command


def assert_progress_close() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        workspace = make_workspace(Path(temp_dir))
        run(finalize_command(workspace, "in-progress"))
        record_path = workspace / "learning-records/2026-01-02-test-progress.md"
        assert record_path.exists()
        assert "Session status: in-progress" in record_path.read_text(encoding="utf-8")
        assert "PLC:SESSION-PROGRESS:START" in (
            workspace / "CURRENT_LEARNING_STATE.md"
        ).read_text(encoding="utf-8")
        assert "PLC:SESSION-FINALIZE:START" in (
            workspace / "lessons/0001-test-lesson.html"
        ).read_text(encoding="utf-8")
        plan = json.loads((workspace / "LEARNING_PLAN.json").read_text(encoding="utf-8"))
        assert plan["current_checkpoint"] == "checkpoint-one"
        assert plan["checkpoints"][0]["progress"]["learning_record"].endswith(
            "test-progress.md"
        )


def assert_complete_advances() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        workspace = make_workspace(Path(temp_dir))
        run(finalize_command(workspace, "complete"))
        plan = json.loads((workspace / "LEARNING_PLAN.json").read_text(encoding="utf-8"))
        assert plan["current_checkpoint"] == "checkpoint-two"
        assert plan["checkpoints"][0]["status"] == "complete"
        assert plan["checkpoints"][1]["status"] == "in-progress"
        index = json.loads((workspace / "lesson-index.json").read_text(encoding="utf-8"))
        assert index["lessons"][0]["status"] == "complete"


def assert_workspace_without_plan() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        workspace = make_workspace(Path(temp_dir), include_plan=False)
        result = run(finalize_command(workspace, "in-progress", include_plan=False))
        output = json.loads(result.stdout)
        assert output["learning_plan"] is None
        assert output["current_checkpoint"] is None
        assert (workspace / "learning-records/2026-01-02-test-progress.md").exists()
        state = (workspace / "CURRENT_LEARNING_STATE.md").read_text(encoding="utf-8")
        assert "Current plan checkpoint: not-configured" in state
        run(finalize_command(workspace, "complete", include_plan=False))
        index = json.loads((workspace / "lesson-index.json").read_text(encoding="utf-8"))
        assert index["lessons"][0]["status"] == "complete"


def assert_incomplete_evidence_cannot_complete() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        workspace = make_workspace(Path(temp_dir))
        before_plan = (workspace / "LEARNING_PLAN.json").read_text(encoding="utf-8")
        result = run(finalize_command(workspace, "complete")[:-4], expect_success=False)
        assert "requires --prediction and --ipo" in result.stderr
        assert (workspace / "LEARNING_PLAN.json").read_text(encoding="utf-8") == before_plan
        assert not (workspace / "learning-records").exists()


def main() -> int:
    assert_progress_close()
    assert_complete_advances()
    assert_workspace_without_plan()
    assert_incomplete_evidence_cannot_complete()
    print("Session finalization regression: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
