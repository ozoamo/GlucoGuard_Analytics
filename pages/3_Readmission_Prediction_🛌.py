import streamlit as st
import pandas as pd
import numpy as np
import pickle
import shap
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Load the saved model
model_pkl_file = "jupyter-notebooks/model.pkl"
with open(model_pkl_file, 'rb') as file:
    model = pickle.load(file)

st.set_page_config(
    page_title="GlucoGuard Dashboard",
    page_icon="./assets/Page-icon.png",
)

#3_Predictive_Analytics_🤷‍♂️

# Set the title of the Streamlit app
st.title("Readmission Prediction")

# Sidebar configuration
st.sidebar.image("./assets/glucoguard-logo.png")
st.markdown(
"""
    ##### This tool helps you predict the chances of a patient being readmitted by analyzing their key health information, supporting better care decisions.
"""
)

# Input features for prediction
st.markdown("<h2 style='font-size:20px;'>Enter Patient and Clinical Data</h2>", unsafe_allow_html=True)

# Create two columns for the input fields
col1, col2 = st.columns(2)

# Define the input fields in the first column
with col1:
    age = st.selectbox("Age Group", 
                       ['[0-10)', '[10-20)', '[20-30)', '[30-40)', 
                        '[40-50)', '[50-60)', '[60-70)', 
                        '[70-80)', '[80-90)', '[90-100)'])
    gender = st.selectbox("Gender", ["Male", "Female", "Unknown"])
    race = st.selectbox("Race", ["Caucasian", "AfricanAmerican", "Hispanic", "Asian", "Other"])

# Define the sliders in the second column
with col2:
    time_in_hospital = st.slider("Time in Hospital (days)", min_value=0, max_value=20, step=1)
    num_lab_procedures = st.slider("Total Lab Tests Conducted", min_value=0, max_value=150, step=1)
    num_procedures = st.slider("Total Medical Procedures Performed", min_value=0, max_value=10, step=1,
                               help="Examples include: hemodialysis, diabetic foot care, cardiac stenting.")
    num_medications = st.slider("Number of Medications", min_value=0, max_value=30, step=1)

# Additional inputs for lab results and medication
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

# Medication information
st.subheader("Medication Information")
med_col1, med_col2 = st.columns(2)

with med_col1:
    diabetesMed = st.selectbox("Diabetes Medication", ["No", "Yes"])

with med_col2:
    change = st.selectbox("Change of Medications", ["No", "Yes"])

# Medications list
medications = [
    'Metformin', 'Examide', 'Citoglipton',
    'Insulin', 'Glyburide-Metformin', 'Glipizide-Metformin', 
    'Glimepiride-Pioglitazone', 'Metformin-Rosiglitazone', 
    'Metformin-Pioglitazone', 'Sulfonylureas', 'Mitiglinides', 
    'Thiazolidinediones', 'Glucosidase Inhibitors'
]

# Initialize a dictionary to hold medication selections
med_inputs = {}

# Create two columns for medications
med_col1, med_col2 = st.columns(2)
medication_disabled = diabetesMed == "No"

with med_col1:
    for med in medications[:len(medications)//2]:
        med_inputs[med] = st.checkbox(med.capitalize(), value=False, disabled=medication_disabled)

with med_col2:
    for med in medications[len(medications)//2:]:
        med_inputs[med] = st.checkbox(med.capitalize(), value=False, disabled=medication_disabled)

# Encode the categorical variables
age_cat = {
    '[0-10)': 0, '[10-20)': 1, '[20-30)': 2, '[30-40)': 3, 
    '[40-50)': 4, '[50-60)': 5, '[60-70)': 6, '[70-80)': 7, 
    '[80-90)': 8, '[90-100)': 9
}
max_glu_serum_cat = {'Not measured': 0, 'Normal': 1, 'Elevated': 2, 'High': 3}
A1Cresult_cat = {'Not measured': 0, 'Normal': 1, 'High': 2}
binary_map = {"No": 0, "Yes": 1}

# Create an input DataFrame based on user inputs
input_data = pd.DataFrame({
    'age': [age_cat[age]], 
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

def st_shap(plot, height=None):
    """Function to display a SHAP plot in Streamlit."""
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    st.components.v1.html(shap_html, height=height)

# Prediction button
if st.button("Predict Readmission"):
    prediction = model.predict(normalized_input_data)
    st.write("The model predicts the patient will " + ("be readmitted." if prediction[0] == 1 else "not be readmitted."))
    
    # SHAP analysis
    explainer = shap.Explainer(model)
    shap_values = explainer(normalized_input_data)
    
    st.subheader("SHAP Analysis")
    
    # SHAP Force Plot
    st.subheader("Force Plot")
    
    shap.initjs()  # Initialize JavaScript for SHAP
    
    # Only include features that have non-zero or non-empty input

    # Filter out the features that were not selected or are irrelevant
    relevant_features = input_data.columns[(input_data != 0).any(axis=0)]  # Filter non-zero features
    relevant_input_data = input_data[relevant_features]  # Filter input data accordingly
    relevant_shap_values = shap_values.values[0][:len(relevant_features)]  # Filter SHAP values to match

    # Display filtered force plot
    st_shap(shap.force_plot(explainer.expected_value, relevant_shap_values, relevant_input_data.iloc[0, :]))

    st.subheader("Explanation:")
    st.write("The plot shows which patient's characteristics contributed to the possibility of this patient's readmission. Features in red contributed to a higher likelihood of readmission (a positive prediction) while the ones in blue contributed to a lower likelihood of readmission (a negative prediction).")

    # Separate positive and negative contributions
    positive_contributions = [(name, value) for name, value in zip(relevant_features, relevant_shap_values) if value > 0]
    negative_contributions = [(name, value) for name, value in zip(relevant_features, relevant_shap_values) if value < 0]

    # Display the positive contributions
    st.subheader("Features contributing to a positive prediction")
    if positive_contributions:
        for feature, value in positive_contributions:
            st.write(f"Feature: **{feature}** | SHAP Value: **{value:.4f}**")
    else:
        st.write("No positive contributions for this prediction.")

    # Display the negative contributions
    st.subheader("Features contributing to a negative prediction")
    if negative_contributions:
        for feature, value in negative_contributions:
            st.write(f"Feature: **{feature}** | SHAP Value: **{value:.4f}**")
    else:
        st.write("No negative contributions for this prediction.")

st.write("**Please note that if the characteristcs contributing to the prediction are not clinically significant, consider clinical judgement over the result of this tool.**")
