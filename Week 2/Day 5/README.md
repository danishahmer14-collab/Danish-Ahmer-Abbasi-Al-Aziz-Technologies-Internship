# Week 2 — Day 5

## Task(s) Assigned
NumPy 
Pandas 
Data cleaning 
EDA 
Data visualization 
Machine learning concepts 
Classification 
Regression 
Model training 
Model evaluation 
scikit-learn 
Friday Deliverables:
- Working ML project
- Dataset documentation
- GitHub repository
- README.md
- Model evaluation report
- Project demonstration
## What I Did
Created an end-to-end machine learning pipeline that classifies Titanic passenger survival. A summary of the week's activities is presented. Assuming the the real Titanic dataset, the pipeline will load it (in Tasksd5.py) and clean it up by filling in missing data (SA5: Part 2: Step 5.3). The deck is dropped, age is filled in with the median, and missing embark_town is filled in with the mode.When more than 10% of data is missing, it renders a descriptive statistics or summary (EDA) report (correlation heatmap, outlier detection using IQR, and 4 chart types), preprocesses data for modeling (numeric sex for sex, scales features, etc.), splits into 80% training / 20% testing, then trains and compares four classification models: Logistic Regression, Decision Tree, Random Forest, and K-Nearest Neighbors. Additionally, I created full project documentation:a DATASET.md documenting each column and known data quality issues, and a MODEL_EVALUATION_REPORT.md analyzing these results and selecting a terminal model.
## Key Learnings
This project combined the entire week into one actual workflow of isolated exercises. Some of the first things I saw were how data cleaning decisions—such as clicking to select the median vs. mode for each column, or removing one of them with 77% missing data—have a direct impact on the EDA and models they can work with.Running all four models side by side made the differences between them much better than just reading about them in theory: overfit with Decision Tree. Logistic Regression has lower training accuracy (97.9%) compared to test accuracy (75.4%). This was the most similar with only a slight difference between train and test. Random Forest had the best F1-score (0.753) and won overall, but I learned that even “best” is not always the answer—there was a definite overfitting. Although it wasn't the most significant, the gap (0.180) should be flagged rather than ignored, because its value score looked best.While writing the model evaluation report, I learned that just as documenting a model's strengths is important, it is important to document reasons for selecting a model, including weaknesses, as important as the metrics themselves. In general, this project confirmed that the preprocessing, evaluation, and EDA are not distinct boxes to tick; building on each other, skipping or rushing through any one of them (such as not checking if a data point was missing early) would have been a problem later on in the pipeline.

## Files in this folder
- `Tasksd5.py` — Full ML pipeline: loads Titanic data, cleans it, runs EDA,
  preprocesses for ML, trains 4 models, evaluates and compares them.
- `DatasetDocumentation.md` — Documentation of the dataset's columns and known issues.
- `MODEL_EVALUATION_REPORT.md` — Full model comparison, analysis, and final
  model recommendation.
- `requirements.txt` — Python packages needed to run the project.
- 'ProjectDemonstration.txt'— contains demonstration of my project 
