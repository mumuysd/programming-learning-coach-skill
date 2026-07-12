# Learning Workspace

Use this reference when reading or updating the programming learning workspace. Keep records short and evidence-based.

## Workspace Root

Resolve the workspace from an explicit user path first, then from `WORKSPACE.md` beside the installed Skill. `WORKSPACE.example.md` is the publishable template; `WORKSPACE.md` is local configuration and must not be committed.

Treat `CURRENT_LEARNING_STATE.md` as the source of truth for the next session. Treat the annual plan as a roadmap, not a calendar that overrides evidence.

When available, keep these fields short and current:

```md
## Independent completion
Level: {unassessed / 0 / 1 / 2 / 3}
Last support needed: {none, one hint, guided questions, or full demonstration}

## Stability and recovery
Current feature stable: {yes/no + minimum cases run}
Blocked core point: {concept or none}
Consecutive failed attempts: {0, 1, or 2}
Pending evidence: {what the learner still must run or explain}
```

## Recommended Structure

- `MISSION.md`: Why the user is learning programming and what observable success looks like.
- `RESOURCES.md`: Trusted resources for Python, pandas, automation, debugging, and project work.
- `CURRENT_LEARNING_STATE.md`: Current stage, active project, independent-completion level, next task, weak concepts, blocked attempts, feature stability, and pending evidence.
- `NOTES.md`: User preferences, pacing, recurring friction, and teaching notes.
- `lesson-index.json`: Lesson id, topic, path, lifecycle status, latest evidence, and next review.
- `lessons/*.html`: No-answer lesson maps created at the start of a lesson and updated after evidence appears.
- `reference/*.md`: Compact durable notes for recurring concepts and confirmed error patterns.
- `learning-records/*.md`: Daily or session records based on demonstrated learning.
- `concept-notes/*.md`: Short durable notes for concepts that should be reviewed later.
- `practice-records/*.md`: Exercises attempted, errors encountered, and transfer tasks.
- `review-queue/*.md`: Concepts, tasks, and repeated error patterns that need spaced review before promotion to a reference.

Create missing folders only when the session needs them. Do not create extra README, changelog, or installation files.

## Mission

If `MISSION.md` is missing or stale, ask before changing it. Keep it short:

```md
# Mission: Programming Learning

## Why
{Concrete reason for learning programming.}

## Success looks like
- {Observable coding ability or project outcome}

## Constraints
- {Time, energy, tools, preferred coaching style}

## Out of scope
- {Topics to avoid for now}
```

## Resources

Use `RESOURCES.md` to keep high-trust sources. Prefer official documentation when explaining library behavior.

```md
# Programming Resources

## Knowledge

- [Resource title](https://example.com)
  Covers: {topic}. Use for: {when to consult it}.

## Wisdom

- [Community or course](https://example.com)
  Use for: {feedback or examples}.
```

If resources are thin, surface that gap instead of pretending the workspace is well grounded.

## Lessons

Create or update a `lessons/` file before the first teaching question, code change, debugging check, or exercise in every formal learning, review, or learning-oriented debugging session. Use the existing lesson for a continuing topic; create a new numbered lesson for a new topic. Verify that the file exists, then report its absolute path in the first user-visible teaching response. The artifact is a no-answer learning map that shows:

- the goal,
- the session contract: independent level, time box, minimum runnable version, out-of-scope boundary, and required evidence,
- concepts and functions used in the lesson,
- the input / process / output target,
- prediction questions,
- exercise steps,
- blank space for observations.

Use `scripts/create_lesson.py` for a new topic; it adds a `prepared` entry to `lesson-index.json`. If existing lesson files have no index, run `scripts/rebuild_lesson_index.py` once. Use `scripts/update_lesson.py` for a continuing or completed lesson: `in-progress` before teaching, `complete` only with user evidence, and a next-review task when appropriate.

Do not include finished code, answer keys, exact final output, or final explanations in a start-of-lesson artifact. If the workspace cannot be written, request permission and pause instead of replacing the file with chat-only material. After the user has completed the evidence loop, update the lesson with what happened and what should be reviewed next.

## Reference

Create `reference/` notes for durable knowledge that will recur. A reference note should be shorter than a lesson and optimized for later review.

Create a concept reference after sufficient completion evidence. Create an error-pattern reference only after the same language/library area, error class or symptom, and root cause have appeared three cumulative times. Track the first and second occurrences in `review-queue/` or `practice-records/` instead.

Use the following format for a concept reference:

```md
# {Concept}

## Use when
{When this concept appears in project work.}

## Plain meaning
{Short explanation.}

## Common pattern
{Small reusable pattern or pseudocode.}

## Common mistake
{Mistake to watch for.}

## Review prompt
{One tiny question or exercise.}
```

## Learning Records

Write a learning record only when the user demonstrated understanding, corrected a misconception, completed a real run, or changed the learning path.

Recommended format:

```md
# YYYY-MM-DD {short topic}

## Practiced ability
{One programming ability, such as loops, debugging, file I/O, pandas, or code quality.}

## Independent completion
- Baseline level:
- Support needed:
- Resulting level:

## Evidence
- Prediction:
- User-run result:
- Input / Process / Output:

## Learned
{What changed in the user's understanding.}

## Acceptance
- Can run:
- Result correct:
- Tests sufficient:
- Meets today's floor:
- Current gap:

## Next target
{One small next step.}
```

Do not record material that was only explained by Codex.

## Concept Notes

Create a concept note when a concept will likely recur. Keep it compact:

```md
# {Concept}

## Plain meaning
{Short explanation in the user's language.}

## Example
{Small code or project example.}

## Common mistake
{What the user confused or may confuse.}

## Review task
{One tiny task to check retention later.}
```

## Review Queue

Add an item to `review-queue/` when a concept was shaky, recently learned, needed again soon, or when an error pattern has appeared fewer than three times.

```md
# Review: {concept}

## Why review
{Reason this matters now.}

## Prompt
{Question or tiny exercise.}

## Last evidence
{What the user last showed.}

## Error pattern tracking
- Pattern: {language or library + error class or symptom + root cause}
- Occurrences: {1 or 2}
- Last seen: {date or session}
- Next check: {one small diagnostic or transfer exercise}
```

When an error reaches three same-type occurrences, promote it to an error-pattern reference and retain one small review task in the queue. When the user asks to review, choose from this queue before inventing unrelated practice.
