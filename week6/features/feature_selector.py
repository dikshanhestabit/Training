import pandas as pd
import numpy as np
import os
import sys
import json
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logger


class FeatureSelector:
    """Feature selection using mutual information."""
    
    def __init__(self, n_features=20):
        self.n_features = n_features
        self.selected_features = []
        self.mi_scores = None
        
    def fit(self, X, y):
        """Fit feature selector using mutual information."""
        logger.info("=" * 60)
        logger.info("FEATURE SELECTION PIPELINE")
        logger.info("=" * 60)
        
        logger.info("Calculating mutual information scores...")
        mi_scores = mutual_info_classif(X, y, random_state=42)
        self.mi_scores = pd.Series(mi_scores, index=X.columns).sort_values(ascending=False)
        
        self.selected_features = self.mi_scores.head(self.n_features).index.tolist()
        
        logger.info(f"Selected {len(self.selected_features)} features")
        logger.info(f"Top 10 features: {self.selected_features[:10]}")
        logger.info("=" * 60)
        
        return self
    
    def transform(self, X):
        """Apply feature selection to dataset."""
        return X[self.selected_features]
    
    def fit_transform(self, X, y):
        """Fit and transform in one step."""
        self.fit(X, y)
        return self.transform(X)
    
    def get_selected_features(self):
        """Get list of selected feature names."""
        return self.selected_features
    
    def plot_importance(self, output_dir='screenshots'):
        """Generate and save feature importance visualization."""
        os.makedirs(output_dir, exist_ok=True)
        
        plt.figure(figsize=(10, 8))
        self.mi_scores.head(20).sort_values().plot(kind='barh', color='steelblue')
        plt.xlabel('Mutual Information Score')
        plt.ylabel('Features')
        plt.title('Top 20 Features by Mutual Information')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'feature_importance.png'), dpi=300)
        plt.close()
        logger.info(f"Saved feature importance plot to {output_dir}/feature_importance.png")
    
    def save_feature_list(self, filepath):
        """Export selected features to JSON."""
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
    """Main execution function for feature selection."""
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
    
    X = df.drop('income', axis=1)
    y = df['income']
    
    selector = FeatureSelector(n_features=20)
    X_selected = selector.fit_transform(X, y)
    
    logger.info(f"Selected features shape: {X_selected.shape}")
    
    selector.plot_importance()
    selector.save_feature_list(FEATURE_LIST_PATH)
    
    logger.info("\nPerforming train-test split (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_selected, y, test_size=0.2, random_state=42, stratify=y
    )
    
    logger.info(f"X_train shape: {X_train.shape}")
    logger.info(f"X_test shape: {X_test.shape}")
    logger.info(f"y_train shape: {y_train.shape}")
    logger.info(f"y_test shape: {y_test.shape}")
    
    X_train.to_csv(X_TRAIN_PATH, index=False)
    X_test.to_csv(X_TEST_PATH, index=False)
    y_train.to_csv(Y_TRAIN_PATH, index=False, header=['income'])
    y_test.to_csv(Y_TEST_PATH, index=False, header=['income'])
    
    logger.info(f"\nTrain-test splits saved:")
    logger.info(f"  - {X_TRAIN_PATH}")
    logger.info(f"  - {X_TEST_PATH}")
    logger.info(f"  - {Y_TRAIN_PATH}")
    logger.info(f"  - {Y_TEST_PATH}")
    
    logger.info("\n" + "=" * 60)
    logger.info("FEATURE SELECTION COMPLETE")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
