<div align="center">

# Programming Learning Coach

> *"Stop collecting answers. Start proving you can read, run, debug, and explain code."*

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-programming--learning--coach-blueviolet)](SKILL.md)
[![Local Skill](https://img.shields.io/badge/Install-local%20Codex%20skill-informational)](#quick-start)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**A programming-learning Skill that creates a no-answer lesson map before every formal learning session, then trains prediction, user-run evidence, debugging, review, and Input / Process / Output explanation before marking progress complete.**

[See Examples](#examples) . [Quick Start](#quick-start) . [Trigger Phrases](#trigger-phrases) . [Safety](#safety-boundaries) . [Validation](#validation)

</div>

---

## What Problem It Solves

Most coding assistants can fix the code faster than a beginner can learn from it. That is useful for shipping, but it can quietly erase the learning loop.

This Skill is for sessions where the goal is not "give me the answer." The goal is to build programming ability: read code, predict behavior, run locally, inspect output, explain Input / Process / Output, and only then update the learning record.

It is especially useful for Python automation learning, pandas/CSV/reporting projects, debugging practice, and short project-English recap. The workspace, plan, and project are configurable for each learner.

Before every formal learning, review, or learning-oriented debugging session, it creates or updates a lesson file and reports its absolute path before teaching. That lesson is a map rather than an answer sheet: concepts, functions, input/output targets, prediction questions, and exercise steps are allowed; final code and final answers are not.

References are deliberately selective: reusable concepts can be captured after real learning evidence, while a recurring error is first tracked in the review queue and becomes an error-pattern reference only after it appears three times with the same area, symptom, and root cause.

---

## Examples

- [Start-of-lesson map](examples/start-lesson-map.md)
- [Normal learning session](examples/normal-session.md)
- [Debugging learning session](examples/debugging-session.md)
- [Result card template](examples/result-card-template.md)

Sample result card:

```text
Programming Learning Card
Ability: Debugging
Evidence: user predicted the failure, ran locally, inspected the traceback, and explained Input / Process / Output.
Next review: recreate the same fix without looking at the old code.
```

---

## Quick Start

Current local install target:

```text
~/.codex/skills/programming-learning-coach
```

Configure a local workspace once:

```text
cp WORKSPACE.example.md WORKSPACE.md
```

Set `workspace_root` in `WORKSPACE.md` to an absolute local path. This local file is intentionally excluded from version control.

First prompt after installing:

```text
Use $programming-learning-coach to continue my programming learning session based on my current progress.
```

Public installation and registry links are added only after a real source repository exists.

For other Agent Skills-compatible runtimes, copy the folder into that runtime's Skills directory, then create a local `WORKSPACE.md` from `WORKSPACE.example.md`.

---

## Trigger Phrases

- "开始今天编程学习"
- "继续 Python 自动化学习"
- "我运行报错了，带我调试"
- "今天复习一下旧概念"
- "练习 for 循环 / 函数 / 文件读写 / pandas"
- "先给我生成这节课的 lesson"
- "我懂了，检查一下我是不是真的懂"
- "更新今天的学习记录"
- "做一个项目英语复盘"
- "Start today's programming lesson"
- "Help me debug this as a learning exercise"
- "Review an old Python concept"

---

## What It Delivers

| Need | Skill behavior | Visible output |
|---|---|---|
| Continue learning | Reads state, creates or updates and verifies a lesson file, then chooses one small goal | Lesson path + lesson map + session target + first question |
| Start a lesson | Creates a no-answer lesson map | `lessons/0001-topic.html` |
| Continue a lesson | Updates lesson lifecycle state and index before teaching | `lesson-index.json` + lesson path |
| Practice coding | Uses an exercise ladder | Prediction + run + IPO explanation |
| Debug an error | Trains error reading before fixing | Debug trace + why the fix worked |
| Review concepts | Uses review queue and concept notes | Review prompt + next review target |
| Build concept reference | Captures reusable concepts after evidence | `reference/concept.md` |
| Track repeated error | Tracks the first two matching errors, promotes the third | `review-queue/pattern.md` or `reference/error-pattern.md` |
| Record progress | Updates only after evidence | Learning record or no-update reason |
| Project English | Keeps English tied to code | 1 sentence + 5 words + IPO explanation |

---

## How It Differs

| Common assistant behavior | This Skill |
|---|---|
| Gives complete code quickly | Gives hints first and full code only when explicitly requested |
| Treats "I understand" as enough | Requires explanation, prediction, or a transfer task |
| Counts agent-side runs as progress | Requires user-run evidence for learning completion |
| Fixes errors for the user | Teaches the debugging process step by step |
| Mixes learning with publishing | Keeps public-content drafting outside the learning session |

---

## Safety Boundaries

- Does not mark progress complete from Codex-side verification alone.
- Does not start a formal learning, review, or learning-oriented debugging session before creating, verifying, and reporting the path of its no-answer lesson file.
- Does not put final answers, finished target code, or exact final output into a start-of-lesson artifact.
- Does not update learning files before prediction, local run, output review, and Input / Process / Output explanation are present.
- Does not create an error-pattern reference until the same error type has appeared three times; earlier occurrences remain review work.
- Does not generate public posts or marketing copy as part of the learning session.
- Does not assume any workspace exists; resolve an explicit root or local `WORKSPACE.md` before starting a formal learning flow.
- Does not hide missing resources or thin learning evidence.

---

## File Structure

```text
programming-learning-coach/
├── SKILL.md
├── WORKSPACE.example.md
├── agents/openai.yaml
├── references/
│   ├── CODING-COACHING-PROTOCOL.md
│   ├── LESSON-REFERENCE-PROTOCOL.md
│   └── LEARNING-WORKSPACE.md
├── examples/
│   ├── debugging-session.md
│   ├── normal-session.md
│   ├── start-lesson-map.md
│   └── result-card-template.md
├── scripts/
│   ├── create_lesson.py
│   ├── rebuild_lesson_index.py
│   ├── update_lesson.py
│   └── run_preflight_regression.py
└── test-prompts.json
```

---

## Validation

Run the standard skill structure check:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/programming-learning-coach
```

Use `test-prompts.json` as the behavior suite. A passing response should:

- ask for prediction before execution,
- create, verify, and report the path of a no-answer lesson file before teaching in every formal learning session,
- avoid full code unless requested,
- require user-run evidence,
- ask for Input / Process / Output,
- keep first and second matching errors in the review queue, then promote the third to an error-pattern reference,
- keep public-post work outside this Skill.

Run the real three-scenario regression after installing the Skill and configuring Codex:

```bash
python3 scripts/run_preflight_regression.py
```

It starts isolated Codex sessions for a new lesson, a learning-oriented debug session, and a review session. Each run must produce a lesson file, a matching `lesson-index.json` entry, a path-first response, and no answer-like lesson markup.

---

## Credits

The teaching stance follows rubber-duck programming lessons: ask guiding questions, ask for predictions, give one hint at a time, review the learner's attempt, and only provide full code when explicitly requested.
