# Example: Normal Learning Session

## User prompt

```text
Use $programming-learning-coach to continue my Python automation learning session.
```

## Good response shape

```text
学习资料已生成：/absolute/path/to/lessons/0016-dictionary-summary-values.html

Current stage: you are improving a weekly report script that reads task data and writes Markdown.

Independent level: 1. You can work with guided questions, but there is not yet enough evidence to claim you can rebuild this feature without prompts.

Time box: 30 minutes.

Tiny goal: make one small change to the task detail section without changing the summary.

Minimum runnable version: the original summary still renders and one detail row is shown correctly.

Not today: adding a new report section or refactoring unrelated functions.

Before changing code, predict this:
If the CSV has columns task, status, and hours, which two columns should the detail loop read first?
```

## Why this is good

- It chooses one small project-connected goal.
- It makes the ability baseline, minimum version, and boundary visible.
- It asks for prediction before code.
- It does not hand over a finished script.
- It sets up a later Input / Process / Output check.

## Completion gate

The Skill should mark this complete only after the user:

- predicted what should happen,
- ran the script locally,
- inspected the generated report,
- explained Input / Process / Output in their own words.

If the learner cannot provide the local run or explanation, the next session is a recovery task rather than a new concept.
