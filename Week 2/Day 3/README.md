# Week 2 — Day 3

## Task(s) Assigned
What is Machine Learning?
AI vs ML vs Deep Learning
Supervised learning
Unsupervised learning
Classification
Regression
Clustering
Features and labels
Training data
Testing data
Validation data
Train/test split
Data preprocessing
Feature scaling

Hands-on:
Prepare a dataset for machine learning.
Split data into training and testing sets.

## What I Did
I used a new virtual environment for this task and installed the necessary libraries (pandas, scikit-learn). The next thing I did was create a python script Using a data set to learn about Titanic, choosing relevant features and a label tackling missing data, encoding categorical data to numerical forms, scaling the data, etc.Data splitting into training (80%) and testing (20%) sets, and features using scikit-learn's train_test_split.

## Key Learnings
Firstly I revised the concept of machine learning — teaching machines to find
Identify patterns in data and make predictions based on data.Then I revised AI vs
Machine Learning and Deep Learning, as well as how AI is transforming machines to operate intelligently and using a set of rules.
systems, robotics, etc.). AI is a part of ML, in which machines learn from data.
Rather than hard coded rules. Deep Learning is a part of ML that employs
Multi-layered neural networks to do complex calculations. Supervised learning, data is labelled and in unsupervised learning, data is unlabeled.
Classification means Classification of data into categories (e.g. spam or not spam)
and works for supervised learning, while regression is a supervised learning
task whose output is a real number (e.g. fare, price, stocks).
Clustering is an unsupervised learning problem where similar data points are grouped together.
Without any pre-established categories (such as grouping passengers by similar age/fare)
patterns). Features and Labels — Features (X) are the columns being used in the model as inputs.
takes lessons from (age, fare, class). The label (y) is the solution you are seeking to
predict (survived). Training / Testing / Validation Data Training data is what
the model learns from. The cost of providing the test data is high, and it is not used to train the model.
— only used to see if model is working well on data not used to train the model. Validation data is
An optional third split during development to fine tune settings without losing data.
Data Preprocessing is cleaning and preparing raw
Data before feeding it to model. Train/Test Split is splitting your data so that
The model will not "cheat" by training and testing on the same data —
imitates its performance on "real unseen data". Feature Scaling — putting
numeric scales are on the same scale (e.g. age is 0-80, fare is 0-500)
The more there are numbers doesn't automatically mean that one feature is dominant.

## Files in this folder
- `Tasksd3.py` — Loads the Titanic dataset, selects features/label,
  preprocesses the data (fills missing values, encodes categorical columns),
  applies feature scaling, and splits the data into training and testing sets.
