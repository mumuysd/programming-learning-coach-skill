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
Read a CSV file and identify which columns the script can use.

Concepts and functions:
- pandas: the library used to work with table-like data.
- read_csv(): loads a CSV file into a DataFrame.
- df.columns: shows the column names available in the data.
- df["column_name"]: selects one column by name.

Input / Process / Output target:
- Input: a CSV file with task data.
- Process: load the file and inspect column names.
- Output: know which column names are safe to use in the next step.

Before you run:
Predict what df.columns will show if the CSV has task,status,hours as its header.

Exercise:
1. Load the CSV.
2. Print the column names.
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
