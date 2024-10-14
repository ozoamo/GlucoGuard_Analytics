import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler

# Load the saved model
model_pkl_file = "jupyter-notebooks/model.pkl"
with open(model_pkl_file, 'rb') as file:
    model = pickle.load(file)

# Set the title of the Streamlit app
st.title("GlucoGuard Analytics Dashboard")

# Input features for prediction
st.header("Enter Patient Data")

# Create two columns for the input fields
col1, col2 = st.columns(2)

# Define the input fields in the first column
with col1:
    # Input age as a text box
    age = st.text_input("Age (years)", placeholder="Enter age (0-100)", value="")
    
    # Gender selection
    gender = st.selectbox("Gender", ["Male", "Female", "Unknown"])
    
    # Race selection
    race = st.selectbox("Race", ["Caucasian", "AfricanAmerican", "Hispanic", "Asian", "Other"])

# Define the sliders in the second column
with col2:
    time_in_hospital = st.slider("Time in Hospital (days)", min_value=1, max_value=30, step=1)
    num_lab_procedures = st.slider("Number of Lab Procedures", min_value=1, max_value=150, step=1)
    num_procedures = st.slider("Number of Procedures", min_value=0, max_value=10, step=1)
    num_medications = st.slider("Number of Medications", min_value=1, max_value=100, step=1)

# Create a row for Max Glucose Serum and A1C Result
st.subheader("Lab Information")
glucose_col, a1c_col = st.columns(2)

with glucose_col:
    max_glu_serum_transformed = st.selectbox("Max Glucose Serum", 
                                              ['Not measured', 'Normal', 'Elevated', 'High'], 
                                              index=0)

with a1c_col:
    A1Cresult_transformed = st.selectbox("A1C Result", 
                                          ['Not measured', 'Normal', 'High'], 
                                          index=0)

# Create a row for Diabetes Medication and Change of Medications
st.subheader("Medication Information")
med_col1, med_col2 = st.columns(2)

with med_col1:
    diabetesMed = st.selectbox("Diabetes Medication", ["No", "Yes"])

with med_col2:
    change = st.selectbox("Change of Medications", ["No", "Yes"])

# Medications list
medications = [
    'metformin', 'troglitazone', 'examide', 'citoglipton',
    'insulin', 'glyburide-metformin', 'glipizide-metformin', 
    'glimepiride-pioglitazone', 'metformin-rosiglitazone', 
    'metformin-pioglitazone', 'SU', 'mitiglinides', 
    'thiazolidinediones', 'glucosidase_inh'
]

# Initialize a dictionary to hold medication selections
med_inputs = {}

# Medication selection section
st.subheader("List of Medications")
st.write("Check the medications the patient takes:")

# Create two columns for medications
med_col1, med_col2 = st.columns(2)

# Create a flag for enabling/disabling the medication checkboxes
medication_disabled = diabetesMed == "No"

with med_col1:
    # Display half of the medications in the first column
    for med in medications[:len(medications)//2]:
        med_inputs[med] = st.checkbox(med.capitalize(), value=False, disabled=medication_disabled)

with med_col2:
    # Display the other half of the medications in the second column
    for med in medications[len(medications)//2:]:
        med_inputs[med] = st.checkbox(med.capitalize(), value=False, disabled=medication_disabled)

# Encode the categorical variables
age_cat = {str(i): i for i in range(101)}  # Updated to accept any age between 0 and 100
max_glu_serum_cat = {'Not measured': 0, 'Normal': 1, 'Elevated': 2, 'High': 3}
A1Cresult_cat = {'Not measured': 0, 'Normal': 1, 'High': 2}
binary_map = {"No": 0, "Yes": 1}

# Create an input DataFrame based on user inputs
input_data = pd.DataFrame({
    'age': [int(age) if age.isdigit() and 0 <= int(age) <= 100 else 0],  # Use the input age, default to 0 if invalid
    'max_glu_serum_transformed': [max_glu_serum_cat[max_glu_serum_transformed]],
    'A1Cresult_transformed': [A1Cresult_cat[A1Cresult_transformed]],
    'time_in_hospital': [time_in_hospital],
    'num_lab_procedures': [num_lab_procedures],
    'num_procedures': [num_procedures],
    'num_medications': [num_medications],
    'race_AfricanAmerican': [1 if race == "AfricanAmerican" else 0],
    'race_Asian': [1 if race == "Asian" else 0],
    'race_Caucasian': [1 if race == "Caucasian" else 0],
    'race_Hispanic': [1 if race == "Hispanic" else 0],
    'race_Other': [1 if race == "Other" else 0],
    'gender_Female': [1 if gender == "Female" else 0],
    'gender_Male': [1 if gender == "Male" else 0],
    'gender_Unknown': [1 if gender == "Unknown" else 0],
    'change_Ch': [1 if change == "Yes" else 0],
    'change_No': [1 if change == "No" else 0],
    'diabetesMed_Yes': [1 if diabetesMed == "Yes" else 0],
    'diabetesMed_No': [1 if diabetesMed == "No" else 0]
})

# Add the medications to the input DataFrame using checkbox inputs
for med in medications:
    input_data[med] = [binary_map['Yes'] if med_inputs[med] else binary_map['No']]

# Normalize the input data using the same scaler as in the training process
scaler = MinMaxScaler()
normalized_input_data = scaler.fit_transform(input_data)

# Perform prediction
if st.button("Predict Readmission"):
    prediction = model.predict(normalized_input_data)
    st.write("The model predicts the patient will " + ("be readmitted." if prediction[0] == 1 else "not be readmitted."))
