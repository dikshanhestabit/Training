# Adult Income Prediction 

This repository contains the end-to-end Machine Learning pipeline for predicting income levels (`<=50K` or `>50K`) based on census data.

## Project Structure

- **data/**: Raw and processed datasets.
- **features/**: Feature engineering scripts and pipelines.
- **models/**: Saved models (`best_model.pkl`) and artifacts.
- **training/**: Scripts for model training and evaluation.
- **tuning/**: Hyperparameter tuning scripts.
- **deployment/**: APIs (`api.py`) and Docker configuration.
- **monitoring/**: Drift detection and dashboards.
- **notebooks/**: EDA and experimental notebooks.

## Quick Start

### 1. Setup Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run API
```bash
uvicorn deployment.api:app --reload
```
API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Run Monitoring Dashboard
```bash
streamlit run monitoring/dashboard.py
```

## Documentation

- [Data Analysis Report](DATA-REPORT.md)
- [Feature Engineering](FEATURE-ENGINEERING-DOC.md)
- [Model Comparison & Results](MODEL-COMPARISON.md)
- [Deployment Instructions](DEPLOYMENT-NOTES.md)
- [Model Interpretation (SHAP)](MODEL-INTERPRETATION.md)


