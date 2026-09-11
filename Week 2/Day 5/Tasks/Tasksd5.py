import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# PART 1: LOAD DATA

print("=" * 60)
print("PART 1: LOAD DATA")
print("=" * 60)

df = sns.load_dataset("titanic")
print(f"Loaded {df.shape[0]} rows, {df.shape[1]} columns")
print(df.head())

# PART 2: DATA CLEANING

print("\n" + "=" * 60)
print("PART 2: DATA CLEANING")
print("=" * 60)

print("\nMissing values before cleaning:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# Fill missing age with median (robust to outliers)
df["age"] = df["age"].fillna(df["age"].median())

# Fill missing embark_town with the most common value (mode)
df["embark_town"] = df["embark_town"].fillna(df["embark_town"].mode()[0])

# Drop 'deck' - too many missing values (over 75%) to be useful
df = df.drop(columns=["deck"])

print("\nMissing values after cleaning:")
remaining_na = df.isnull().sum()
print(remaining_na[remaining_na > 0] if remaining_na.sum() > 0 else "None remaining (in used columns)")

# PART 3: EXPLORATORY DATA ANALYSIS (EDA)

print("\n" + "=" * 60)
print("PART 3: EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print("\nDescriptive statistics:")
print(df[["age", "fare"]].describe())

numeric_df = df.select_dtypes(include="number")
corr_matrix = numeric_df.corr()
print("\nCorrelation with 'survived':")
print(corr_matrix["survived"].sort_values(ascending=False))

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_correlation_heatmap.png")
plt.close()

# Outlier detection on fare
Q1, Q3 = df["fare"].quantile([0.25, 0.75])
IQR = Q3 - Q1
outliers = df[(df["fare"] < Q1 - 1.5*IQR) | (df["fare"] > Q3 + 1.5*IQR)]
print(f"\nFare outliers detected (IQR method): {len(outliers)}")

# Visualizations
plt.figure(figsize=(7, 5))
plt.hist(df["age"], bins=20, color="skyblue", edgecolor="black")
plt.title("Distribution of Passenger Ages")
plt.xlabel("Age"); plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_histogram_age.png")
plt.close()

plt.figure(figsize=(6, 5))
df["survived"].map({0: "Did not survive", 1: "Survived"}).value_counts().plot(
    kind="bar", color=["salmon", "seagreen"])
plt.title("Survival Counts")
plt.xlabel("Outcome"); plt.ylabel("Number of Passengers")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_bar_survival.png")
plt.close()

plt.figure(figsize=(7, 5))
plt.scatter(df["age"], df["fare"], c=df["survived"], cmap="coolwarm", alpha=0.6)
plt.title("Age vs Fare (colored by survival)")
plt.xlabel("Age"); plt.ylabel("Fare")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_scatter_age_fare.png")
plt.close()

avg_fare_by_class = df.groupby("pclass")["fare"].mean()
plt.figure(figsize=(6, 5))
plt.plot(avg_fare_by_class.index, avg_fare_by_class.values, marker="o", color="purple")
plt.title("Average Fare by Passenger Class")
plt.xlabel("Passenger Class"); plt.ylabel("Average Fare")
plt.xticks([1, 2, 3])
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_line_avg_fare.png")
plt.close()

print(f"\nAll EDA charts saved to '{OUTPUT_DIR}/' folder.")


# PART 4: PREPROCESSING FOR MACHINE LEARNING

print("\n" + "=" * 60)
print("PART 4: PREPROCESSING FOR MACHINE LEARNING")
print("=" * 60)

features = ["pclass", "sex", "age", "fare", "sibsp", "parch"]
label = "survived"

ml_data = df[features + [label]].copy()
ml_data["sex"] = ml_data["sex"].map({"male": 0, "female": 1})

X = ml_data[features]
y = ml_data[label]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
print(f"Features used: {features}")
print(f"Training set: {X_train.shape[0]} rows | Testing set: {X_test.shape[0]} rows")

# PART 5: MODEL TRAINING & EVALUATION

print("\n" + "=" * 60)
print("PART 5: MODEL TRAINING & EVALUATION")
print("=" * 60)

models = {
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
    "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
}

results = []

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred_test = model.predict(X_test)
    y_pred_train = model.predict(X_train)

    acc = accuracy_score(y_test, y_pred_test)
    prec = precision_score(y_test, y_pred_test)
    rec = recall_score(y_test, y_pred_test)
    f1 = f1_score(y_test, y_pred_test)
    train_acc = accuracy_score(y_train, y_pred_train)
    cv_scores = cross_val_score(model, X_scaled, y, cv=5)

    print(f"\n{name}")
    print(f"  Accuracy: {acc:.3f} | Precision: {prec:.3f} | Recall: {rec:.3f} | F1: {f1:.3f}")
    print(f"  Train acc: {train_acc:.3f} (gap: {train_acc - acc:.3f}) | CV acc: {cv_scores.mean():.3f}")

    results.append({
        "Model": name, "Accuracy": acc, "Precision": prec,
        "Recall": rec, "F1-score": f1, "CV Accuracy": cv_scores.mean(),
        "Overfit Gap": train_acc - acc,
    })

results_df = pd.DataFrame(results).sort_values("F1-score", ascending=False)
print("\n" + "-" * 60)
print("MODEL COMPARISON (sorted by F1-score)")
print("-" * 60)
print(results_df.to_string(index=False))

best_model_name = results_df.iloc[0]["Model"]
best_model = models[best_model_name]
y_pred_best = best_model.predict(X_test)
cm = confusion_matrix(y_test, y_pred_best)

print(f"\nBEST MODEL: {best_model_name}")
print(f"Confusion matrix:\n{cm}")

# Save comparison table and confusion matrix for the report
results_df.to_csv(f"{OUTPUT_DIR}/model_comparison.csv", index=False)

plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Did not survive", "Survived"],
            yticklabels=["Did not survive", "Survived"])
plt.title(f"Confusion Matrix - {best_model_name}")
plt.ylabel("Actual"); plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/06_confusion_matrix_best_model.png")
plt.close()

print(f"\nResults saved: {OUTPUT_DIR}/model_comparison.csv, "
      f"{OUTPUT_DIR}/06_confusion_matrix_best_model.png")
print("\nPipeline complete.")