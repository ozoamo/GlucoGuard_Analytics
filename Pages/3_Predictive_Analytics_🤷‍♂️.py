import streamlit as st
import pandas as pd
import numpy as np

st.title("Predictive Analytics ")

# Function to simulate prediction (replace with your actual model)
def predict_readmission(features):
    # Simulated prediction logic (you should replace this with your actual model)
    # Here, we simply return "Yes" if the number of lab procedures is above a certain threshold
    if features['num_lab_procedures'] > 5:
        return "Yes"
    else:
        return "No"

# Set the title of the app
st.title("Patient Readmission Prediction")

# Create two columns for user input
col1, col2 = st.columns(2)

# Input fields in the first column
with col1:
    time_in_hospital = st.number_input("Time in Hospital (days)", min_value=1, max_value=30, value=5)
    num_lab_procedures = st.number_input("Number of Lab Procedures", min_value=0, max_value=100, value=10)
    num_procedures = st.number_input("Number of Procedures", min_value=0, max_value=10, value=1)
    num_medications = st.number_input("Number of Medications", min_value=1, max_value=50, value=5)
    number_outpatient = st.number_input("Number of Outpatient Visits", min_value=0, max_value=10, value=1)
    number_emergency = st.number_input("Number of Emergency Visits", min_value=0, max_value=5, value=0)

# Input fields in the second column
with col2:
    number_inpatient = st.number_input("Number of Inpatient Visits", min_value=0, max_value=5, value=0)
    number_diagnoses = st.number_input("Number of Diagnoses", min_value=1, max_value=20, value=2)
    
    race = st.selectbox("Race", ["Caucasian", "African American", "Hispanic", "Asian", "Other"])
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.selectbox("Age", ["[0-10)", "[10-20)", "[20-30)", "[30-40)", "[40-50)", "[50-60)", "[60-70)", "[70+]"])

# Nominal features in a single column
admission_type_id = st.selectbox("Admission Type ID", [1, 2, 3, 4, 5])
discharge_disposition_id = st.selectbox("Discharge Disposition ID", [1, 2, 3, 4, 5])
admission_source_id = st.selectbox("Admission Source ID", [1, 2, 3, 4, 5])
diag_1 = st.selectbox("Diagnosis 1", ["Diabetes", "Hypertension", "Heart Disease", "Other"])
diag_2 = st.selectbox("Diagnosis 2", ["None", "Diabetes", "Hypertension", "Heart Disease", "Other"])
diag_3 = st.selectbox("Diagnosis 3", ["None", "Diabetes", "Hypertension", "Heart Disease", "Other"])
max_glu_serum = st.selectbox("Max Glucose Serum", ["Normal", "Prediabetes", "Diabetes"])
A1Cresult = st.selectbox("A1C Result", ["Normal", "Prediabetes", "Diabetes"])

# Nominal medication options
medications = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride', 'acetohexamide',
               'glipizide', 'glyburide', 'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose',
               'miglitol', 'troglitazone', 'tolazamide', 'examide', 'citoglipton', 'insulin',
               'glyburide-metformin', 'glipizide-metformin', 'glimepiride-pioglitazone',
               'metformin-rosiglitazone', 'metformin-pioglitazone']

# Initialize a dictionary to store medication inputs
medication_inputs = {}

# Add an explanatory note for medication checkboxes
st.markdown("### Medication Use")
st.markdown("Check the box if you currently use any of the following medications:")

# Create two columns for medication checkboxes
med_col1, med_col2 = st.columns(2)

with med_col1:
    for med in medications[:len(medications)//2]:  # First half of medications
        medication_inputs[med] = st.checkbox(med)

with med_col2:
    for med in medications[len(medications)//2:]:  # Second half of medications
        medication_inputs[med] = st.checkbox(med)

# Predict button
if st.button("Predict Readmission"):
    # Collecting features into a dictionary
    features = {
        'time_in_hospital': time_in_hospital,
        'num_lab_procedures': num_lab_procedures,
        'num_procedures': num_procedures,
        'num_medications': num_medications,
        'number_outpatient': number_outpatient,
        'number_emergency': number_emergency,
        'number_inpatient': number_inpatient,
        'number_diagnoses': number_diagnoses,
        'race': race,
        'gender': gender,
        'age': age,
        'admission_type_id': admission_type_id,
        'discharge_disposition_id': discharge_disposition_id,
        'admission_source_id': admission_source_id,
        'diag_1': diag_1,
        'diag_2': diag_2,
        'diag_3': diag_3,
        'max_glu_serum': max_glu_serum,
        'A1Cresult': A1Cresult,
        'medications': medication_inputs
    }

    # Make prediction
    prediction = predict_readmission(features)
    st.success(f"The predicted readmission status is: **{prediction}**")