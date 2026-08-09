#!/usr/bin/env python3
"""Update one lesson lifecycle entry without turning it into an answer key."""

from __future__ import annotations

import argparse
import html
from pathlib import Path

from create_lesson import LESSON_TYPES, load_index, now, save_index


def resolve_entry(index: dict, selector: str) -> dict:
    matches = [entry for entry in index["lessons"] if selector in {entry["id"], entry["path"], Path(entry["path"]).name}]
    if len(matches) != 1:
        raise ValueError(f"Expected one lesson for {selector!r}, found {len(matches)}")
    return matches[0]


def append_update(path: Path, details: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if "</body>" not in text:
        raise ValueError(f"Lesson does not contain </body>: {path}")
    section = "\n  <section><h2>Session Update</h2><ul>\n"
    section += "\n".join(f"    <li>{html.escape(detail)}</li>" for detail in details)
    section += "\n  </ul></section>\n"
    path.write_text(text.replace("</body>", section + "</body>", 1), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--lesson", required=True)
    parser.add_argument("--status", choices=["prepared", "in-progress", "complete"], required=True)
    parser.add_argument("--evidence")
    parser.add_argument("--next-review")
    parser.add_argument("--independent-level", choices=["unassessed", "0", "1", "2", "3"])
    parser.add_argument("--support-level", choices=["unassessed", "step-by-step", "light-guidance", "independent"])
    parser.add_argument("--lesson-type", choices=LESSON_TYPES)
    parser.add_argument("--why-now")
    parser.add_argument("--resume-decision", choices=["continue", "shrink", "restructure"])
    parser.add_argument("--comparison-note")
    args = parser.parse_args()
    if args.status == "complete" and not args.evidence:
        parser.error("--evidence is required when --status is complete")
    if args.status == "in-progress" and bool(args.resume_decision) != bool(args.comparison_note):
        parser.error("--resume-decision and --comparison-note must be provided together")
    return args


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    index = load_index(workspace)
    entry = resolve_entry(index, args.lesson)
    lesson_path = (workspace / entry["path"]).resolve()
    lessons_dir = (workspace / "lessons").resolve()
    if lessons_dir not in lesson_path.parents or not lesson_path.is_file():
        raise ValueError(f"Invalid lesson path: {lesson_path}")
    details = [f"Status: {args.status}"]
    for label, value in (("Evidence", args.evidence), ("Next review", args.next_review), ("Independent level", args.independent_level), ("Support level", args.support_level), ("Resume decision", args.resume_decision), ("Evidence comparison", args.comparison_note)):
        if value:
            details.append(f"{label}: {value}")
    append_update(lesson_path, details)
    entry["status"] = args.status
    entry["updated_at"] = now()
    for field, value in (("last_evidence", args.evidence), ("next_review", args.next_review), ("independent_level", args.independent_level), ("support_level", args.support_level), ("lesson_type", args.lesson_type), ("why_now", args.why_now), ("resume_decision", args.resume_decision), ("comparison_note", args.comparison_note)):
        if value:
            entry[field] = value
    save_index(workspace, index)
    print(lesson_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
