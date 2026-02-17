# Model Comparison Report

## 1. Validation Performance

|                     |   Accuracy |   Precision |   Recall |   F1 Score |   ROC-AUC |
|:--------------------|-----------:|------------:|---------:|-----------:|----------:|
| Logistic Regression |   0.788518 |    0.538894 | 0.848451 |   0.659072 |  0.887302 |
| Random Forest       |   0.806958 |    0.570701 | 0.803036 |   0.667114 |  0.889779 |
| XGBoost             |   0.798937 |    0.556149 | 0.819876 |   0.662688 |  0.887538 |
| Neural Network      |   0.837785 |    0.695145 | 0.582475 |   0.633602 |  0.891591 |

## 2. Training Performance

|                     |   Accuracy |   Precision |   Recall |   F1 Score |   ROC-AUC |
|:--------------------|-----------:|------------:|---------:|-----------:|----------:|
| Logistic Regression |   0.789032 |    0.539530 | 0.848610 |   0.659660 |  0.887844 |
| Random Forest       |   0.849825 |    0.633150 | 0.895714 |   0.741875 |  0.942743 |
| XGBoost             |   0.845568 |    0.620659 | 0.923428 |   0.742354 |  0.941816 |
| Neural Network      |   0.844331 |    0.711146 | 0.596664 |   0.648499 |  0.899577 |

## Best Model Selection
The best model selected is **Random Forest**.

## Confusion Matrix
![Confusion Matrix](screenshots/confusion_matrix_best_model.png)
