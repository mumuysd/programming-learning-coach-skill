# Programming Learning Coach

> A no-answer programming-learning Skill for Python practice, debugging, review, and small project work.

`programming-learning-coach` is not designed to immediately write a finished solution for the learner. It helps build a repeatable learning loop: assess independent-completion ability, read code, predict behavior, run code locally, inspect output, debug, and explain Input / Process / Output.

[中文 README](README.md)

## Why This Exists

Coding assistants can solve many problems immediately. That is useful when shipping a product, but it can skip the learning loop. A learner may receive an answer without learning how to read code, locate an error, or verify understanding.

This Skill makes that loop explicit:

1. Create a no-answer lesson before formal teaching starts.
2. Ask the learner to predict behavior before running code.
3. Use learner-run output as learning evidence.
4. Teach debugging through error reading, hypothesis testing, and one change at a time.
5. Synchronize evidence-bearing session progress across the lesson, learning record, and current state.
6. Block advancement when the current feature is unstable or the learner lacks evidence for the next independent-completion level.

## Who It Is For

- Python beginners learning control flow, functions, data structures, and file I/O.
- Learners practicing automation, pandas, CSV, reporting, or small projects.
- Developers who want to debug as a learning exercise instead of receiving a complete patch.
- Anyone who wants durable review prompts, concept notes, and short project-English recap tied to real work.

## Core Behavior

| Situation | What the Skill does |
|---|---|
| Start a lesson | Creates a lesson file before teaching and reports its absolute path first. |
| Continue a lesson | Updates lesson lifecycle state and `lesson-index.json` before proceeding. |
| Practice code | Moves from reading and prediction toward small transfer exercises. |
| Debug an error | Guides error-type reading, line location, variable inspection, minimal reproduction, and one change at a time. |
| Review a concept | Selects a weak concept or review-queue item, then asks for fresh evidence. |
| Repeat an error | Tracks the first two occurrences; creates an error reference only after a third matching error. |
| Assess independence | Records Levels 0-3 only from learner-owned evidence and promotion gates. |
| Close a session | Synchronizes the lesson, record, current state, and an optional checkpoint-linked learning plan. |

## Install

### Codex

Clone the repository, then copy the Skill folder into the Codex Skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/mumuysd/programming-learning-coach-skill.git ~/.codex/skills/programming-learning-coach
cd ~/.codex/skills/programming-learning-coach
cp WORKSPACE.example.md WORKSPACE.md
```

Set `workspace_root` in `WORKSPACE.md` to an absolute local path for the learner's materials. `WORKSPACE.md` is private local configuration and is ignored by Git; do not commit it.

For another Agent Skills-compatible runtime, copy this folder into that runtime's Skills directory and create `WORKSPACE.md` from the included template.

## How It Works

### 1. Lesson preflight

Before a formal lesson, review, or learning-oriented debugging session, the Skill creates or updates a no-answer lesson in `lessons/`. Its first teaching response must begin with:

```text
学习资料已生成：/absolute/path/to/lessons/0001-topic.html
```

The lesson map may contain goals, relevant concepts or functions, Input / Process / Output targets, prediction questions, and exercise steps. It must not contain final answers, finished target code, or exact final output.

### 2. Evidence-based coaching

The Skill advances one small concept at a time. It asks a question or gives one hint, then waits for the learner to predict, try, run, inspect, and explain.

Every formal session also states the learner's current independent-completion level, a time box, minimum runnable version, out-of-scope boundary, and required evidence. A project milestone needs stable representative cases before a new feature is added.

When the learner says "I understand," the next step is an explanation, prediction, or small transfer exercise rather than immediate advancement.

### 3. Learning records and review

A configured learning workspace can gradually contain:

```text
learning-workspace/
├── CURRENT_LEARNING_STATE.md
├── lessons/
├── lesson-index.json
├── learning-records/
├── concept-notes/
├── practice-records/
├── review-queue/
└── reference/
```

The workspace can start small. Create only the files and directories needed for the learner's current stage. Evidence-bearing sessions are closed with one synchronized operation; partial progress remains `in-progress`, while full evidence may complete the lesson or advance an optional plan checkpoint.

## Example Prompts

```text
Start today's programming lesson. I want to practice Python dictionaries.
```

```text
Help me debug this pandas KeyError as a learning exercise. Do not give me the full fix first.
```

```text
Review Python functions and return values with me.
```

## Included Files

| Path | Purpose |
|---|---|
| `SKILL.md` | Core coaching, lesson-preflight, and debugging instructions. |
| `WORKSPACE.example.md` | Private workspace configuration template. |
| `references/` | Coaching protocol, workspace structure, and lesson/reference rules. |
| `scripts/create_lesson.py` | Creates a no-answer HTML lesson and index entry. |
| `scripts/update_lesson.py` | Records a lesson's lifecycle progress. |
| `scripts/finalize_session.py` | Synchronizes session evidence across progress artifacts. |
| `scripts/rebuild_lesson_index.py` | Builds an index for existing lesson files. |
| `scripts/run_preflight_regression.py` | Runs isolated Agent regression scenarios. |
| `scripts/run_session_finalize_regression.py` | Tests partial progress, completion advancement, and evidence guards. |
| `examples/` | Expected lesson and coaching examples. |
| `test-prompts.json` | Behavior expectations for manual evaluation. |

## Boundaries

- This is a learning coach, not a production-code delivery workflow.
- Agent-side code execution is not evidence that the learner has completed a lesson.
- A real lesson file must exist before formal teaching; a chat-only lesson does not satisfy the rule.
- Start-of-lesson artifacts do not contain finished code, final answers, or exact target output.
- Public-post and marketing-copy work are outside the learning session.
- Complete code is provided only when the learner explicitly requests it.

## Validate

Validate the Skill structure:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/programming-learning-coach
```

In an environment with authenticated, non-interactive Codex CLI access, run the three-scenario regression:

```bash
cd ~/.codex/skills/programming-learning-coach
python3 scripts/run_preflight_regression.py
python3 scripts/run_session_finalize_regression.py
```

The preflight regression creates temporary workspaces for a new lesson, learning-oriented debugging, and review. The session-finalization regression verifies synchronized progress records, optional learning-plan advancement, and rejection of unsupported completion claims.

## Contributing

Issues and pull requests are welcome. Keep changes focused on learning behavior, preserve the no-answer lesson rule, and add or update evaluation coverage when behavior changes.

## License

Released under the [MIT License](LICENSE).
