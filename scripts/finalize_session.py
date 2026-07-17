#!/usr/bin/env python3
"""Finalize an evidence-bearing learning session across every progress artifact."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
from datetime import UTC, date, datetime
from pathlib import Path

from create_lesson import load_index
from update_lesson import resolve_entry


STATE_START = "<!-- PLC:SESSION-PROGRESS:START -->"
STATE_END = "<!-- PLC:SESSION-PROGRESS:END -->"
LESSON_START = "<!-- PLC:SESSION-FINALIZE:START -->"
LESSON_END = "<!-- PLC:SESSION-FINALIZE:END -->"
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLAN_FILE_NAME = "LEARNING_PLAN.json"


def timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def replace_managed_block(text: str, start: str, end: str, block: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if pattern.search(text):
        return pattern.sub(block, text, count=1)
    return text.rstrip() + "\n\n" + block + "\n"


def upsert_state_block(text: str, block: str) -> str:
    pattern = re.compile(re.escape(STATE_START) + r".*?" + re.escape(STATE_END), re.DOTALL)
    if pattern.search(text):
        return pattern.sub(block, text, count=1)
    updated_line = re.search(r"^Last updated:.*$", text, re.MULTILINE)
    if updated_line:
        position = updated_line.end()
        return text[:position] + "\n\n" + block + text[position:]
    return block + "\n\n" + text


def update_last_updated(text: str, record_date: str) -> str:
    pattern = re.compile(r"^Last updated:.*$", re.MULTILINE)
    if pattern.search(text):
        return pattern.sub(f"Last updated: {record_date}", text, count=1)
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines.insert(1, "")
        lines.insert(2, f"Last updated: {record_date}")
        return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return f"Last updated: {record_date}\n\n{text}"


def build_record(args: argparse.Namespace) -> str:
    prediction = args.prediction or "Pending; not yet supplied by the learner."
    ipo = args.ipo or "Pending; the learner has not yet submitted a complete explanation."
    return f"""# {args.record_date} {args.record_title}

## Practiced ability
{args.practiced_ability}

## Independent completion
- Baseline level: {args.baseline_level}
- Support needed: {args.support_needed}
- Resulting level: {args.resulting_level}

## Evidence
- Prediction: {prediction}
- User-run result: {args.user_run_result}
- Input / Process / Output: {ipo}

## Learned
{args.learned}

## Acceptance
- Session status: {args.status}
- Can run: {args.can_run}
- Result correct: {args.result_correct}
- Tests sufficient: {args.tests_sufficient}
- Meets today's floor: {args.meets_floor}
- Current gap: {args.current_gap}

