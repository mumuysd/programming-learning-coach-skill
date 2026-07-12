# Example: Debugging Learning Session

## User prompt

```text
Use $programming-learning-coach. My pandas script raises KeyError: 'status'.
```

## Good response shape

```text
学习资料已生成：/absolute/path/to/lessons/0017-debug-pandas-keyerror-status.html

Let's debug this as a learning step, not just patch it.

Minimum runnable version: inspect the actual columns and reproduce the failing lookup once.

Not today: rewriting the whole script or adding new report features.

First question: where does the code read df["status"], and what are the actual CSV column names?

Before changing anything, predict the likely cause:
1. The column is missing.
2. The column exists but has extra spaces.
3. The code is reading the wrong file.

Which one do you think is most likely, and why?
```

## Why this is good

- It trains error reading.
- It asks for the line and actual data shape.
- It narrows the issue before proposing a fix.
- It avoids replacing the whole script.

## Completion gate

The Skill should not mark the step complete until the user explains:

```text
Input: the CSV file and its columns.
Process: pandas reads the file and looks up the status column.
Output: the script either prints/writes the report or raises KeyError when the column is missing.
```
