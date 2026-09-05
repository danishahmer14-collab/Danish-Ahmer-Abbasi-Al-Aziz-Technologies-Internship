#pandas 
import pandas as pd

# Series - 1D labeled array
s = pd.Series([10, 20, 30])

# DataFrame - 2D table (like Excel)
df = pd.DataFrame({
    "name": ["Ali", "Sara", "Danish"],
    "age": [20, 19, 21],
    "marks": [80, 92, 74]
})
print(df)
#Reading csv and JSon file
df = pd.read_csv("data.csv")
df = pd.read_json("data.json")
#Selecting Columns
print(df["name"])              # one column
print(df[["name", "marks"]])    # multiple columns
#Filtering Rows
print(df[df["marks"] > 80])           # rows where marks > 80
print(df[(df["age"] > 19) & (df["marks"] > 75)])   # multiple conditions
#Sorting
df.sort_values("marks")                    # ascending
df.sort_values("marks", ascending=False)    # descending
#Mising Values
df.isnull().sum()          # count missing values per column
df.dropna()                 # remove rows with missing values
df.fillna(0)                 # fill missing values with 0
df["marks"].fillna(df["marks"].mean())   # fill with column mean
# Duplicate Values
df.duplicated().sum()       # count duplicate rows
df.drop_duplicates()         # remove duplicates
#Basic Data Cleaning (typical pipeline)
df = df.drop_duplicates()
df["marks"] = df["marks"].fillna(df["marks"].mean())
df = df.dropna(subset=["name"])   # drop rows only if name is missing