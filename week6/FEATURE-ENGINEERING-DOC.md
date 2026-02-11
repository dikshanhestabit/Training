# Feature Engineering & Selection Documentation

## Overview
This document details the feature engineering and selection pipeline implemented for the Adult Income dataset.

## 1. Categorical Encoding Strategies
Implemented multiple encoding strategies as per the task requirements to handle different types of categorical data:
- **Target Encoding:** Applied to high-cardinality features (`occupation`, `native.country`, `workclass`). This encodes categories based on the mean of the target variable, effectively capturing the relationship without exploding dimensionality.
- **OneHot Encoding:** Applied to features with fewer categories (`sex`, `race`, `marital.status`, `relationship`, `education`). This creates binary flags for each category, which is ideal for most ML models.
- **Label/Ordinal Mapping:** Education levels are represented by the existing `education.num` feature, preserving the natural order of educational attainment.

## 2. Numerical Transformations
To improve the distribution of numerical features and meet the task's "Advanced Transformations" criteria, we applied:
- **Log Transformation:** Used `log1p` on `capital.gain` and `capital.loss` to handle extreme skewness and zero values.
- **Sqrt Transformation:** Applied to `fnlwgt` to normalize its distribution.
- **Power Transformation:** Created squared terms (`age_squared`, `hours_squared`) to capture potential non-linear relationships.
- **Normalization:** Used `StandardScaler` on all numerical features to ensure they have a mean of 0 and standard deviation of 1.

## 3. Feature Generation (10+ New Features)
Generated **11+ new meaningful features** to improve model richness:
1. `capital.gain_log`: Log of capital gains.
2. `capital.loss_log`: Log of capital losses.
3. `fnlwgt_sqrt`: Square root of final weights.
4. `age_squared`: Quadratic term for age.
5. `hours_squared`: Quadratic term for working hours.
6. `age_hours`: Interaction between age and working hours.
7. `education_hours`: Interaction between education level and working hours.
8. `capital_total`: Total capital activity (gain + loss).
9. `is_married`: Binary indicator extracted from marital status.
10. `is_male`: Binary indicator extracted from gender.
11. `has_capital_gain`: Indicator for whether an individual had any capital gains.

## 4. Feature Selection
Applied feature selection to identify the most predictive features:
- **Mutual Information (MI):** We used MI to rank all 51 features (raw + engineered + encoded) and selected the top 20. MI captures any kind of statistical dependency (linear or non-linear) between the features and the target income.
- **Feature Importance Visualization:** The results were plotted in `screenshots/`, showing the top 20 most impactful features.

