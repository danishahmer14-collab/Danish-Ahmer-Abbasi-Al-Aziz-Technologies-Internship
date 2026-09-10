# Week 2 — Day 4

## Task(s) Assigned
Introduction to scikit-learn
Linear Regression
Logistic Regression
Decision Trees
Random Forest
K-Nearest Neighbors
Model training
Prediction
Accuracy
Precision
Recall
F1-score
Confusion matrix
Mean Squared Error
Overfitting
Underfitting
Cross-validation basics

Hands-on:
Train multiple machine learning models.
Compare model performance.
Select the best-performing model.

## What I Did
I used the cleaned and split Titanic dataset from Day 3 (features: pclass, sex, age, fare, sibsp, parch, label: survived) and trained four different classification models from scikit-learn: Logistic Regression, Decision Tree, Random Forest, and K-Nearest Neighbors. For each model, I trained it on the training set, made predictions on the test set, and calculated accuracy, precision, recall, F1-score, and a confusion matrix. I also compared each model's training accuracy against its test accuracy to check for overfitting, and ran 5-fold cross-validation for a more reliable performance estimate. Finally, I built a comparison table of all four models sorted by F1-score and selected the best-performing one.

## Key Learnings
I learned that scikit-learn provides a consistent interface (.fit() to train, .predict() to predict) across very different algorithms, which makes comparing models straightforward. Linear Regression predicts continuous numbers, while Logistic Regression, despite its name, is actually used for classification. Decision Trees split data through a series of yes/no questions and are easy to interpret but prone to overfitting, which I saw directly in my results: the Decision Tree had 97.9% training accuracy but only 75.4% test accuracy, a huge gap showing it had memorized the training data instead of learning general patterns. Random Forest builds many trees and averages them, which usually helps with overfitting, but in my run it still showed a fairly large train/test gap (97.9% vs 79.9%). K-Nearest Neighbors classifies a point based on its closest neighbors and had the smallest gap between accuracy and cross-validation score (78.8% vs 82.0%), suggesting good generalization. I also learned the difference between accuracy, precision, and recall — accuracy alone can be misleading, so precision (how many predicted positives were correct) and recall (how many actual positives were caught) give a fuller picture, which F1-score combines into one number. The confusion matrix showed exactly where each model's errors came from (false positives vs false negatives). Cross-validation gave a more trustworthy performance estimate than a single train/test split by averaging results across 5 different splits. In my results, Random Forest had the highest F1-score (0.753) and was selected as the best model overall, though I noted its overfitting gap as a caveat worth investigating further (e.g. limiting tree depth).
## Files in this folder
  Tasksd4.py` — Trains Logistic Regression, Decision Tree,
  Random Forest, and K-Nearest Neighbors on the Titanic dataset, evaluates each
  with accuracy/precision/recall/F1/confusion matrix, checks for overfitting via
  train-vs-test accuracy and cross-validation, then compares all models and
  selects the best performing one.
