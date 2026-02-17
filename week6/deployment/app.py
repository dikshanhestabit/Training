import streamlit as st
import requests
import json

st.title("Income Prediction App")
st.write("Enter the details below to check if income is >50K or <=50K.")

# Inputs
age = st.number_input("Age", min_value=17, max_value=90, value=35)
workclass = st.selectbox("Workclass", ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Without-pay", "Never-worked"])
education = st.selectbox("Education", ["Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm", "Assoc-voc", "9th", "7th-8th", "12th", "Masters", "1st-4th", "10th", "Doctorate", "5th-6th", "Preschool"])
marital_status = st.selectbox("Marital Status", ["Married-civ-spouse", "Divorced", "Never-married", "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"])
occupation = st.selectbox("Occupation", ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", "Armed-Forces"])
relationship = st.selectbox("Relationship", ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"])
race = st.selectbox("Race", ["White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other", "Black"])
sex = st.selectbox("Sex", ["Female", "Male"])
capital_gain = st.number_input("Capital Gain", value=0)
capital_loss = st.number_input("Capital Loss", value=0)
hours_per_week = st.number_input("Hours per Week", value=40)
native_country = st.selectbox("Native Country", ["United-States", "India", "Mexico", "Other"])

# Education mapping
edu_map = {
    "Bachelors": 13, "Some-college": 10, "11th": 7, "HS-grad": 9, 
    "Prof-school": 15, "Assoc-acdm": 12, "Assoc-voc": 11, "9th": 5, 
    "7th-8th": 4, "12th": 8, "Masters": 14, "1st-4th": 2, "10th": 6, 
    "Doctorate": 16, "5th-6th": 3, "Preschool": 1
}

if st.button("Predict"):
    # Data to send
    data = {
        "age": age,
        "workclass": workclass,
        "fnlwgt": 189778,
        "education": education,
        "education.num": edu_map[education],
        "marital.status": marital_status,
        "occupation": occupation,
        "relationship": relationship,
        "race": race,
        "sex": sex,
        "capital.gain": capital_gain,
        "capital.loss": capital_loss,
        "hours.per.week": hours_per_week,
        "native.country": native_country
    }
    
    try:
        res = requests.post("http://127.0.0.1:8000/predict", json=data)
        
        if res.status_code == 200:
            output = res.json()
            st.write("### Result")
            st.write(f"Prediction: {output['prediction']}")
            st.write(f"Probability: {output['probability']:.2f}")
            st.write(f"Request ID: {output['request_id']}")
        else:
            st.error("Check if API is running.")
    except Exception as e:
        st.error(f"Error: {e}")
