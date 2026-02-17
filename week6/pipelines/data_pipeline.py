import pandas as pd
import numpy as np
import os
import sys

# Adding the project root to the python path to import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logger

def load_data(filepath):
    try:
        logger.info(f"Loading data from {filepath}...")
        df = pd.read_csv(filepath)
        logger.info(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found at {filepath}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        sys.exit(1)

def clean_data(df):
    logger.info("Starting data cleaning process...")
    
    # 1. Handling Missing Values
    # Replacing '?' with NaN
    df.replace('?', np.nan, inplace=True)
    
    initial_shape = df.shape
    
    # Checking for missing values
    missing_values = df.isnull().sum().sum()
    logger.info(f"Total missing values before imputation: {missing_values}")
    
    # Imputing missing values
    # For categorical columns, Mode is used
    # For numerical columns, Median is used
    for col in df.columns:
        if df[col].dtype == 'object':
            # Categorical column 
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])
        else:
            # Ensuring column is numeric before calculating median
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            
    logger.info("Missing values imputed.")
    
    # 2. Removing Duplicates
    duplicates = df.duplicated().sum()
    logger.info(f"files with duplicates: {duplicates}")
    if duplicates > 0:
        df.drop_duplicates(inplace=True)
        logger.info(f"Removed {duplicates} duplicate rows.")
        
    # 3. Handling Outliers (IQR Method) for numerical columns
    # focus on 'age' and 'hours-per-week' as likely candidates for outliers
    # Note: outlier removal can reduce dataset size significantly
   
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numerical_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Identifying outliers
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        logger.info(f"Column '{col}': found {len(outliers)} outliers.")
        
        # Capping outliers (Winsorization) 
        # df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
        df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])
        
    logger.info("Outliers handled (capped at 1.5*IQR bounds).")
    
    final_shape = df.shape
    logger.info(f"Data cleaning completed. Final shape: {final_shape}")
    
    return df

def save_data(df, output_path):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"Data saved successfully to {output_path}")
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        sys.exit(1)

def main():
    RAW_DATA_PATH = os.path.join('data', 'raw', 'adult.csv')
    PROCESSED_DATA_PATH = os.path.join('data', 'processed', 'final.csv')
    
    # Checking if raw data exists
    if not os.path.exists(RAW_DATA_PATH):
        logger.error(f"Raw data not found at {RAW_DATA_PATH}. Please download the dataset and place it there.")
        # Fallback to check for any csv in raw
        raw_files = [f for f in os.listdir(os.path.join('data', 'raw')) if f.endswith('.csv')]
        if raw_files:
            RAW_DATA_PATH = os.path.join('data', 'raw', raw_files[0])
            logger.info(f"Found {RAW_DATA_PATH}, using it instead.")
        else:
            sys.exit(1)

    # Executing pipeline
    df = load_data(RAW_DATA_PATH)
    clean_df = clean_data(df)
    save_data(clean_df, PROCESSED_DATA_PATH)

if __name__ == "__main__":
    main()
