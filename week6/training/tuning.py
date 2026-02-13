import pandas as pd
import numpy as np
import optuna
import xgboost as xgb
import joblib
import json
import os
import sys
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import f1_score

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logger

def load_data(filepath):
    # Load engineered features
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        sys.exit(1)
    return pd.read_csv(filepath)

def objective(trial, X, y):
    # Define hyperparameter search space
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'use_label_encoder': False,
        'n_jobs': -1,
        'random_state': 42,
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000, step=100),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'gamma': trial.suggest_float('gamma', 0, 5),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10)
    }
    
    # Stratified K-Fold CV to handle imbalance if any
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    model = xgb.XGBClassifier(**params)
    
    # Optimize for F1 Score
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
    
    # Split data for final evaluation (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    logger.info("Starting Optuna optimization...")
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X_train, y_train), n_trials=50)
    
    logger.info(f"Best trial: {study.best_trial.value}")
    logger.info(f"Best params: {study.best_trial.params}")
    
    # Save best parameters
    results_path = os.path.join(RESULTS_DIR, 'results.json')
    with open(results_path, 'w') as f:
        json.dump(study.best_trial.params, f, indent=4)
    logger.info(f"Tuning results saved to {results_path}")
    
    # Retrain best model on full training set
    logger.info("Retraining best model...")
    best_params = study.best_trial.params
    # Add fixed params
    best_params.update({
        'objective': 'binary:logistic',
        'eval_metric': 'logloss', 
        'use_label_encoder': False,
        'random_state': 42
    })
    
    final_model = xgb.XGBClassifier(**best_params)
    final_model.fit(X_train, y_train)
    
    # Save tuned model
    model_path = os.path.join(MODELS_DIR, 'best_tuned_model.pkl')
    joblib.dump(final_model, model_path)
    logger.info(f"Tuned model saved to {model_path}")

if __name__ == "__main__":
    main()
