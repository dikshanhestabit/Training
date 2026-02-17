import pandas as pd
import numpy as np
import os
import sys
import json
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
)
from sklearn.base import clone

import xgboost as xgb
import lightgbm as lgb

# Adding project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logger

def load_data(filepath):
    """Load processed features."""
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        sys.exit(1)
    df = pd.read_csv(filepath)
    return df

def train_and_evaluate(X, y, models, k=5):
    """Train models using k-fold cross-validation."""
    results = {}
    best_model_name = None
    best_score = -1
    best_model_instance = None 

    kf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
    scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']

    for name, model in models.items():
        logger.info(f"Training {name} with {k}-fold CV...")
        cv_results = cross_validate(model, X, y, cv=kf, scoring=scoring, n_jobs=-1, return_train_score=True)
        
        # Validation Metrics
        mean_metrics = {
            'Accuracy': float(np.mean(cv_results['test_accuracy'])),
            'Precision': float(np.mean(cv_results['test_precision'])),
            'Recall': float(np.mean(cv_results['test_recall'])),
            'F1 Score': float(np.mean(cv_results['test_f1'])),
            'ROC-AUC': float(np.mean(cv_results['test_roc_auc']))
        }
        
        # Training Metrics
        train_metrics = {
            'Accuracy': float(np.mean(cv_results['train_accuracy'])),
            'Precision': float(np.mean(cv_results['train_precision'])),
            'Recall': float(np.mean(cv_results['train_recall'])),
            'F1 Score': float(np.mean(cv_results['train_f1'])),
            'ROC-AUC': float(np.mean(cv_results['train_roc_auc']))
        }
        
        results[name] = {
            'Validation': mean_metrics,
            'Training': train_metrics
        }
        
        logger.info(f"{name} Val F1: {mean_metrics['F1 Score']:.4f}")

        if mean_metrics['F1 Score'] > best_score:
            best_score = mean_metrics['F1 Score']
            best_model_name = name
            best_model_instance = model

    return results, best_model_name, best_model_instance

def plot_confusion_matrix(model, X, y, output_path):
    """Generate confusion matrix plot."""
    y_pred = model.predict(X)
    cm = confusion_matrix(y, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.savefig(output_path)
    plt.close()

def main():
    INPUT_PATH = os.path.join('data', 'processed', 'features_engineered.csv')
    MODELS_DIR = 'models'
    EVAL_DIR = 'evaluation'
    
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(EVAL_DIR, exist_ok=True)
    
    logger.info("Loading data...")
    df = load_data(INPUT_PATH)
    
    X = df.drop('income', axis=1)
    y = df['income']
    
    # Loading Selected Features
    FEATURE_LIST_PATH = os.path.join('features', 'feature_list.json')
    if not os.path.exists(FEATURE_LIST_PATH):
        logger.error(f"Feature list not found. Run feature_selector.py first.")
        sys.exit(1)
        
    with open(FEATURE_LIST_PATH, 'r') as f:
        feature_data = json.load(f)
        selected_features = feature_data.get('selected_features', [])
    
    X = X[selected_features]
    
    # Calculating class weights
    neg_count = (y == 0).sum()
    pos_count = (y == 1).sum()
    scale_pos_weight = neg_count / pos_count
 
    # Initializing Models
    models = {
        'Logistic Regression': LogisticRegression(
            max_iter=1000, 
            random_state=42, 
            class_weight='balanced',
            solver='liblinear'
        ),
        'Random Forest': RandomForestClassifier(
            n_estimators=300, 
            random_state=42, 
            class_weight='balanced',
            min_samples_leaf=5 
        ),
        'XGBoost': xgb.XGBClassifier(
            use_label_encoder=False, 
            eval_metric='logloss', 
            random_state=42, 
            scale_pos_weight=scale_pos_weight,
            n_estimators=300,
            learning_rate=0.1
        ),
        'Neural Network': MLPClassifier(
            hidden_layer_sizes=(100, 50), 
            max_iter=1000, 
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )
    }
    
    # Training
    results, best_model_name, best_model_instance = train_and_evaluate(X, y, models)
    
    # Saving Metrics
    metrics_path = os.path.join(EVAL_DIR, 'metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(results, f, indent=4)
    
    # Saving Best Model
    logger.info(f"Saving best model: {best_model_name}")
    best_model_instance.fit(X, y)
    model_path = os.path.join(MODELS_DIR, 'best_model.pkl')
    joblib.dump(best_model_instance, model_path)
    
    # Plotting
    screenshots_dir = 'screenshots'
    os.makedirs(screenshots_dir, exist_ok=True)
    cm_path = os.path.join(screenshots_dir, 'confusion_matrix_best_model.png')
    plot_confusion_matrix(best_model_instance, X, y, cm_path)

    # Report Generation
    comparison_path = 'MODEL-COMPARISON.md'
    with open(comparison_path, 'w') as f:
        f.write("# Model Comparison Report\n\n")
        
        f.write("## 1. Validation Performance\n\n")
        f.write("|                     |   Accuracy |   Precision |   Recall |   F1 Score |   ROC-AUC |\n")
        f.write("|:--------------------|-----------:|------------:|---------:|-----------:|----------:|\n")
        
        for name, metrics in results.items():
            val = metrics['Validation']
            f.write(f"| {name:<19} | {val['Accuracy']:10.6f} | {val['Precision']:11.6f} | {val['Recall']:8.6f} | {val['F1 Score']:10.6f} | {val['ROC-AUC']:9.6f} |\n")
            
        f.write("\n## 2. Training Performance\n\n")
        f.write("|                     |   Accuracy |   Precision |   Recall |   F1 Score |   ROC-AUC |\n")
        f.write("|:--------------------|-----------:|------------:|---------:|-----------:|----------:|\n")
        
        for name, metrics in results.items():
            train = metrics['Training']
            f.write(f"| {name:<19} | {train['Accuracy']:10.6f} | {train['Precision']:11.6f} | {train['Recall']:8.6f} | {train['F1 Score']:10.6f} | {train['ROC-AUC']:9.6f} |\n")
        
        f.write(f"\n## Best Model Selection\n")
        f.write(f"The best model selected is **{best_model_name}**.\n\n")
        
        f.write("## Confusion Matrix\n")
        f.write("![Confusion Matrix](screenshots/confusion_matrix_best_model.png)\n")

    logger.info(f"Report saved to {comparison_path}")

if __name__ == "__main__":
    main()
