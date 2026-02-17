import sys
import os
import pandas as pd
import numpy as np
import json
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Adding project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logger

class FeatureSelector:
    # Feature selection using Recursive Feature Elimination (RFE).
    
    def __init__(self, n_features=20):
        self.n_features = n_features
        self.selected_features = []
        self.mi_scores = None 
        self.estimator = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        
    def fit(self, X, y):
        # Fit feature selector using RFE.
        
        logger.info("FEATURE SELECTION PIPELINE (RFE)")
        
        
        logger.info(f"Running RFE with RandomForest to select top {self.n_features} features...")
        rfe = RFE(estimator=self.estimator, n_features_to_select=self.n_features, step=1)
        rfe.fit(X, y)
        
        self.selected_features = X.columns[rfe.support_].tolist()
        
        # Using the underlying model's feature importance instead of just 1/rank
        # This provides a realistic distribution of scores
        self.mi_scores = pd.Series(rfe.estimator_.feature_importances_, index=self.selected_features).sort_values(ascending=False)
        
        logger.info(f"Selected {len(self.selected_features)} features")
        logger.info(f"Top 10 features: {self.selected_features[:10]}")
        
        
        return self

    def transform(self, X):
        # Applying feature selection to dataset.
        return X[self.selected_features]
    
    def fit_transform(self, X, y):
        # Fit and transform in one step.
        self.fit(X, y)
        return self.transform(X)
    
    def get_selected_features(self):
        # Get list of selected feature names.
        return self.selected_features
    
    def plot_importance(self, output_dir='screenshots'):
        # Generating and saving feature importance visualization.
        os.makedirs(output_dir, exist_ok=True)
        
        plt.figure(figsize=(10, 8))
        # Plot top 20
        self.mi_scores.head(20).sort_values().plot(kind='barh', color='seagreen')
        plt.xlabel('RFE Score (1/Rank)')
        plt.ylabel('Features')
        plt.title('Top 20 Features by RFE Ranking')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'feature_importance_rfe.png'), dpi=300)
        plt.close()
        logger.info(f"Saved feature importance plot to {output_dir}/feature_importance_rfe.png")
    
    def save_feature_list(self, filepath):
        # Exporting selected features to JSON.
        feature_data = {
            'total_features_before_selection': len(self.mi_scores),
            'total_features_after_selection': len(self.selected_features),
            'selected_features': self.selected_features,
            'feature_importance_scores': self.mi_scores.to_dict()
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(feature_data, f, indent=2)
        
        logger.info(f"Feature list saved to {filepath}")


def main():
    # Main execution function for feature selection.
    logger.info("Starting feature selection process...")
    
    INPUT_DATA_PATH = os.path.join('data', 'processed', 'features_engineered.csv')
    FEATURE_LIST_PATH = os.path.join('features', 'feature_list.json')
    
    X_TRAIN_PATH = os.path.join('data', 'processed', 'X_train.csv')
    X_TEST_PATH = os.path.join('data', 'processed', 'X_test.csv')
    Y_TRAIN_PATH = os.path.join('data', 'processed', 'y_train.csv')
    Y_TEST_PATH = os.path.join('data', 'processed', 'y_test.csv')
    
    logger.info(f"Loading engineered features from {INPUT_DATA_PATH}...")
    df = pd.read_csv(INPUT_DATA_PATH)
    logger.info(f"Data loaded. Shape: {df.shape}")
    
    # DROPPING NOISY FEATURES: fnlwgt is sampling weight, irrelevant to income prediction
    # If the model uses it, it's overfitting to the specific sampling of the dataset.
    drop_cols = ['income', 'fnlwgt', 'fnlwgt_sqrt']
    existing_drop_cols = [c for c in drop_cols if c in df.columns]
    
    X = df.drop(existing_drop_cols, axis=1)
    y = df['income']

    # 1. SPLITTING DATA FIRST (To avoid data leakage)
    logger.info("\nPerforming train-test split (80/20) BEFORE selection...")
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 2. SELECTING FEATURES ONLY USING TRAINING DATA
    # Selection strategy: Reducing feature bloat (20 features) to improve generalization
    selector = FeatureSelector(n_features=20)
    X_train_selected = selector.fit_transform(X_train_raw, y_train)
    X_test_selected = selector.transform(X_test_raw)
    
    logger.info(f"Selected features shape (Train): {X_train_selected.shape}")
    
    selector.plot_importance()
    selector.save_feature_list(FEATURE_LIST_PATH)
    
    logger.info(f"X_train shape: {X_train_selected.shape}")
    logger.info(f"X_test shape: {X_test_selected.shape}")
    logger.info(f"y_train shape: {y_train.shape}")
    logger.info(f"y_test shape: {y_test.shape}")
    
    X_train_selected.to_csv(X_TRAIN_PATH, index=False)
    X_test_selected.to_csv(X_TEST_PATH, index=False)
    y_train.to_csv(Y_TRAIN_PATH, index=False, header=['income'])
    y_test.to_csv(Y_TEST_PATH, index=False, header=['income'])
    
    logger.info(f"\nTrain-test splits saved:")
    logger.info(f"  - {X_TRAIN_PATH}")
    logger.info(f"  - {X_TEST_PATH}")
    logger.info(f"  - {Y_TRAIN_PATH}")
    logger.info(f"  - {Y_TEST_PATH}")
    
   
    logger.info("FEATURE SELECTION COMPLETE")
    


if __name__ == "__main__":
    main()
