import pandas as pd
import numpy as np
import optuna
import joblib
import json
import os
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
import matplotlib.pyplot as plt

# Adding project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logger

def load_data(filepath):
    # Loading engineered features
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        sys.exit(1)
    return pd.read_csv(filepath)

def objective(trial, X, y):
    # Defining hyperparameter search space
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000, step=50),
        'max_depth': trial.suggest_int('max_depth', 5, 30),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
        'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None]),
        'class_weight': 'balanced',
        'random_state': 42,
        'n_jobs': -1
    }
    
    # Stratified K-Fold CV to handle imbalance
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    model = RandomForestClassifier(**params)
    
    # Optimizing for F1 Score
    scores = cross_val_score(model, X, y, cv=cv, scoring='f1', n_jobs=-1)
    return scores.mean()

def main():
    INPUT_PATH = os.path.join('data', 'processed', 'features_engineered.csv')
    RESULTS_DIR = 'tuning'
    MODELS_DIR = 'models'
    
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    logger.info("Loading data for tuning...")
    df = load_data(INPUT_PATH)
    
    X = df.drop('income', axis=1)
    y = df['income']
    
    # Loading selected features
    FEATURE_LIST_PATH = os.path.join('features', 'feature_list.json')
    if os.path.exists(FEATURE_LIST_PATH):
        with open(FEATURE_LIST_PATH, 'r') as f:
            feature_data = json.load(f)
            selected_features = feature_data.get('selected_features', [])
            if selected_features:
                X = X[selected_features]
                logger.info(f"Tuning on {len(selected_features)} selected features.")
    
    # Splitting data for final evaluation (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    logger.info("Starting Optuna optimization...")
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X_train, y_train), n_trials=50)
    
    logger.info(f"Best trial: {study.best_trial.value}")
    logger.info(f"Best params: {study.best_trial.params}")
    
    # Saving best parameters
    results_path = os.path.join(RESULTS_DIR, 'results.json')
    with open(results_path, 'w') as f:
        json.dump(study.best_trial.params, f, indent=4)
    logger.info(f"Tuning results saved to {results_path}")
    
    # Retraining best model on full training set
    logger.info("Retraining best model...")
    
    # 1. Baseline Model (Standard params)
    baseline_model = RandomForestClassifier(n_estimators=300, class_weight='balanced', random_state=42)
    baseline_model.fit(X_train, y_train)
    y_pred_base = baseline_model.predict(X_test)
    
    baseline_metrics = {
        "f1": f1_score(y_test, y_pred_base),
        "accuracy": accuracy_score(y_test, y_pred_base),
        "precision": precision_score(y_test, y_pred_base),
        "recall": recall_score(y_test, y_pred_base)
    }

    # 2. Tuned Model
    best_params = study.best_trial.params
    best_params.update({
        'class_weight': 'balanced',
        'random_state': 42,
        'n_jobs': -1
    })
    
    final_model = RandomForestClassifier(**best_params)
    final_model.fit(X_train, y_train)
    y_pred_tuned = final_model.predict(X_test)
    
    tuned_metrics = {
        "f1": f1_score(y_test, y_pred_tuned),
        "accuracy": accuracy_score(y_test, y_pred_tuned),
        "precision": precision_score(y_test, y_pred_tuned),
        "recall": recall_score(y_test, y_pred_tuned)
    }
    
    # Saving comparison evidence
    comparison_data = {
        "baseline": baseline_metrics,
        "tuned": tuned_metrics,
        "improvement_f1": tuned_metrics["f1"] - baseline_metrics["f1"],
        "best_params": study.best_trial.params
    }
    
    with open(os.path.join(RESULTS_DIR, 'comparison.json'), 'w') as f:
        json.dump(comparison_data, f, indent=4)
        
    logger.info(f"Comparison evidence saved. F1 Improvement: {comparison_data['improvement_f1']:.4f}")
    
    # Saving tuned model
    model_path = os.path.join(MODELS_DIR, 'best_tuned_model.pkl')
    joblib.dump(final_model, model_path)
    logger.info(f"Tuned model saved to {model_path}")
    
    # Saving importance plot for tuned model
    plt.figure(figsize=(10, 8))
    feat_importances = pd.Series(final_model.feature_importances_, index=X_train.columns)
    feat_importances.nlargest(20).plot(kind='barh')
    plt.title("Feature Importance (Tuned Random Forest)")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig(os.path.join('screenshots', 'feature_importance_tuned.png'))
    plt.close()

if __name__ == "__main__":
    main()
