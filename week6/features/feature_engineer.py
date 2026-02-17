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
        #Transforming features and generate new features.
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
        
        # Normalizing numerical features
        logger.info("Normalizing numerical features...")
        
        if self.scaler is None:
            self.scaler = StandardScaler()
            # Selecting numerical columns (all columns after encoding should be numeric)
            X_numeric = X.select_dtypes(include=[np.number])
            
            # Fit scaler and save feature names
            X_scaled = self.scaler.fit_transform(X_numeric)
            
            # Update columns in X (in-place modification)
            X[X_numeric.columns] = X_scaled
            self.feature_names = X.columns.tolist()
        else:
            # Inference phase: align columns to match training
            expected_features = getattr(self.scaler, 'feature_names_in_', self.feature_names)
            
            # Identify missing columns and fill with 0
            # Identify extra columns and drop them
            X = X.reindex(columns=expected_features, fill_value=0)
            
            # Checking for any remaining non-numeric columns (shouldn't happen but safe)
            X_numeric = X.select_dtypes(include=[np.number])
            
            # Now scale
            X[X_numeric.columns] = self.scaler.transform(X[X_numeric.columns])
        
        # Ensuring final output columns match training exactly
        if self.feature_names:
             X = X.reindex(columns=self.feature_names, fill_value=0)

        logger.info(f"Feature engineering complete. Total features: {len(X.columns)}")
        
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



if __name__ == "__main__":
    pass

