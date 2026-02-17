import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys

# Adding project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logger

def generate_report():
    # Loading data
    processed_path = 'data/processed/final.csv'
    if not os.path.exists(processed_path):
        logger.error(f"File not found: {processed_path}")
        sys.exit(1)
        
    df = pd.read_csv(processed_path)
    logger.info(f"Loaded processed data. Shape: {df.shape}")
    
    # Creating output directory for figures
    report_dir = 'screenshots'
    os.makedirs(report_dir, exist_ok=True)
    
    # Generating Plots
    
    # 1. Target Distribution
    plt.figure(figsize=(8, 6))
    if 'income' in df.columns:
        sns.countplot(x='income', data=df)
        plt.title('Distribution of Income')
        plt.savefig(f'{report_dir}/income_distribution.png')
        plt.close()
        logger.info("Generated income_distribution.png")
    
    # 2. Correlation Matrix
    plt.figure(figsize=(10, 8))
    numeric_df = df.select_dtypes(include=['number'])
    if not numeric_df.empty:
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix')
        plt.savefig(f'{report_dir}/correlation_matrix.png')
        plt.close()
        logger.info("Generated correlation_matrix.png")
    
    # 2b. Missing Values Heatmap (on raw data for demonstration)
    # Load raw data to show missing values before cleaning
    raw_path = 'data/raw/adult.csv'
    if os.path.exists(raw_path):
        raw_df = pd.read_csv(raw_path)
        raw_df.replace('?', pd.NA, inplace=True)  # Replace '?' with NA for visualization
        
        plt.figure(figsize=(12, 6))
        sns.heatmap(raw_df.isnull(), cbar=True, cmap='viridis', yticklabels=False)
        plt.title('Missing Values Heatmap (Raw Data)')
        plt.xlabel('Features')
        plt.ylabel('Samples')
        plt.savefig(f'{report_dir}/missing_values_heatmap.png')
        plt.close()
        logger.info("Generated missing_values_heatmap.png")

    # 3. Feature Distributions
    numeric_cols = ['age', 'fnlwgt', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']
    for col in numeric_cols:
        if col in df.columns:
            plt.figure(figsize=(8, 4))
            sns.histplot(df[col], kde=True)
            plt.title(f'Distribution of {col}')
            plt.savefig(f'{report_dir}/{col}_distribution.png')
            plt.close()
            logger.info(f"Generated {col}_distribution.png")
            
    # Generating Stats for Report
    with open('screenshots/eda_stats.txt', 'w') as f:
        f.write("### Dataset Statistics\n")
        f.write(f"- Total Rows: {df.shape[0]}\n")
        f.write(f"- Total Columns: {df.shape[1]}\n")
        f.write("\n### Column Check\n")
        f.write(str(df.dtypes))
        f.write("\n\n### Missing Values (Processed)\n")
        f.write(str(df.isnull().sum()))
        f.write("\n\n### Descriptive Statistics\n")
        f.write(str(df.describe()))
    
    logger.info("Generated stats in screenshots/eda_stats.txt")

if __name__ == "__main__":
    generate_report()
