import pandas as pd
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

# STEP 1: Load and prepare the dataset of  Day 3
df = sns.load_dataset("titanic")

features = ["pclass", "sex", "age", "fare", "sibsp", "parch"]
label = "survived"

data = df[features + [label]].copy()
data["age"] = data["age"].fillna(data["age"].median())
data["sex"] = data["sex"].map({"male": 0, "female": 1})

X = data[features]
y = data[label]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
print("STEP 1: Data ready ->", X_train.shape[0], "train rows,", X_test.shape[0], "test rows")



# STEP 2: Define the models we want to compare

models = {
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
    "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
}
print("\nSTEP 2: Models to compare:", list(models.keys()))

# STEP 3: Train each model and evaluate it

results = []

for name, model in models.items():
    print(f"\n{'='*55}")
    print(f"Training: {name}")
    print(f"{'='*55}")

    # --- TRAINING: model learns patterns from the training data ---
    model.fit(X_train, y_train)

    # --- PREDICTION: model applies what it learned to new data ---
    y_pred_test = model.predict(X_test)
    y_pred_train = model.predict(X_train)

    # --- METRICS ---
    acc = accuracy_score(y_test, y_pred_test)
    prec = precision_score(y_test, y_pred_test)
    rec = recall_score(y_test, y_pred_test)
    f1 = f1_score(y_test, y_pred_test)
    cm = confusion_matrix(y_test, y_pred_test)

    # --- OVERFITTING CHECK ---
   
    train_acc = accuracy_score(y_train, y_pred_train)

    # --- CROSS-VALIDATION ---

    cv_scores = cross_val_score(model, X_scaled, y, cv=5)

    print(f"Accuracy (test):     {acc:.3f}")
    print(f"Precision:           {prec:.3f}")
    print(f"Recall:              {rec:.3f}")
    print(f"F1-score:            {f1:.3f}")
    print(f"Confusion matrix:\n{cm}")
    print(f"Train accuracy:      {train_acc:.3f}  (test: {acc:.3f}, "
          f"gap: {train_acc - acc:.3f})")
    print(f"Cross-val accuracy:  {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")

    results.append({
        "Model": name,
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1-score": f1,
        "CV Accuracy": cv_scores.mean(),
        "Overfit Gap": train_acc - acc,
    })

# STEP 4: Compare all models side by side

results_df = pd.DataFrame(results).sort_values("F1-score", ascending=False)
print(f"\n{'='*55}")
print("STEP 4: MODEL COMPARISON (sorted by F1-score)")
print(f"{'='*55}")
print(results_df.to_string(index=False))

# STEP 5: Select the best-performing model

best_model_row = results_df.iloc[0]
print(f"\nSTEP 5: BEST MODEL -> {best_model_row['Model']}")
print(f"  F1-score:     {best_model_row['F1-score']:.3f}")
print(f"  Accuracy:     {best_model_row['Accuracy']:.3f}")
print(f"  CV Accuracy:  {best_model_row['CV Accuracy']:.3f}")
print(f"  Overfit Gap:  {best_model_row['Overfit Gap']:.3f} "
      f"({'small, looks healthy' if abs(best_model_row['Overfit Gap']) < 0.1 else 'large, may be overfitting'})")

print("\nSTEP 5: WHY THIS ONE")
print("- Highest F1-score means the best balance of precision and recall.")
print(f"- Cross-validation accuracy ({best_model_row['CV Accuracy']:.3f}) is close to")
print(f"  test accuracy ({best_model_row['Accuracy']:.3f}), so the result is fairly")
print("  consistent, not just a lucky single train/test split.")
if abs(best_model_row['Overfit Gap']) < 0.1:
    print("- A small overfit gap means the model generalizes well to new data,")
    print("  rather than just memorizing the training set.")
else:
    print(f"- CAVEAT: the overfit gap ({best_model_row['Overfit Gap']:.3f}) is fairly large,")
    print("  meaning this model is fitting the training data notably better than")
    print("  the test data. It's still the best performer here, but a next step")
    print("  worth trying would be limiting tree depth (e.g. max_depth=5) to")
    print("  reduce overfitting and see if test performance improves further.")