#!/usr/bin/env python3
"""Create a numbered, no-answer lesson and register it in lesson-index.json."""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import UTC, datetime
from pathlib import Path

INDEX_FILE_NAME = "lesson-index.json"
LESSON_TYPES = ("new-knowledge", "practice", "review", "transfer")
LANGUAGES = {
    "en": {
        "goal": "Goal", "contract": "Session Contract", "teaching": "New Knowledge",
        "explanations": "Core Explanations", "rule": "Decision Rule", "contrast": "Contrasting Cases",
        "mechanism": "How It Works", "sources": "Primary Source", "concepts": "Concepts And Functions",
        "ipo": "Input / Process / Output Target", "predict": "Before You Run", "steps": "Exercise Steps",
        "notes": "Your Notes", "boundary": "Teaching cases explain the idea. Apply the rule to the exercise inputs; do not copy a conclusion.",
    },
    "zh": {
        "goal": "本课目标", "contract": "本课约定", "teaching": "新知识讲解",
        "explanations": "核心解释", "rule": "判断规则", "contrast": "对照案例",
        "mechanism": "处理机制", "sources": "主要资料", "concepts": "本课概念与函数",
        "ipo": "Input / Process / Output 目标", "predict": "运行前预测", "steps": "练习步骤",
        "notes": "学习者记录", "boundary": "上面的案例只用于讲解。请把规则迁移到练习输入，不要照抄案例结论。",
    },
}


def now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def escaped(value: str) -> str:
    return html.escape(value, quote=True)


def item_list(items: list[str], indent: str = "      ") -> str:
    return "\n".join(f"{indent}<li>{escaped(item)}</li>" for item in items)


def source_list(items: list[str]) -> str:
    rendered: list[str] = []
    for item in items:
        parts = [part.strip() for part in item.split("|") if part.strip()]
        url = next((part for part in parts if re.fullmatch(r"https?://\S+", part)), None)
        if not url:
            rendered.append(f"      <li>{escaped(item)}</li>")
            continue
        title = next((part for part in parts if part != url), url)
        detail = [part for part in parts if part not in {title, url}]
        suffix = f"：{escaped('；'.join(detail))}" if detail else ""
        rendered.append(f'      <li><a href="{escaped(url)}">{escaped(title)}</a>{suffix}</li>')
    return "\n".join(rendered)


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
    index_path(workspace).write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def next_lesson_number(lessons_dir: Path) -> int:
    numbers = [int(match.group(1)) for path in lessons_dir.glob("*.html") if (match := re.match(r"^(\d{4})-", path.name))]
    return max(numbers, default=0) + 1