## Next target
{args.next_target}
"""


def build_lesson_text(text: str, args: argparse.Namespace, record_rel: str) -> str:
    block = f"""{LESSON_START}
  <section>
    <h2>Recorded Session Result</h2>
    <ul>
      <li>Status: {html.escape(args.status)}</li>
      <li>Evidence: {html.escape(args.evidence_summary)}</li>
      <li>Learning record: {html.escape(record_rel)}</li>
      <li>Current gap: {html.escape(args.current_gap)}</li>
      <li>Next target: {html.escape(args.next_target)}</li>
      <li>Independent level: {html.escape(args.resulting_level)}</li>
    </ul>
  </section>
{LESSON_END}"""
    if LESSON_START in text:
        return replace_managed_block(text, LESSON_START, LESSON_END, block)
    if "</body>" not in text:
        raise ValueError("Lesson does not contain </body>")
    return text.replace("</body>", block + "\n</body>", 1)


def checkpoint_by_id(plan: dict, checkpoint_id: str) -> dict:
    matches = [item for item in plan.get("checkpoints", []) if item.get("id") == checkpoint_id]
    if len(matches) != 1:
        raise ValueError(f"Expected one checkpoint for {checkpoint_id!r}, found {len(matches)}")
    return matches[0]


def update_plan(
    plan: dict,
    checkpoint_id: str,
    args: argparse.Namespace,
    lesson_rel: str,
    record_rel: str,
) -> None:
    if plan.get("current_checkpoint") != checkpoint_id:
        raise ValueError(
            "Session checkpoint does not match LEARNING_PLAN.json.current_checkpoint: "
            f"{checkpoint_id!r} != {plan.get('current_checkpoint')!r}"
        )
    checkpoint = checkpoint_by_id(plan, checkpoint_id)
    plan["updated_at"] = args.record_date
    checkpoint["updated_at"] = timestamp()
    checkpoint["progress"] = {
        "session_status": args.status,
        "lesson": lesson_rel,
        "learning_record": record_rel,
        "evidence": args.evidence_summary,
        "current_gap": args.current_gap,
        "next_target": args.next_target,
        "independent_level": args.resulting_level,
        "updated_at": checkpoint["updated_at"],
    }
    if args.status == "in-progress":
        checkpoint["status"] = "in-progress"
        return

    checkpoint["status"] = "complete"
    checkpoint["evidence"] = args.evidence_summary
    next_id = checkpoint.get("next_checkpoint")
    plan["current_checkpoint"] = next_id
    if next_id:
        next_checkpoint = checkpoint_by_id(plan, next_id)
        if next_checkpoint["status"] == "pending":
            next_checkpoint["status"] = "in-progress"
            next_checkpoint["updated_at"] = timestamp()


def build_state_block(
    args: argparse.Namespace,
    lesson_rel: str,
    record_rel: str,
    recorded_checkpoint: str | None,
    active_checkpoint: str | None,
) -> str:
    checkpoint_label = recorded_checkpoint or "not-configured"
    if recorded_checkpoint and not active_checkpoint and args.status == "complete":
        plan_target = "plan-complete"
    else:
        plan_target = active_checkpoint or "not-configured"
    return f"""{STATE_START}
## Latest Recorded Session

