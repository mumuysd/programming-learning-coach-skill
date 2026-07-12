# Independent Completion And Acceptance Protocol

Use this reference to assign an evidence-based ability level, control progression, and accept project work. It measures what the learner can do independently, not what Codex can generate.

## Independent-Completion Levels

| Level | Meaning | Evidence required to claim it |
| --- | --- | --- |
| `0` | Cannot begin without a full demonstration. | Needs the full path or cannot explain the task after a guided attempt. |
| `1` | Can complete with prompts, questions, or local examples. | Can make a supported attempt, run it, and explain the basic IPO. |
| `2` | Can complete a familiar task from requirements and old code. | Meets every Level 1 to 2 promotion gate below. |
| `3` | Can rebuild a core feature from a blank file using only requirements. | Meets every Level 2 to 3 promotion gate below. |
| `unassessed` | Evidence is not yet sufficient to assign a level. | Start with a small diagnostic, never guess upward. |

## Promotion Gates

Promote `1` to `2` only when the learner has shown all of these:

- completed without line-by-line prompting,
- split the work into 3-5 useful steps,
- wrote the core logic,
- fixed at least one real error,
- completed a basic test or representative run,
- explained Input / Process / Output.

Promote `2` to `3` only when the learner has shown all of these:

- started the core feature from a blank file,
- used requirements rather than copying the old implementation,
- wrote pseudocode or consulted official documentation when stuck,
- completed the core feature,
- handled the key abnormal case,
- wrote run instructions and a test note,
- explained the Input / Process / Output and main design choices.

Do not promote on a single good answer, an agent-side run, copied code, or a claim of understanding.

## Recovery Rules

Apply these rules before assigning new project work:

- No user-run evidence in the prior session: assign only the smallest review or recovery task.
- Two failed attempts at the same core point: stop feature progression and assign 2-3 drills one level lower on the exercise ladder.
- Current feature cannot run reliably: repair and test it before adding a new feature.
- Learner cannot explain a key variable, execution order, or IPO: keep the current ability level and use a smaller diagnostic.

## Session Contract

Every formal session must state:

```text
Current independent level: {0 / 1 / 2 / 3 / unassessed}
Today's theme: {one small ability}
Time box: {realistic duration}
Must complete: {one observable result}
Minimum runnable version: {smallest acceptable result}
Not today: {explicit boundary}
Think first: {one key question}
Submit before advancement: {run result + output/error + IPO explanation}
```

## Focused Code Check

After a focused task, use this exact decision shape:

```text
Can run: {yes/no + evidence}
Result correct: {yes/no/partly}
Learner can explain: {yes/no + gap}
Tests sufficient: {yes/no + missing case}
Independent level: {current level and support needed}
Meets today's floor: {yes/no}
Current gap: {one most important gap}
Only next task: {one recovery or advancement task}
```

## Project Milestone Acceptance

Do not call a project milestone stable merely because one run works. Require:

- a runnable minimum version,
- at least three representative cases, including a relevant abnormal case,
- clear names and single-purpose functions or sections,
- no unnecessary complexity in the current scope,
- a short README or run instruction,
- learner explanation of Input / Process / Output,
- user evidence that separates learner-written work from Codex-written work.

Use the lightest check that fits the milestone. Do not turn a small daily lesson into a release process.
