import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# STEP 1: Load the real dataset

df = sns.load_dataset("titanic")
print("STEP 1: Loaded dataset with shape:", df.shape)

# STEP 2: Looking at the structure of the data

print("\nSTEP 2: First 5 rows")
print(df.head())

print("\nSTEP 2: Column data types")
print(df.dtypes)

print("\nSTEP 2: Missing values per column")
print(df.isnull().sum())

# STEP 3: Descriptive statistics
print("\nSTEP 3: Descriptive statistics for 'age' and 'fare'")
for col in ["age", "fare"]:
    print(f"\n{col.upper()}")
    print("  Mean:    ", round(df[col].mean(), 2))
    print("  Median:  ", round(df[col].median(), 2))
    print("  Mode:    ", df[col].mode()[0])
    print("  Variance:", round(df[col].var(), 2))
    print("  Std Dev: ", round(df[col].std(), 2))

# STEP 4: Correlation between numeric variables

numeric_df = df.select_dtypes(include="number")
corr_matrix = numeric_df.corr()
print("\nSTEP 4: Correlation matrix")
print(corr_matrix)

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("01_correlation_heatmap.png")
plt.show()

# STEP 5: Outlier detection

Q1 = df["fare"].quantile(0.25)
Q3 = df["fare"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df["fare"] < lower_bound) | (df["fare"] > upper_bound)]
print(f"\nSTEP 5: Outlier bounds for fare -> [{lower_bound:.2f}, {upper_bound:.2f}]")
print(f"STEP 5: Number of outliers found: {len(outliers)}")

plt.figure(figsize=(6, 4))
sns.boxplot(x=df["fare"])
plt.title("Boxplot of Fare (dots beyond whiskers = outliers)")
plt.tight_layout()
plt.savefig("02_fare_boxplot.png")
plt.show()

# STEP 6: Visualizations

# 6a. HISTOGRAM - shows the distribution/shape of a single numeric column
plt.figure(figsize=(7, 5))
plt.hist(df["age"].dropna(), bins=20, color="skyblue", edgecolor="black")
plt.title("Histogram: Distribution of Passenger Ages")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("03_histogram_age.png")
plt.show()

# 6b. BAR CHART - compares counts across categories
class_counts = df["class"].value_counts()
plt.figure(figsize=(6, 5))
plt.bar(class_counts.index, class_counts.values, color="salmon")
plt.title("Bar Chart: Passenger Count by Class")
plt.xlabel("Class")
plt.ylabel("Number of Passengers")
plt.tight_layout()
plt.savefig("04_bar_class.png")
plt.show()

# 6c. SCATTER PLOT - shows relationship between two numeric variables
plt.figure(figsize=(7, 5))
plt.scatter(df["age"], df["fare"], alpha=0.5, color="green")
plt.title("Scatter Plot: Age vs Fare")
plt.xlabel("Age")
plt.ylabel("Fare")
plt.tight_layout()
plt.savefig("05_scatter_age_fare.png")
plt.show()

# 6d. LINE CHART - shows how a value changes across an ordered category
avg_fare_by_class = df.groupby("pclass")["fare"].mean()
plt.figure(figsize=(6, 5))
plt.plot(avg_fare_by_class.index, avg_fare_by_class.values, marker="o", color="purple")
plt.title("Line Chart: Average Fare by Passenger Class")
plt.xlabel("Passenger Class")
plt.ylabel("Average Fare")
plt.xticks([1, 2, 3])
plt.tight_layout()
plt.savefig("06_line_avg_fare.png")
plt.show()

# STEP 7: Identify and summarize patterns

print("\nSTEP 7: PATTERNS IDENTIFIED")
print("-" * 50)
print("1. Fare is right-skewed: mean (32.2) >> median (14.45),")
print("   meaning most tickets were cheap but a few were very expensive.")
print("2. Age is roughly symmetric (mean ~30, median ~28) -> not skewed.")
print("3. pclass and fare are strongly negatively correlated (-0.55):")
print("   lower class number (1st class) = higher fare.")
print(f"4. {len(outliers)} fare outliers detected, almost certainly")
print("   1st class passengers with premium tickets.")
print("5. 3rd class had by far the most passengers (bar chart).")
print("6. Age and fare show no strong relationship (scatter plot,")
print("   correlation = 0.096) -> ticket price wasn't age-driven.")
print("7. Average fare clearly rises from 3rd -> 1st class (line chart),")
print("   confirming the class-based pricing structure.")

print("\nDone. All charts saved as PNG files (01-06) in the current folder.")