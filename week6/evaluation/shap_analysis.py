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
    # Calculate SHAP values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X, show=False)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def plot_feature_importance(model, feature_names, output_path):
    # Plot feature importance from model
    importance = model.feature_importances_
    indices = np.argsort(importance)[::-1]
    
    plt.figure(figsize=(10, 6))
    plt.title("Feature Importance")
    plt.bar(range(X.shape[1]), importance[indices], align="center")
    plt.xticks(range(X.shape[1]), np.array(feature_names)[indices], rotation=90)
    plt.xlim([-1, X.shape[1]])
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
    INPUT_PATH = os.path.join('data', 'processed', 'features_engineered.csv')
    MODEL_PATH = os.path.join('models', 'best_tuned_model.pkl')
    
    if not os.path.exists(MODEL_PATH):
        logger.error("Tuned model not found. Run training/tuning.py first.")
        sys.exit(1)
        
    logger.info("Loading data and model...")
    df = pd.read_csv(INPUT_PATH)
    model = joblib.load(MODEL_PATH)
    
    X = df.drop('income', axis=1)
    y = df['income']
    
    # Split to get Test set (same seed as tuning.py)
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    make_plots_dir()
    
    # 1. SHAP Analysis
    logger.info("Generating SHAP summary plot...")
    plot_shap_summary(model, X_test, 'screenshots/shap_summary.png')
    
    # 2. Feature Importance
    logger.info("Generating feature importance chart...")
    #xgb has built-in plot_importance, but we can stick to simple bar chart
    plt.figure(figsize=(10, 8))
    feat_importances = pd.Series(model.feature_importances_, index=X.columns)
    feat_importances.nlargest(20).plot(kind='barh')
    plt.title('Feature Importance')
    plt.savefig('screenshots/feature_importance.png')
    plt.close()

    # 3. Error Analysis
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
