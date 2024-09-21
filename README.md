Project Overview

This project focuses on predicting the price of insurance claims using machine learning algorithms.
Data Source

The dataset is sourced from real-time data provided by a leading medical aid society in Zimbabwe.
Data Preparation

 Data Import & Cleaning: The dataset was imported, cleaned, and appropriate character definitions were applied.
 Exploratory Data Analysis (EDA): EDA was performed to ensure that the data met formatting standards, with date columns cleaned and formatted correctly.

Data Processing

   Train-Test Split: The dataset was split into training and testing sets before proceeding with feature engineering.
   Feature Engineering: This included transformations and adjustments to the dataset to enhance model performance.
   Missing Value Treatment: Missing values were treated using median imputation to support the assumption of normality.
   One-Hot Encoding: Categorical variables were converted into a numerical format using one-hot encoding on the training set.

Model Development & Evaluation

   Model Evaluation: Models were evaluated, and the Root Mean Squared Error (RMSE) and Relative Mean Error (RME) were found to be at minimal levels, indicating low error rates.
   Random Forest Model: After evaluating several algorithms, predictions were made using Random Forest models, which yielded strong results.
