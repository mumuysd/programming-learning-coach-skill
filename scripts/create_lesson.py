#!/usr/bin/env python3
"""Create a numbered no-answer lesson file and register it in lesson-index.json."""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import UTC, datetime
from pathlib import Path

INDEX_FILE_NAME = "lesson-index.json"


def now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def escaped(value: str) -> str:
    return html.escape(value, quote=True)


def item_list(items: list[str]) -> str:
    return "\n".join(f"      <li>{escaped(item)}</li>" for item in items)


def index_path(workspace: Path) -> Path:
    return workspace / INDEX_FILE_NAME


def load_index(workspace: Path) -> dict:
    path = index_path(workspace)
    if not path.exists():
        return {"version": 1, "lessons": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("lessons"), list):
        raise ValueError(f"Unsupported lesson index: {path}")
    return data


def save_index(workspace: Path, index: dict) -> None:
    index_path(workspace).write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def next_lesson_number(lessons_dir: Path) -> int:
    highest = 0
    for lesson_path in lessons_dir.glob("*.html"):
        match = re.match(r"^(\d{4})-", lesson_path.name)
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def render_lesson(args: argparse.Namespace, lesson_number: int) -> str:
    concepts = args.concept + args.function
    steps = args.step + ["Run locally and record what happened."]
    out_of_scope = args.not_today or ["Do not add unrelated features."]
    required_evidence = args.required_evidence or [
        "A local run result.",
        "An Input / Process / Output explanation.",
    ]
    title = f"{lesson_number:04d}: {args.topic}"
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>{escaped(title)}</title>
</head>
<body>
  <h1>{escaped(args.topic)}</h1>
  <section>
    <h2>Goal</h2>
    <p>{escaped(args.goal)}</p>
  </section>
  <section>
    <h2>Session Contract</h2>
    <ul>
      <li>Independent level: {escaped(args.independent_level)}</li>
      <li>Time box: {escaped(args.time_box)}</li>
      <li>Minimum runnable version: {escaped(args.minimum_version)}</li>
      <li>Not today:
      <ul>
{item_list(out_of_scope)}
      </ul>
      </li>
      <li>Submit before advancement:
      <ul>
{item_list(required_evidence)}
      </ul>
      </li>
    </ul>
  </section>
  <section>
    <h2>Concepts And Functions</h2>
    <ul>
{item_list(concepts)}
    </ul>
  </section>
  <section>
    <h2>Input / Process / Output Target</h2>
    <ul>
      <li>Input: {escaped(args.input)}</li>
      <li>Process: {escaped(args.process)}</li>
      <li>Output: {escaped(args.output)}</li>
    </ul>
  </section>
  <section>
    <h2>Before You Run</h2>
    <p>{escaped(args.prediction)}</p>
  </section>
  <section>
    <h2>Exercise Steps</h2>
    <ol>
{item_list(steps)}
    </ol>
  </section>
  <section>
    <h2>Your Notes</h2>
    <p>Prediction:</p>
    <p>Actual output:</p>
    <p>Input / Process / Output:</p>
  </section>
</body>
</html>
"""


def register_lesson(
    workspace: Path, lesson_path: Path, topic: str, slug: str, args: argparse.Namespace
) -> None:
    index = load_index(workspace)
    lesson_id = lesson_path.name.split("-", 1)[0]
    index["lessons"].append(
        {
            "id": lesson_id,
            "topic": topic,
            "slug": slug,
            "path": str(lesson_path.relative_to(workspace)),
            "status": "prepared",
            "prepared_at": now(),
            "updated_at": now(),
            "last_evidence": None,
            "next_review": None,
            "independent_level": args.independent_level,
            "minimum_version": args.minimum_version,
        }
    )
    save_index(workspace, index)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, help="Learning workspace root")
    parser.add_argument("--topic", required=True, help="Short lesson topic")
    parser.add_argument("--slug", required=True, help="Dash-case filename suffix")
    parser.add_argument("--goal", required=True, help="One observable learning goal")
    parser.add_argument("--concept", action="append", required=True, help="Concept used today")
    parser.add_argument("--function", action="append", default=[], help="Function or method used today")
    parser.add_argument("--input", required=True, help="Input target")
    parser.add_argument("--process", required=True, help="Process target")
    parser.add_argument("--output", required=True, help="Output target")
    parser.add_argument("--prediction", required=True, help="Prediction prompt")
    parser.add_argument("--step", action="append", required=True, help="Exercise step")
    parser.add_argument(
        "--independent-level",
        choices=["unassessed", "0", "1", "2", "3"],
        default="unassessed",
        help="Evidence-based learner ability before this session",
    )
    parser.add_argument(
        "--time-box",
        default="Choose a realistic time box before coding.",
        help="Expected duration for this focused session",
    )
    parser.add_argument(
        "--minimum-version",
        default="Define the smallest runnable version before coding.",
        help="Smallest acceptable result for this session",
    )
    parser.add_argument(
        "--not-today", action="append", default=[], help="Explicitly out-of-scope work"
    )
    parser.add_argument(
        "--required-evidence",
        action="append",
        default=[],
        help="Evidence the learner must submit before advancement",
    )
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        parser.error("--slug must use lowercase letters, digits, and hyphens")
    return args


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    lessons_dir = workspace / "lessons"
    lessons_dir.mkdir(parents=True, exist_ok=True)
    lesson_number = next_lesson_number(lessons_dir)
    lesson_path = lessons_dir / f"{lesson_number:04d}-{args.slug}.html"
    lesson_path.write_text(render_lesson(args, lesson_number), encoding="utf-8")
    register_lesson(workspace, lesson_path, args.topic, args.slug, args)
    print(lesson_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
