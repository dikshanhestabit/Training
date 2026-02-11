import pandas as pd
import numpy as np
import os
import sys
import joblib
from sklearn.preprocessing import StandardScaler
from category_encoders import TargetEncoder
import warnings
warnings.filterwarnings('ignore')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logger


class FeatureEngineer:
    
    def __init__(self):
        self.target_encoder = None
        self.scaler = None
        self.feature_names = None
        
    def fit(self, X, y):
        logger.info("Fitting feature engineering pipeline...")
        
        high_cardinality_cols = ['occupation', 'native.country', 'workclass']
        self.target_encoder = TargetEncoder(cols=high_cardinality_cols)
        self.target_encoder.fit(X[high_cardinality_cols], y)
        
        logger.info("Feature engineering pipeline fitted successfully.")
        return self
    
    def transform(self, X, y=None):
        #Transform features and generate new features.
        logger.info("Transforming features...")
        X = X.copy()
        
        # Categorical Encoding
        logger.info("Encoding categorical features...")
        high_cardinality_cols = ['occupation', 'native.country', 'workclass']
        X[high_cardinality_cols] = self.target_encoder.transform(X[high_cardinality_cols])
        
        # Numerical Transformations
        logger.info("Applying numerical transformations...")
        X['capital.gain_log'] = np.log1p(X['capital.gain'])
        X['capital.loss_log'] = np.log1p(X['capital.loss'])
        X['fnlwgt_sqrt'] = np.sqrt(X['fnlwgt'])
        X['age_squared'] = X['age'] ** 2
        X['hours_squared'] = X['hours.per.week'] ** 2
        
        # Generate new features
        logger.info("Generating new features...")
        X['age_hours'] = X['age'] * X['hours.per.week']
        X['education_hours'] = X['education.num'] * X['hours.per.week']
        X['capital_total'] = X['capital.gain'] + X['capital.loss']
        X['is_married'] = X['marital.status'].str.contains('Married').astype(int)
        X['is_male'] = (X['sex'] == 'Male').astype(int)
        X['has_capital_gain'] = (X['capital.gain'] > 0).astype(int)
        
        # OneHot encode remaining categorical features
        logger.info("OneHot encoding categorical features...")
        categorical_cols = ['sex', 'race', 'marital.status', 'relationship', 'education']
        X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
        
        # Normalize numerical features
        logger.info("Normalizing numerical features...")
        numerical_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        
        if self.scaler is None:
            self.scaler = StandardScaler()
            X[numerical_cols] = self.scaler.fit_transform(X[numerical_cols])
        else:
            X[numerical_cols] = self.scaler.transform(X[numerical_cols])
        
        self.feature_names = X.columns.tolist()
        logger.info(f"Feature engineering complete. Total features: {len(self.feature_names)}")
        
        return X
    
    def fit_transform(self, X, y):
        """Fit and transform in one step."""
        self.fit(X, y)
        return self.transform(X, y)
    
    def save_pipeline(self, filepath):
        """Save the fitted pipeline to disk."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)
        logger.info(f"Pipeline saved to {filepath}")
    
    @staticmethod
    def load_pipeline(filepath):
        """Load a fitted pipeline from disk."""
        pipeline = joblib.load(filepath)
        logger.info(f"Pipeline loaded from {filepath}")
        return pipeline


def main():
    """Main execution function for feature engineering."""
    logger.info("=" * 60)
    logger.info("FEATURE ENGINEERING PIPELINE")
    logger.info("=" * 60)
    
    INPUT_DATA_PATH = os.path.join('data', 'processed', 'final.csv')
    OUTPUT_DATA_PATH = os.path.join('data', 'processed', 'features_engineered.csv')
    PIPELINE_PATH = os.path.join('features', 'feature_pipeline.pkl')
    
    logger.info(f"Loading cleaned data from {INPUT_DATA_PATH}...")
    df = pd.read_csv(INPUT_DATA_PATH)
    logger.info(f"Data loaded. Shape: {df.shape}")
    
    X = df.drop('income', axis=1)
    y = df['income'].apply(lambda x: 1 if x.strip() == '>50K' else 0)
    
    logger.info(f"Features shape: {X.shape}")
    logger.info(f"Target distribution: {y.value_counts().to_dict()}")
    
    feature_engineer = FeatureEngineer()
    X_transformed = feature_engineer.fit_transform(X, y)
    
    logger.info(f"Transformed features shape: {X_transformed.shape}")
    
    X_transformed['income'] = y
    X_transformed.to_csv(OUTPUT_DATA_PATH, index=False)
    logger.info(f"Engineered features saved to {OUTPUT_DATA_PATH}")
    
    feature_engineer.save_pipeline(PIPELINE_PATH)
    
    logger.info("=" * 60)
    logger.info("FEATURE ENGINEERING COMPLETE")
    logger.info(f"Original features: 15")
    logger.info(f"Engineered features: {X_transformed.shape[1] - 1}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
