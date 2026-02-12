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

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logger

def load_data(filepath):
    """Load engineered features."""
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        sys.exit(1)
    df = pd.read_csv(filepath)
    return df

def train_and_evaluate(X, y, models, k=5):
    """
    Train multiple models using k-fold cross-validation and return metrics.
    """
    results = {}
    best_model_name = None
    best_score = -1
    best_model_instance = None # To retrain later

    kf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
    
    scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']

    for name, model in models.items():
        logger.info(f"Training {name} with {k}-fold CV...")
        
        cv_results = cross_validate(model, X, y, cv=kf, scoring=scoring, n_jobs=-1)
        
        # Calculate mean scores
        mean_metrics = {
            'Accuracy': float(np.mean(cv_results['test_accuracy'])),
            'Precision': float(np.mean(cv_results['test_precision'])),
            'Recall': float(np.mean(cv_results['test_recall'])),
            'F1 Score': float(np.mean(cv_results['test_f1'])),
            'ROC-AUC': float(np.mean(cv_results['test_roc_auc']))
        }
        
        results[name] = mean_metrics
        logger.info(f"{name} Results: {mean_metrics}")

        # Determine best model based on F1 Score (or ROC-AUC)
        if mean_metrics['F1 Score'] > best_score:
            best_score = mean_metrics['F1 Score']
            best_model_name = name
            best_model_instance = model

    return results, best_model_name, best_model_instance

def plot_confusion_matrix(model, X, y, output_path):
    """Generate and save confusion matrix plot."""
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
    
    # Initialize Models
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'XGBoost': xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42),
        'Neural Network': MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
    }
    
    # Train and Evaluate
    results, best_model_name, best_model_instance = train_and_evaluate(X, y, models)
    
    # Save Metrics
    metrics_path = os.path.join(EVAL_DIR, 'metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(results, f, indent=4)
    logger.info(f"Metrics saved to {metrics_path}")
    
    # Retrain Best Model on Full Data
    logger.info(f"Retraining best model ({best_model_name}) on full dataset...")
    best_model_instance.fit(X, y)
    
    # Save Best Model
    model_path = os.path.join(MODELS_DIR, 'best_model.pkl')
    joblib.dump(best_model_instance, model_path)
    logger.info(f"Best model saved to {model_path}")
    
    # Plot Confusion Matrix for Best Model
    cm_path = os.path.join(EVAL_DIR, 'confusion_matrix.png')
    plot_confusion_matrix(best_model_instance, X, y, cm_path)
    logger.info(f"Confusion matrix saved to {cm_path}")

    # Create/Update MODEL-COMPARISON.md
    comparison_path = 'MODEL-COMPARISON.md'
    with open(comparison_path, 'w') as f:
        f.write("# Model Comparison Report\n\n")
        f.write("| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |\n")
        f.write("|-------|----------|-----------|--------|----------|---------|\n")
        for name, metrics in results.items():
            f.write(f"| {name} | {metrics['Accuracy']:.4f} | {metrics['Precision']:.4f} | {metrics['Recall']:.4f} | {metrics['F1 Score']:.4f} | {metrics['ROC-AUC']:.4f} |\n")
        
        f.write(f"\n\n**Best Model:** {best_model_name} (F1 Score: {results[best_model_name]['F1 Score']:.4f})\n")
    logger.info(f"Model comparison report saved to {comparison_path}")

if __name__ == "__main__":
    main()
