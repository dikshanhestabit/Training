import pandas as pd
import numpy as np
import shap
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logger

def make_plots_dir():
    # Ensure screenshots directory exists
    os.makedirs('screenshots', exist_ok=True)

def plot_shap_summary(model, X, output_path):
    # Sampling 500 rows for faster SHAP computation
    X_sample = X.sample(n=min(500, len(X)), random_state=42)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)
    
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_sample, show=False)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def plot_feature_importance(model, feature_names, output_path):
    # Plot feature importance from model
    importance = model.feature_importances_
    indices = np.argsort(importance)[::-1]
    
    plt.figure(figsize=(10, 6))
    plt.title("Feature Importance")
    plt.bar(range(len(feature_names)), importance[indices], align="center")
    plt.xticks(range(len(feature_names)), np.array(feature_names)[indices], rotation=90)
    plt.xlim([-1, len(feature_names)])
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_error_heatmap(y_true, y_pred, output_path):
    # Confusion Matrix Heatmap
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', cbar=False)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Error Analysis Heatmap')
    plt.savefig(output_path)
    plt.close()

def main():
    X_TEST_PATH = os.path.join('data', 'processed', 'X_test.csv')
    Y_TEST_PATH = os.path.join('data', 'processed', 'y_test.csv')
    MODEL_PATH = os.path.join('models', 'best_tuned_model.pkl')
    
    if not os.path.exists(MODEL_PATH):
        logger.error("Tuned model not found. Run training/tuning.py first.")
        sys.exit(1)
        
    logger.info("Loading corrected test data and model...")
    X_test = pd.read_csv(X_TEST_PATH)
    y_test = pd.read_csv(Y_TEST_PATH)['income']
    model = joblib.load(MODEL_PATH)
    
    make_plots_dir()
    
    # 1. SHAP Analysis
    logger.info("Generating SHAP summary plot...")
    plot_shap_summary(model, X_test, 'screenshots/shap_summary.png')
    
    # 2. Error Analysis
    logger.info("Performing Error Analysis...")
    y_pred = model.predict(X_test)
    
    # Error Heatmap
    plot_error_heatmap(y_test, y_pred, 'screenshots/error_heatmap.png')
    
    # Print Classification Report
    report = classification_report(y_test, y_pred)
    print("\nClassification Report:\n", report)
    
    logger.info("Analysis complete. Check screenshots/ folder.")

if __name__ == "__main__":
    main()
