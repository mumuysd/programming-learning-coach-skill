#!/usr/bin/env python3
"""Create a lesson index for existing lesson HTML files without changing them."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from create_lesson import now, save_index


def topic_from_html(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"<h1>(.*?)</h1>", text, flags=re.DOTALL)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return path.stem.split("-", 1)[-1].replace("-", " ")


def entry_from_path(workspace: Path, path: Path, current: str | None) -> dict:
    match = re.match(r"^(\d{4})-(.+)\.html$", path.name)
    if not match:
        raise ValueError(f"Unexpected lesson name: {path.name}")
    lesson_id, slug = match.groups()
    return {
        "id": lesson_id,
        "topic": topic_from_html(path),
        "slug": slug,
        "path": str(path.relative_to(workspace)),
        "status": "prepared" if lesson_id == current else "unknown",
        "prepared_at": None,
        "updated_at": now(),
        "last_evidence": None,
        "next_review": None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, help="Learning workspace root")
    parser.add_argument("--current", help="Optional prepared lesson id, such as 0016")
    parser.add_argument("--force", action="store_true", help="Replace an existing lesson index")
    args = parser.parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    lessons_dir = workspace / "lessons"
    index_path = workspace / "lesson-index.json"
    if index_path.exists() and not args.force:
        parser.error(f"Index already exists: {index_path}. Use --force to replace it.")
    lesson_paths = sorted(lessons_dir.glob("[0-9][0-9][0-9][0-9]-*.html"))
    if not lesson_paths:
        parser.error(f"No numbered lessons found: {lessons_dir}")
    index = {"version": 1, "lessons": [entry_from_path(workspace, path, args.current) for path in lesson_paths]}
    save_index(workspace, index)
    print(index_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