def normalized(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def validate_content_value(workspace: Path, args: argparse.Namespace) -> None:
    if args.lesson_type != "new-knowledge":
        if any((args.knowledge_delta, args.explanation, args.decision_rule, args.contrast_case, args.mechanism_step)):
            raise ValueError("Only new-knowledge lessons may include a teaching block.")
        return
    gaps = []
    if not args.knowledge_delta:
        gaps.append("--knowledge-delta")
    if len(args.explanation) < 2:
        gaps.append("at least two --explanation values")
    if not args.decision_rule:
        gaps.append("--decision-rule")
    if len(args.contrast_case) < 2:
        gaps.append("at least two --contrast-case values")
    if len(args.mechanism_step) < 2:
        gaps.append("at least two --mechanism-step values")
    if gaps:
        raise ValueError("new-knowledge lessons require substantive teaching content: " + ", ".join(gaps))
    duplicate = next((entry for entry in load_index(workspace)["lessons"] if entry.get("status") == "complete" and normalized(entry.get("knowledge_delta")) == normalized(args.knowledge_delta)), None)
    if duplicate:
        raise ValueError(f"knowledge_delta already completed in {duplicate['path']}; create practice, review, or transfer instead.")


def teaching_section(args: argparse.Namespace, labels: dict[str, str]) -> str:
    if args.lesson_type != "new-knowledge":
        return ""
    return f"""  <section class=\"teaching\">
    <h2>{labels['teaching']}</h2>
    <h3>{labels['explanations']}</h3>
    <ul>
{item_list(args.explanation)}
    </ul>
    <h3>{labels['rule']}</h3>
    <p>{escaped(args.decision_rule)}</p>
    <h3>{labels['contrast']}</h3>
    <ul>
{item_list(args.contrast_case)}
    </ul>
    <h3>{labels['mechanism']}</h3>
    <ol>
{item_list(args.mechanism_step)}
    </ol>
    <p><strong>{escaped(labels['boundary'])}</strong></p>
  </section>
"""


def render_lesson(args: argparse.Namespace, lesson_number: int) -> str:
    labels = LANGUAGES[args.language]
    concepts = args.concept + args.function
    steps = args.step + ["Run locally and record what happened." if args.language == "en" else "亲自运行，并记录实际发生了什么。"]
    out_of_scope = args.not_today or ["Do not add unrelated features." if args.language == "en" else "不添加无关功能。"]
    required_evidence = args.required_evidence or ["A local run result." if args.language == "en" else "一次本地运行结果。", "An Input / Process / Output explanation." if args.language == "en" else "自己的 Input / Process / Output 解释。"]
    title = f"{lesson_number:04d}: {args.topic}"
    sources = f"""  <section>
    <h2>{labels['sources']}</h2>
    <ul>
{source_list(args.source)}
    </ul>
  </section>
""" if args.source else ""
    return f"""<!doctype html>
<html lang=\"{args.language}\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{escaped(title)}</title>
  <style>body{{font-family:system-ui,sans-serif;line-height:1.6;max-width:860px;margin:2rem auto;padding:0 1rem}}section{{border-top:1px solid #ddd;padding:1rem 0}}.teaching{{background:#f5f8ff;padding:1rem;border:1px solid #cbd8f6}}code{{background:#f0f0f0;padding:.1rem .25rem}}</style>
</head>
<body>
  <h1>{escaped(args.topic)}</h1>
  <section><h2>{labels['goal']}</h2><p>{escaped(args.goal)}</p><p><strong>Lesson type:</strong> {escaped(args.lesson_type)}<br><strong>Why now:</strong> {escaped(args.why_now)}</p></section>
  <section><h2>{labels['contract']}</h2><ul>
    <li>Independent level: {escaped(args.independent_level)}</li>
    <li>Support level: {escaped(args.support_level)}</li>
    <li>Time box: {escaped(args.time_box)}</li>
    <li>Minimum runnable version: {escaped(args.minimum_version)}</li>
    <li>Not today:<ul>
{item_list(out_of_scope, '        ')}
    </ul></li>
    <li>Submit before advancement:<ul>
{item_list(required_evidence, '        ')}
    </ul></li>
  </ul></section>
{sources}{teaching_section(args, labels)}  <section><h2>{labels['concepts']}</h2><ul>
{item_list(concepts)}
  </ul></section>
  <section><h2>{labels['ipo']}</h2><ul><li>Input: {escaped(args.input)}</li><li>Process: {escaped(args.process)}</li><li>Output: {escaped(args.output)}</li></ul></section>
  <section><h2>{labels['predict']}</h2><p>{escaped(args.prediction)}</p></section>
  <section><h2>{labels['steps']}</h2><ol>
{item_list(steps)}
  </ol></section>
  <section><h2>{labels['notes']}</h2><p>Prediction:</p><p>Actual output:</p><p>Input / Process / Output:</p></section>
</body>
</html>
"""


def register_lesson(workspace: Path, lesson_path: Path, args: argparse.Namespace) -> None:
    index = load_index(workspace)
    index["lessons"].append({
        "id": lesson_path.name.split("-", 1)[0], "topic": args.topic, "slug": args.slug,
        "path": str(lesson_path.relative_to(workspace)), "status": "prepared",
        "prepared_at": now(), "updated_at": now(), "last_evidence": None, "next_review": None,
        "lesson_type": args.lesson_type, "knowledge_delta": args.knowledge_delta,
        "why_now": args.why_now, "independent_level": args.independent_level,
        "support_level": args.support_level, "minimum_version": args.minimum_version,
        "teaching_content": {"explanations": args.explanation, "decision_rules": [args.decision_rule] if args.decision_rule else [], "contrast_cases": args.contrast_case, "mechanism_steps": args.mechanism_step},
    })
    save_index(workspace, index)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--lesson-type", choices=LESSON_TYPES, required=True)
    parser.add_argument("--why-now", required=True)
    parser.add_argument("--knowledge-delta")
    parser.add_argument("--concept", action="append", required=True)
    parser.add_argument("--function", action="append", default=[])
    parser.add_argument("--source", action="append", default=[], help="Title | URL | use")
    parser.add_argument("--explanation", action="append", default=[])
    parser.add_argument("--decision-rule")
    parser.add_argument("--contrast-case", action="append", default=[])
    parser.add_argument("--mechanism-step", action="append", default=[])
    parser.add_argument("--input", required=True)
    parser.add_argument("--process", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--prediction", required=True)
    parser.add_argument("--step", action="append", required=True)
    parser.add_argument("--independent-level", choices=["unassessed", "0", "1", "2", "3"], default="unassessed")
    parser.add_argument("--support-level", choices=["unassessed", "step-by-step", "light-guidance", "independent"], default="unassessed")
    parser.add_argument("--time-box", default="30 minutes")
    parser.add_argument("--minimum-version", default="Define the smallest runnable version before coding.")
    parser.add_argument("--not-today", action="append", default=[])
    parser.add_argument("--required-evidence", action="append", default=[])
    parser.add_argument("--language", choices=sorted(LANGUAGES), default="en")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        parser.error("--slug must use lowercase letters, digits, and hyphens")
    return args


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    validate_content_value(workspace, args)
    lessons_dir = workspace / "lessons"
    lessons_dir.mkdir(exist_ok=True)
    number = next_lesson_number(lessons_dir)
    lesson_path = lessons_dir / f"{number:04d}-{args.slug}.html"
    lesson_path.write_text(render_lesson(args, number), encoding="utf-8")
    register_lesson(workspace, lesson_path, args)
    print(lesson_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
