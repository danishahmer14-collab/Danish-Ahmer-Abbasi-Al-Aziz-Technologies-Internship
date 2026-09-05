import pandas as pd
import numpy as np

# ---------- 1. Load a real-world dataset ----------
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

print("===== First 5 rows =====")
print(df.head())

print("\n===== Dataset shape (rows, columns) =====")
print(df.shape)

print("\n===== Column info =====")
print(df.info())

# ---------- 2. Explore basic statistics ----------
print("\n===== Descriptive statistics =====")
print(df.describe())

# ---------- 3. Check for missing values ----------
print("\n===== Missing values per column =====")
print(df.isnull().sum())

# ---------- 4. Clean the data ----------

# Fill missing 'Age' values with the column's mean (numeric column)
df["Age"] = df["Age"].fillna(df["Age"].mean())

# Fill missing 'Embarked' values with the most common value (mode)
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

# 'Cabin' has too many missing values to fill meaningfully — drop the column
df = df.drop(columns=["Cabin"])

# Check and remove duplicate rows
print("\n===== Duplicate rows before cleaning =====")
print(df.duplicated().sum())

df = df.drop_duplicates()

# ---------- 5. Confirm the cleaning worked ----------
print("\n===== Missing values AFTER cleaning =====")
print(df.isnull().sum())

print("\n===== Duplicate rows AFTER cleaning =====")
print(df.duplicated().sum())

print("\n===== Cleaned dataset shape =====")
print(df.shape)

# ---------- 6. Basic column selection & filtering (bonus practice) ----------

# Select specific columns
print("\n===== Name and Age columns =====")
print(df[["Name", "Age"]].head())

# Filter rows: passengers older than 50
print("\n===== Passengers older than 50 =====")
print(df[df["Age"] > 50].head())

# Sort by Fare, descending
print("\n===== Top 5 highest fares =====")
print(df.sort_values("Fare", ascending=False).head())

# Save the cleaned dataset for later use
df.to_csv("titanic_cleaned.csv", index=False)
print("\nCleaned dataset saved to titanic_cleaned.csv")