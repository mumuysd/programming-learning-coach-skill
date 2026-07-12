# Lesson And Reference Protocol

Use this reference before creating or updating `lessons/` or `reference/` artifacts in the learning workspace.

## Core Rule

A lesson file must be created or updated at the start of every formal learning, review, or learning-oriented debugging session. Create it before the first teaching question, code change, debugging check, or exercise. A promise to create a lesson, or lesson text only in chat, does not satisfy the rule. Verify the file exists and report its absolute path in the first user-visible teaching response. It must be a no-answer learning map: show what the user will use, what to notice, and what to try, but do not reveal the final solution before the user has predicted, attempted, run, inspected, and explained.

## Start-Of-Lesson Requirement

Create or update a lesson at the start for:

- a new or continuing programming lesson,
- a review session,
- debugging used as a learning exercise,
- a new concept or function will be introduced,
- a durable project-learning task.

Do not create a lesson for a tiny non-learning clarification, public-content request, or direct production-code delivery. If a user starts a formal session but the workspace cannot be written, request permission and pause the teaching flow. Do not silently substitute an unsaved chat lesson.

## Lesson Naming

Save lessons in the learning workspace:

```text
lessons/0001-<dash-case-topic>.html
```

When continuing an existing topic, update its current lesson file. When starting a new topic, scan existing lesson numbers and increment the highest number. Use short dash-case names such as:

- `0001-read-csv-columns.html`
- `0002-debug-keyerror-status.html`
- `0003-loop-through-task-rows.html`

For a new topic, use `scripts/create_lesson.py` to make the numbered file and its `lesson-index.json` entry. The script prints its absolute path; verify that path before teaching. For a continuing topic, use `scripts/update_lesson.py --status in-progress` before the first teaching question. Use `--status complete --evidence ...` only after the user completion evidence is present.

## Start-Of-Lesson Content

At session start, every lesson must include:

- lesson goal,
- session contract: independent level, time box, minimum runnable version, out-of-scope boundary, and required evidence,
- concepts used today,
- functions or methods used today,
- input / process / output target,
- prediction question,
- exercise steps,
- blank slots for the user's observations.

Add these when useful:

- why this matters for the active project,
- prerequisite concepts,
- starter checklist,
- links or names of trusted resources to consult.

At session start, a lesson must not include:

- finished code for the target task,
- answer key,
- exact final output,
- final explanation of why the solution works,
- completed Input / Process / Output wording,
- a polished learning record.

## Minimal Lesson Template

Use simple HTML so the lesson can be opened directly.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{Lesson number}: {Topic}</title>
</head>
<body>
  <h1>{Topic}</h1>
  <section>
    <h2>Goal</h2>
    <p>{One small observable skill.}</p>
  </section>
  <section>
    <h2>Session Contract</h2>
    <ul>
      <li>Independent level: {0 / 1 / 2 / 3 / unassessed}</li>
      <li>Time box: {realistic duration}</li>
      <li>Minimum runnable version: {smallest acceptable result}</li>
      <li>Not today: {explicit boundary}</li>
      <li>Submit before advancement: {run result + output/error + IPO explanation}</li>
    </ul>
  </section>
  <section>
    <h2>Concepts And Functions</h2>
    <ul>
      <li><code>{function_or_concept}</code>: {plain meaning, not the answer}</li>
    </ul>
  </section>
  <section>
    <h2>Input / Process / Output Target</h2>
    <ul>
      <li>Input: {what data or file the user starts from}</li>
      <li>Process: {what kind of operation they will try}</li>
      <li>Output: {what kind of result to look for, not the exact final answer}</li>
    </ul>
  </section>
  <section>
    <h2>Before You Run</h2>
    <p>{Prediction question.}</p>
  </section>
  <section>
    <h2>Exercise Steps</h2>
    <ol>
      <li>{Small step}</li>
      <li>{Small step}</li>
      <li>Run locally and write what happened.</li>
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
```

Keep styling minimal unless the user asks for a polished visual lesson. Do not spend session time on decoration when the learning task is the priority.

## Updating A Lesson After Evidence

After completion evidence is sufficient, append or update:

- what the user predicted,
- what actually happened,
- the user's Input / Process / Output explanation,
- the misconception or debugging step,
- one next review task.

Do not rewrite the lesson into a full answer dump. Keep it useful for future review.

## Reference Notes

Create references only for durable, reusable knowledge. They are compact review artifacts, not tutorials or answer dumps. Use one of these two types.

### Concept References

Create a concept reference after sufficient completion evidence when a function, concept, or pattern will recur in project work. Save it in:

```text
reference/<dash-case-concept>.md
```

Use this structure:

```md
# {Concept}

## Use when
{When this concept appears in project work.}

## Plain meaning
{Short explanation.}

## Common pattern
{Small reusable pattern or pseudocode. Avoid solving the current task outright.}

## Common mistake
{Mistake to watch for.}

## Review prompt
{One tiny question or exercise.}
```

### Error-Pattern References

Create an error-pattern reference only after the same error type has appeared three cumulative times. A same-type error must share all three of these:

- the same language or library area,
- the same error class or symptom,
- the same underlying root cause.

For example, three pandas `KeyError` cases caused by selecting a column that is absent from the DataFrame count as one error pattern. A `KeyError` caused by a misspelled dictionary key does not count toward that same pattern.

For the first and second occurrence, update a matching `review-queue/` item or practice record. Do not create a `reference/` note yet. On the third occurrence, confirm the pattern and promote it to:

```text
reference/<dash-case-error-pattern>.md
```

Use this structure:

```md
# Error Pattern: {short name}

## Trigger
{What the user was trying to do when it appeared.}

## Root cause
{The shared cause across the three occurrences.}

## Debug checks
{One check at a time: error type, failing line, relevant variable, minimal reproduction.}

## Common mistake
{The action that tends to recreate the issue.}

## Review prompt
{One tiny diagnostic exercise.}
```

If the user explicitly requests an error reference before the third occurrence, explain the three-occurrence default and offer a temporary review-queue note instead.

## Boundary

If the user explicitly asks for full code or final answers, provide them only after acknowledging that this switches out of the default coaching flow.
