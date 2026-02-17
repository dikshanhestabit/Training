
import streamlit as st
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Model Monitoring Dashboard", layout="wide")

st.title("Adult Income Prediction - Monitoring Dashboard")

# Paths
LOGS_PATH = os.path.join('monitoring', 'prediction_logs.csv')
DRIFT_REPORT_PATH = os.path.join('monitoring', 'drift_report.json')

# 1. Prediction Logs
st.header("Recent Predictions")
if os.path.exists(LOGS_PATH):
    try:
        # Load logs 
        df_logs = pd.read_csv(LOGS_PATH)
        st.dataframe(df_logs.tail(50)) # Show last 50
        
        st.subheader("Prediction Distribution")
        fig, ax = plt.subplots()
        sns.countplot(x='prediction', data=df_logs, ax=ax)
        st.pyplot(fig)
        
        st.subheader("Probability Distribution")
        fig2, ax2 = plt.subplots()
        sns.histplot(df_logs['probability'], bins=20, kde=True, ax=ax2)
        st.pyplot(fig2)

    except Exception as e:
        st.error(f"Error loading logs: {e}")
else:
    st.info("No prediction logs found yet. Make some requests to the API!")

# 2. Drift Monitoring
st.header("Drift Monitoring")

if st.button("Run Drift Check Now"):
    # Running the script
    os.system("python monitoring/drift_checker.py")
    st.success("Drift check executed.")

if os.path.exists(DRIFT_REPORT_PATH):
    with open(DRIFT_REPORT_PATH, 'r') as f:
        report = json.load(f)
    
    st.write(f"**Last Check:** {report.get('timestamp')}")
    
    drift_status = " Drift Detected" if report.get('global_drift') else " No Significant Drift"
    st.subheader(f"Status: {drift_status}")
    
    st.json(report.get('details'))
else:
    st.info("No drift report found. Run the check above.")
