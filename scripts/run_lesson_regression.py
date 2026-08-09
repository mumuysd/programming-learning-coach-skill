#!/usr/bin/env python3
"""Check the public lesson generator's no-answer and teaching-content contracts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CREATE = ROOT / "scripts" / "create_lesson.py"


def command(workspace: Path) -> list[str]:
    return [
        sys.executable, str(CREATE), "--workspace", str(workspace),
        "--topic", "Dictionary lookup decisions", "--slug", "dictionary-lookup-decisions",
        "--goal", "Choose direct indexing or get based on whether a missing key is expected.",
        "--lesson-type", "new-knowledge", "--why-now", "Dictionary lookups are needed in the current parser task.",
        "--knowledge-delta", "Choose lookup behavior from missing-key semantics.",
        "--concept", "dictionary key lookup", "--function", "dict.get",
        "--source", "Python dict documentation | https://docs.python.org/3/library/stdtypes.html#dict | verify lookup behavior",
        "--explanation", "Direct indexing signals that a missing key is exceptional and should be visible.",
        "--explanation", "get returns a fallback when absence is an expected branch of the input.",
        "--decision-rule", "Use direct indexing for required data; use get with an explicit fallback for optional data.",
        "--contrast-case", "A required user id missing from a validated record should surface as an error.",
        "--contrast-case", "An optional display label missing from imported data can use a documented default.",
        "--mechanism-step", "The program evaluates the lookup expression against the dictionary.",
        "--mechanism-step", "The chosen lookup behavior returns a value or makes the missing-key case visible before later logic runs.",
        "--input", "One dictionary with required and optional fields.",
        "--process", "Choose and test one lookup behavior for each field.",
        "--output", "Observed value or visible missing-key behavior.",
        "--prediction", "Which lookup should expose a missing key, and which should use a fallback?",
        "--step", "Classify two exercise fields as required or optional.",
        "--step", "Write one small lookup experiment without copying the teaching cases.",
        "--language", "en",
    ]


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="programming-learning-coach-") as temp_dir:
        workspace = Path(temp_dir)
        created = subprocess.run(command(workspace), text=True, capture_output=True, check=False)
        if created.returncode:
            raise AssertionError(created.stderr)
        lesson_path = Path(created.stdout.strip())
        html = lesson_path.read_text(encoding="utf-8")
        for marker in ("<h2>New Knowledge</h2>", "<h3>Core Explanations</h3>", "<h3>Decision Rule</h3>", "<h3>Contrasting Cases</h3>", "<h3>How It Works</h3>"):
            if marker not in html:
                raise AssertionError(f"missing teaching marker: {marker}")
        if any(marker in html for marker in ("<pre>", "Answer Key", "Final Answer")):
            raise AssertionError("lesson leaked answer-like markup")
        entry = json.loads((workspace / "lesson-index.json").read_text(encoding="utf-8"))["lessons"][0]
        if entry["lesson_type"] != "new-knowledge" or len(entry["teaching_content"]["explanations"]) < 2:
            raise AssertionError("index did not retain teaching metadata")
        thin = command(workspace)
        for flag in ("--explanation", "--decision-rule", "--contrast-case", "--mechanism-step"):
            while flag in thin:
                index = thin.index(flag)
                del thin[index:index + 2]
        thin[thin.index("--slug") + 1] = "thin-lesson"
        rejected = subprocess.run(thin, text=True, capture_output=True, check=False)
        if rejected.returncode == 0 or "substantive teaching content" not in rejected.stderr:
            raise AssertionError("thin new-knowledge lesson was not rejected")
    print("PASS: public lesson generator enforces substantive, no-answer teaching material")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
