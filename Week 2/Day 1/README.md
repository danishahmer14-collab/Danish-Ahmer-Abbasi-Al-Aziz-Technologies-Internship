# Week 2 — Day 1

## Task(s) Assigned
NumPy arrays, array shapes, indexing, and broadcasting.Pandas basics — Series, DataFrames, reading CSV/JSON, selecting columns, filtering rows, sorting, handling missing values, removing duplicates, and basic data cleaning. Hands-on: load a real-world dataset and clean/explore it using Pandas.

## What I Did
Refreshed NumPy array operations (shapes, indexing, broadcasting, mathematical operations) and Pandas basics (Series vs DataFrames). I loaded a real world dataset called Titanic dataset, identified missing values with is null sum method and filled the missing values in numeric columns with the column mean and removed duplicate rows using the drop duplicates method. Before further analyzing the data, I used .describe() and .head() to get a feel for what the data was like.

## Key Learnings
I learned that there is a difference between a NumPy array that is purely numeric and a Pandas DataFrame, which is tabular, labeled data that can contain a mix of numeric and string data, more appropriate for real-world data. I also learned about the importance of data cleaning prior to analysis; omitting or discarding missing data and duplicate data can affect statistics and result in incorrect conclusions. I found the filtering and selecting of specific columns/rows a bit like SQL-style querying and found it easier to think about that.

## Files in this folder
numpyExercise.py contains numpy arrays indexing Broadcasting and mathematical operation,PandasExercise.py contains basic pandas operation Reading csv and JSon file through pandas,Filtering rows ,sorting ,selecting columns,Duplicate Values,Basic Data Cleaning Pipeline `DataCleaning.py` has loads the Titanic dataset, checks and handles missing values, removes duplicates, and explores the data using `.describe()` and `.head()`,
