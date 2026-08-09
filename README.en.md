<sub>🌐 <a href="README.md">中文</a> · <b>English</b></sub>

# Programming Learning Coach

An evidence-based programming learning Skill for Python, automation, web development, debugging, and project practice. It does not default to a finished patch. It prepares a lesson, teaches one concrete idea, and asks the learner to predict, run, inspect, and explain.

Its purpose is to build durable programming ability, not to treat one successful run as proof of learning.

## What It Does

```text
trusted source or local artifact
→ no-answer lesson
→ concrete teaching block
→ prediction
→ learner-run evidence
→ Input / Process / Output explanation
→ evidence-based record and review
```

| Situation | Behavior |
| --- | --- |
| New concept | Teach explanations, a decision rule, contrasting cases, and the mechanism before practice. |
| Technical library/API | Prefer a registered official source in `RESOURCES.md`; register a suitable source before relying on factual behavior. |
| Continuing lesson | Compare the lesson with existing evidence and continue only the remaining gap. |
| Debugging | Read the error, locate it, inspect a value, minimize when useful, change one thing, and rerun. |
| Repeated error | Keep the first two occurrences in review; create a reusable reference after a third matching root cause. |

A `new-knowledge` lesson cannot be a definition plus an exercise checklist. It needs at least two substantive explanations, one decision rule, two contrast cases, and a two-step runtime or reasoning mechanism. Teaching examples differ from exercise inputs and the lesson never reveals the finished task code, answer key, or exact final output.

## Install

```bash
npx skills add mumuysd/programming-learning-coach-skill --skill programming-learning-coach
```

Or install locally for Codex:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/mumuysd/programming-learning-coach-skill.git ~/.codex/skills/programming-learning-coach
cd ~/.codex/skills/programming-learning-coach
cp WORKSPACE.example.md WORKSPACE.md
```

Set `workspace_root` in `WORKSPACE.md` to your learning workspace. This local configuration is ignored by Git.

## Example Prompts

```text
Use $programming-learning-coach to teach me the difference between direct dictionary lookup and get. Create the lesson first and do not give the final code yet.
```

```text
Use $programming-learning-coach to help me learn FastAPI path, query, and request-body inputs from official documentation.
```

```text
My pandas code raised KeyError. Use $programming-learning-coach to help me debug it as a learning exercise, without a full fix first.
```

The first teaching reply for a formal session reports the actual lesson path:

```text
学习资料已生成：/absolute/path/to/lessons/0001-topic.html
```

## Workspace

The Skill creates only what the current session needs:

```text
learning-workspace/
├── RESOURCES.md
├── lessons/
├── lesson-index.json
├── learning-records/
├── review-queue/
└── reference/
```

## Boundaries

- This is a learning workflow, not a default production-delivery workflow.
- Agent-side execution is never learner evidence.
- Practice, review, and transfer must not be presented as new knowledge.
- The Skill does not provide investment/trading advice or public-post drafting.

## Validate

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
python3 scripts/run_lesson_regression.py
```

With an authenticated Codex CLI session:

```bash
python3 scripts/run_preflight_regression.py --timeout-seconds 420
```

## License

[MIT License](LICENSE)
