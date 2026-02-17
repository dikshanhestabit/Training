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



from features.feature_engineer import FeatureEngineer

def main():
    # Main execution function for feature engineering.
    logger.info("FEATURE ENGINEERING PIPELINE")
    
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
    
    
    logger.info("FEATURE ENGINEERING COMPLETE")
    logger.info(f"Original features: 15")
    logger.info(f"Engineered features: {X_transformed.shape[1] - 1}")
    


if __name__ == "__main__":
    main()

