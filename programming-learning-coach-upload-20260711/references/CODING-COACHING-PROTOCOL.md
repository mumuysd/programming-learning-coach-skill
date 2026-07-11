# Coding Coaching Protocol

Use this reference to select the next programming task, design exercises, handle debugging, and assess completion.

## Ability Map

Classify the current lesson by the weakest useful ability:

- Syntax: names, expressions, indentation, imports, comments.
- Control flow: `if`, `for`, `while`, `break`, conditions.
- Functions: parameters, return values, scope, reuse.
- Data structures: strings, lists, dictionaries, tuples, sets.
- File I/O: paths, reading, writing, CSV, Markdown, JSON.
- Libraries: pandas, openpyxl, requests, datetime, pathlib, or project libraries.
- Debugging: reading errors, tracing values, isolating failing steps.
- Problem decomposition: splitting a user goal into input, process, and output.
- Code quality: naming, small functions, duplication, testability, simple structure.

Pick one primary ability per session. Secondary abilities may appear, but do not turn them into extra lessons unless they block progress.

## Exercise Ladder

Use the lowest exercise that still tests understanding:

1. Read code and explain what it does.
2. Predict output before running.
3. Fill one missing line or expression.
4. Fix one broken line.
5. Make a tiny modification to working code.
6. Transfer the pattern to a similar input.
7. Write the small function or script from scratch.

If the user fails a step twice, move one level down. If they succeed easily and explain clearly, move one level up next time.

## Teaching Loop

Use this loop for new concepts:

1. Connect the concept to the active project.
2. Ask a prediction or reading question.
3. Let the user attempt before explanation.
4. Give one hint, not the answer.
5. Ask the user to run and inspect output.
6. Ask for Input / Process / Output.
7. Explain briefly after evidence appears.
8. Add a transfer or review task only if it fits the session.

## Debugging Protocol

When debugging, train the process:

1. Identify the exact error type and line.
2. Restate what the program was trying to do.
3. Check the value or type of the variable closest to the failure.
4. Reduce the issue to the smallest reproducible case when needed.
5. Change one thing.
6. Run again.
7. Explain why the change fixed or did not fix the issue.

Do not replace this with a full corrected script unless the user explicitly asks for full code.

## Review And Retention

Use spaced and mixed review:

- Revisit shaky concepts after one or more later sessions.
- Mix old concepts into current project tasks.
- Ask the user to recreate a previous step without looking when appropriate.
- Put recurring weak points into `review-queue/`.
- Promote stable understanding into `concept-notes/`.

## Code Quality Check

For project work, success is not only "it runs." When the task is complete enough, check one quality dimension:

- Clear names.
- Small function or clear section.
- No unnecessary repetition.
- Input, process, and output are visible.
- The next change would be easy to make.
- A simple test or sample run exists.

Use only one quality focus per session unless the user asks for a broader review.

## Project English

Keep English tied to the coding work. Use it to reinforce the same Input / Process / Output model.

Default:

```text
Sentence: This script reads a CSV file and creates a weekly report.
Words: input, output, process, row, report
IPO: The input is..., the process is..., the output is...
```

Do not let English replace the programming task.
