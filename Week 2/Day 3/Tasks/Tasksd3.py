import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import seaborn as sns

# ----------------------------------------------------------
# STEP 1: Load the real dataset
# ----------------------------------------------------------
df = sns.load_dataset("titanic")
print("STEP 1: Loaded dataset with shape:", df.shape)

# STEP 2: Choose features (X) and label (y)

features = ["pclass", "sex", "age", "fare", "sibsp", "parch"]
label = "survived"

data = df[features + [label]].copy()
print(f"\nSTEP 2: Selected features {features}")
print(f"STEP 2: Selected label '{label}'")

# STEP 3: Data preprocessing

# 3a. Handle missing values

print("\nSTEP 3a: Missing values before cleaning:")
print(data.isnull().sum())

data["age"] = data["age"].fillna(data["age"].median())

# 3b. Convert categorical text data into numbers

data["sex"] = data["sex"].map({"male": 0, "female": 1})

print("\nSTEP 3b: Missing values after cleaning:")
print(data.isnull().sum())

print("\nSTEP 3: Preview of cleaned data")
print(data.head())

# STEP 4: Split into features (X) and label (y)

X = data[features]
y = data[label]
print(f"\nSTEP 4: X shape = {X.shape}, y shape = {y.shape}")

# STEP 5: Feature scaling

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("\nSTEP 5: First row before scaling:")
print(X.iloc[0].values)
print("STEP 5: First row after scaling:")
print(X_scaled[0])

# STEP 6: Train/Test split

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print(f"\nSTEP 6: Training set size: {X_train.shape[0]} rows")
print(f"STEP 6: Testing set size:  {X_test.shape[0]} rows")
print(f"STEP 6: Train/test ratio:  {X_train.shape[0]}/{X_test.shape[0]} "
      f"(~{round(X_train.shape[0]/len(X)*100)}% / {round(X_test.shape[0]/len(X)*100)}%)")

# STEP 7: Summary

print("\nSTEP 7: SUMMARY")
print("-" * 50)
print("1. Loaded real Titanic dataset with", df.shape[0], "passengers.")
print("2. Selected 6 features (pclass, sex, age, fare, sibsp, parch)")
print("   and 1 label (survived) -> this is a CLASSIFICATION problem")
print("   because the label is a category (0 or 1), not a number.")
print("3. Filled missing 'age' values with the median, and converted")
print("   'sex' from text to numbers (preprocessing).")
print("4. Scaled all features to a similar range (feature scaling)")
print("   so no single feature dominates due to its size.")
print("5. Split data into 80% training / 20% testing, so the model")
print("   can be evaluated on data it has never seen.")
print("\nThe data (X_train, X_test, y_train, y_test) is now ready")
print("to be fed into a machine learning model in the next step.")