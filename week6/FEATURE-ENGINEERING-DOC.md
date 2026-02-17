# Feature Engineering & Selection Documentation 

## Overview
This document details the advanced feature engineering and selection pipeline implemented for the Adult Income dataset, optimized for high recall and minimal overfitting.

## 1. Categorical Encoding Strategies
Implemented a hybrid encoding strategy to balance information retention and dimensionality:
- **OneHot Encoding:** Applied to lower-cardinality features (`sex`, `race`, `marital.status`, `relationship`, `education`). 
- **Target Encoding:** Used for mapping high-cardinality features like `native.country`, `workclass`, and `occupation`.
- **Ordinal Mapping:** Leveraged the pre-existing `education.num` to preserve the inherent hierarchy of schooling.

## 2. Numerical Transformations & Signal Capture
To capture non-linearities and handle skewed data:
- **Interaction Terms**: Created `age_hours` and `education_hours` to represent how experience and education interact with working intensity.
- **Polynomial Features**: Added `age_squared` and `hours_squared` to model peak earning years and burnout effects.
- **Signal Aggregation**: Created `capital_total` (sum of gain and loss) and `has_capital_gain` (binary flag) to ensure the model captures the overwhelming signal from capital activity even after scaling.
- **Scaling**: All final features are normalized using `StandardScaler`.

## 3. Advanced Feature Selection (RFE)

Moved from simple Mutual Information to **Recursive Feature Elimination (RFE)** using a Random Forest estimator with a **Split-Before-Select** methodology to prevent data leakage.

- **Original Feature Count**: 52 (after encoding and engineering).
- **Reduced Feature Count**: **20 Features**.
- **Crucial Removal**: **`fnlwgt`** (Final Weight) was explicitly removed.
    - *Why?* `fnlwgt` is a sampling weight used by the Census Bureau for population scaling. It is not intrinsic to an individual's earning capacity and often leads to overfitting in high-capacity models.
- **Selection Strategy**:
    - By reducing the feature set to the **Top 20 signals**, minimized model noise and improved the "leakage-free" F1 Score.
    - The top features identified are `occupation`, `age_hours`, and `marital.status_Married-civ-spouse`.

## 4. Final Feature List
The final set of 20 features centers on:
1.  **Work/Education Details**: `occupation`, `education.num`, `education_hours`.
2.  **Stability/Demographics**: `is_married`, `age`, `age_squared`, `is_male`.
3.  **Intensity**: `age_hours`, `hours.per.week`.

The full list is archived in `features/feature_list.json`.