- Lesson: {lesson_rel}
- Learning record: {record_rel}
- Recorded checkpoint: {checkpoint_label}
- Session status: {args.status}
- Independent level: {args.resulting_level}
- Evidence: {args.evidence_summary}
- Current gap: {args.current_gap}
- Current plan checkpoint: {plan_target}
- Only next task: {args.next_target}
{STATE_END}"""


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    temp_path.write_text(text, encoding="utf-8")
    temp_path.replace(path)


def write_all(changes: dict[Path, str]) -> None:
    originals = {path: path.read_text(encoding="utf-8") if path.exists() else None for path in changes}
    written: list[Path] = []
    try:
        for path, text in changes.items():
            atomic_write(path, text)
            written.append(path)
    except Exception:
        for path in reversed(written):
            original = originals[path]
            if original is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, original)
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--lesson", required=True, help="Lesson id, filename, or path")
    parser.add_argument(
        "--checkpoint",
        help="Optional checkpoint id when the workspace uses LEARNING_PLAN.json",
    )
    parser.add_argument("--status", choices=["in-progress", "complete"], required=True)
    parser.add_argument("--record-date", default=date.today().isoformat())
    parser.add_argument("--record-slug", required=True)
    parser.add_argument("--record-title", required=True)
    parser.add_argument("--practiced-ability", required=True)
    parser.add_argument("--baseline-level", choices=["unassessed", "0", "1", "2", "3"], required=True)
    parser.add_argument("--resulting-level", choices=["unassessed", "0", "1", "2", "3"], required=True)
    parser.add_argument("--support-needed", required=True)
    parser.add_argument("--prediction")
    parser.add_argument("--user-run-result", required=True)
    parser.add_argument("--ipo")
    parser.add_argument("--learned", required=True)
    parser.add_argument("--can-run", choices=["yes", "no", "pending"], required=True)
    parser.add_argument("--result-correct", choices=["yes", "no", "pending"], required=True)
    parser.add_argument("--tests-sufficient", choices=["yes", "no", "pending"], required=True)
    parser.add_argument("--meets-floor", choices=["yes", "no"], required=True)
    parser.add_argument("--current-gap", required=True)
    parser.add_argument("--next-target", required=True)
    parser.add_argument("--evidence-summary", required=True)
    parser.add_argument(
        "--preserve-existing-record",
        action="store_true",
        help="Keep an existing record while reconciling the other artifacts",
    )
    args = parser.parse_args()
    if not SLUG_PATTERN.fullmatch(args.record_slug):
        parser.error("--record-slug must use lowercase dash-case")
    try:
        date.fromisoformat(args.record_date)
    except ValueError:
        parser.error("--record-date must use YYYY-MM-DD")
    if args.status == "complete":
        missing = [name for name in ("prediction", "ipo") if not getattr(args, name)]
        if missing:
            parser.error("complete status requires --prediction and --ipo")
        if (
            args.can_run != "yes"
            or args.result_correct != "yes"
            or args.tests_sufficient != "yes"
            or args.meets_floor != "yes"
        ):
            parser.error(
                "complete status requires can-run=yes, result-correct=yes, "
                "tests-sufficient=yes, and meets-floor=yes"
            )
    return args


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    state_path = workspace / "CURRENT_LEARNING_STATE.md"

    index = load_index(workspace)
    entry = resolve_entry(index, args.lesson)
    lesson_checkpoint = entry.get("plan_checkpoint")
    if args.checkpoint and lesson_checkpoint and lesson_checkpoint != args.checkpoint:
        raise ValueError("Lesson plan_checkpoint does not match --checkpoint")
    checkpoint_id = args.checkpoint or lesson_checkpoint
    lesson_path = (workspace / entry["path"]).resolve()
    lessons_dir = (workspace / "lessons").resolve()
    if lessons_dir not in lesson_path.parents or not lesson_path.exists():
        raise ValueError(f"Invalid lesson path: {lesson_path}")

    record_rel = f"learning-records/{args.record_date}-{args.record_slug}.md"
    record_path = workspace / record_rel
    if args.preserve_existing_record and not record_path.exists():
        raise FileNotFoundError(f"Cannot preserve missing record: {record_path}")

    plan_path = workspace / PLAN_FILE_NAME
    plan = None
    if plan_path.exists():
        if not checkpoint_id:
            raise ValueError(
                "Workspace has LEARNING_PLAN.json, but the lesson is not bound to a checkpoint"
            )
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        update_plan(plan, checkpoint_id, args, entry["path"], record_rel)
    elif args.checkpoint:
        raise FileNotFoundError(
            f"--checkpoint was supplied but the workspace has no {PLAN_FILE_NAME}: {plan_path}"
        )

    entry["status"] = args.status
    entry["updated_at"] = timestamp()
    entry["last_evidence"] = args.evidence_summary
    entry["next_review"] = args.next_target
    entry["independent_level"] = args.resulting_level
    entry["learning_record"] = record_rel

    lesson_text = build_lesson_text(
        lesson_path.read_text(encoding="utf-8"), args, record_rel
    )
    if state_path.exists():
        original_state = state_path.read_text(encoding="utf-8")
    else:
        original_state = "# Current Learning State\n"
    state_text = update_last_updated(original_state, args.record_date)
    state_block = build_state_block(
        args,
        entry["path"],
        record_rel,
        checkpoint_id,
        plan.get("current_checkpoint") if plan else None,
    )
    state_text = upsert_state_block(state_text, state_block)

    changes = {
        lesson_path: lesson_text,
        workspace / "lesson-index.json": json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        state_path: state_text,
    }
    if plan is not None:
        changes[plan_path] = json.dumps(plan, ensure_ascii=False, indent=2) + "\n"
    if not args.preserve_existing_record:
        changes[record_path] = build_record(args)
    write_all(changes)

    result = {
        "status": args.status,
        "lesson": str(lesson_path),
        "learning_record": str(record_path),
        "current_state": str(state_path),
        "learning_plan": str(plan_path) if plan is not None else None,
        "current_checkpoint": plan.get("current_checkpoint") if plan else None,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
