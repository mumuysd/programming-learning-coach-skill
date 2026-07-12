#!/usr/bin/env python3
"""Update an existing lesson's lifecycle status and lesson index entry."""

from __future__ import annotations

import argparse
import html
from pathlib import Path

from create_lesson import load_index, now, save_index


def resolve_entry(index: dict, selector: str) -> dict:
    matches = [
        entry
        for entry in index["lessons"]
        if selector in {entry["id"], Path(entry["path"]).name, entry["path"]}
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected one lesson for '{selector}', found {len(matches)}")
    return matches[0]


def append_update(
    lesson_path: Path,
    status: str,
    evidence: str | None,
    next_review: str | None,
    independent_level: str | None,
) -> None:
    text = lesson_path.read_text(encoding="utf-8")
    details = [f"Status: {html.escape(status)}"]
    if evidence:
        details.append(f"Evidence: {html.escape(evidence)}")
    if next_review:
        details.append(f"Next review: {html.escape(next_review)}")
    if independent_level:
        details.append(f"Independent level: {html.escape(independent_level)}")
    section = "\n  <section>\n    <h2>Session Update</h2>\n    <ul>\n"
    section += "\n".join(f"      <li>{detail}</li>" for detail in details)
    section += "\n    </ul>\n  </section>\n"
    if "</body>" not in text:
        raise ValueError(f"Lesson does not contain </body>: {lesson_path}")
    lesson_path.write_text(text.replace("</body>", section + "</body>", 1), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, help="Learning workspace root")
    parser.add_argument("--lesson", required=True, help="Lesson id, filename, or relative path")
    parser.add_argument(
        "--status", choices=["prepared", "in-progress", "complete"], required=True
    )
    parser.add_argument("--evidence", help="User-provided learning evidence")
    parser.add_argument("--next-review", help="One next review task")
    parser.add_argument(
        "--independent-level",
        choices=["unassessed", "0", "1", "2", "3"],
        help="Evidence-based learner ability after this session",
    )
    args = parser.parse_args()
    if args.status == "complete" and not args.evidence:
        parser.error("--evidence is required when --status is complete")
    return args


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    index = load_index(workspace)
    entry = resolve_entry(index, args.lesson)
    lesson_path = (workspace / entry["path"]).resolve()
    lessons_dir = (workspace / "lessons").resolve()
    if lessons_dir not in lesson_path.parents or not lesson_path.exists():
        raise ValueError(f"Invalid lesson path: {lesson_path}")
    append_update(
        lesson_path, args.status, args.evidence, args.next_review, args.independent_level
    )
    entry["status"] = args.status
    entry["updated_at"] = now()
    if args.evidence:
        entry["last_evidence"] = args.evidence
    if args.next_review:
        entry["next_review"] = args.next_review
    if args.independent_level:
        entry["independent_level"] = args.independent_level
    save_index(workspace, index)
    print(lesson_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
