# Example: Start-Of-Lesson Map

## User prompt

```text
Use $programming-learning-coach. Before we start, generate today's lesson for reading a CSV with pandas.
```

## Good lesson shape

The lesson file must be created and its absolute path reported before the user starts coding:

```text
Lesson: Read CSV Columns With pandas

Goal:
Read a CSV file and distinguish file-loading failures from column-selection failures.

Lesson type: new-knowledge

Why now:
The next project step needs a reliable way to inspect unfamiliar CSV input before selecting a column.

Session contract:
- Independent level: 1.
- Time box: 30 minutes.
- Minimum runnable version: load one CSV and print its column names.
- Not today: filtering rows or generating a final report.
- Submit before advancement: terminal output and an Input / Process / Output explanation.

Concepts and functions:
- pandas: the library used to work with table-like data.
- read_csv(): loads a CSV file into a DataFrame.
- df.columns: shows the column names available in the data.
- df["column_name"]: selects one column by name.

Primary source:
- pandas `read_csv` documentation: verify how a CSV is loaded before making claims about DataFrame behavior.

New knowledge:

Core explanations:
- Loading a CSV and selecting a DataFrame column are separate operations; a successful load does not prove a requested column exists.
- The header row becomes the initial column labels, so inspecting `df.columns` is evidence about the actual input rather than a guess about the file.

Decision rule:
Check that the file loaded and inspect its real column labels before treating a column lookup failure as a problem in later report logic.

Contrasting cases:
- A missing file prevents the DataFrame from being created at all.
- A successfully loaded CSV with a misspelled header creates a DataFrame, but selecting the intended name can still fail.

How it works:
1. pandas reads file text and parses the header and rows into a DataFrame.
2. A later column lookup compares the requested name with the DataFrame's actual labels.

The examples above teach the rule. The exercise should use a different CSV and column names, so it cannot be solved by copying the examples.

Input / Process / Output target:
- Input: a CSV file with task data.
- Process: load the file and inspect column names.
- Output: know which column names are safe to use in the next step.

Before you run:
Predict what df.columns will show if the CSV has task,status,hours as its header.

Exercise:
1. Use a small CSV with different column names from the teaching cases.
2. Load it and inspect the actual column labels.
3. Compare your prediction with the actual output.
4. Explain Input / Process / Output in your own words.
```

## What must be absent

This start lesson should not include:

- the complete final script,
- an answer key,
- the exact final generated report,
- a completed Input / Process / Output explanation.

Those can be added only after the user attempts, runs, inspects, and explains.
