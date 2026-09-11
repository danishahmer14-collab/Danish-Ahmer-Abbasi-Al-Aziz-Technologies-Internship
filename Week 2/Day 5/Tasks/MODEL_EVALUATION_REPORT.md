# Model Evaluation Report

## Task

Binary classification: predict whether a Titanic passenger survived (1) or
did not survive (0), based on `pclass`, `sex`, `age`, `fare`, `sibsp`, and
`parch`.

## Setup

- **Train/test split:** 80% train (712 rows) / 20% test (179 rows), fixed
  random seed for reproducibility.
- **Feature scaling:** StandardScaler applied to all features.
- **Cross-validation:** 5-fold, run on the full scaled dataset for a more
  reliable estimate than a single split.

## Models Compared

| Model | Accuracy | Precision | Recall | F1-score | CV Accuracy | Overfit Gap |
|---|---|---|---|---|---|---|
| **Random Forest** | 0.799 | 0.764 | 0.743 | **0.753** | 0.811 | 0.180 |
| Logistic Regression | 0.799 | 0.779 | 0.716 | 0.746 | 0.786 | 0.004 |
| K-Nearest Neighbors | 0.788 | 0.750 | 0.730 | 0.740 | 0.820 | 0.077 |
| Decision Tree | 0.754 | 0.708 | 0.689 | 0.699 | 0.780 | 0.225 |

*(Overfit Gap = training accuracy − test accuracy. Higher means the model
fit the training data more than it generalized to new data.)*

## Selected Model: Random Forest

Random Forest had the **highest F1-score (0.753)**, meaning the best
balance of precision (few false alarms) and recall (few missed survivors)
among the four models tested.

**Confusion matrix (test set, 179 passengers):**

| | Predicted: Did not survive | Predicted: Survived |
|---|---|---|
| **Actual: Did not survive** | 88 (True Negative) | 17 (False Positive) |
| **Actual: Survived** | 19 (False Negative) | 55 (True Positive) |

## Analysis

- **Logistic Regression** was the most consistent model — its train accuracy
  (0.803) and test accuracy (0.799) were nearly identical (gap: 0.004),
  meaning it generalizes very well, though its F1-score was slightly lower
  than Random Forest's.
- **Decision Tree** showed the clearest overfitting: 97.9% training accuracy
  vs. only 75.4% test accuracy — a 22.5-point gap. It memorized the training
  data rather than learning generalizable patterns, and had the weakest test
  performance overall.
- **Random Forest** performed best on the test set and cross-validation, but
  it also carried a large overfit gap (0.180), similar in cause to the
  Decision Tree (Random Forest is an ensemble of trees). It's the strongest
  model here, but not without a caveat.
- **K-Nearest Neighbors** had the smallest gap between test accuracy and
  cross-validation accuracy (0.788 vs. 0.820), suggesting stable, reliable
  performance, though its F1-score was mid-pack.

## Recommendation

**Random Forest is the recommended model** based on F1-score and
cross-validation accuracy. However, given its overfitting gap, a reasonable
next step before deployment would be to **tune hyperparameters** — for
example, limiting `max_depth` or increasing `min_samples_leaf` — to reduce
overfitting and check whether test performance improves further. Logistic
Regression is a strong, more stable alternative if consistency matters more
than squeezing out the last bit of F1-score.

## Limitations

- The dataset is small (891 rows), so single train/test splits can be
  somewhat noisy — cross-validation results are more trustworthy than the
  single-split numbers alone.
- No hyperparameter tuning (e.g., GridSearchCV) was performed; all models
  used scikit-learn's default settings except `random_state` for
  reproducibility.
- Features like `deck` were dropped due to missing data, which may have
  removed some predictive signal.