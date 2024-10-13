import os
import pickle
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
import shap
import matplotlib.pyplot as plt  # Import matplotlib for plotting

# Load the pre-trained model
model_path = r"C:\Users\aozor\Documents\KI\semester 3\course 8\GlucoGuard_Analytics\jupyter-notebooks\best_model.pkl"
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Define the categorical mappings globally
cats = {
    'age': ['[0-10)', '[10-20)', '[20-30)', '[30-40)', '[40-50)', 
            '[50-60)', '[60-70)', '[70-80)', '[80-90)', '[90-100)'],
    'max_glu_serum_transformed': ['Not measured', 'Normal', 'Elevated', 'High'],
    'A1Cresult_transformed': ['Not measured', 'Normal', 'High'],
    'race': ['Caucasian', 'African American', 'Hispanic', 'Asian', 'Other'],  
    'gender': ['Male', 'Female'],  
    'change': ['No', 'Yes'],  
    'diabetesMed': ['No', 'Yes']  
}

# Function to preprocess input data
def preprocess_input(data):
    # Create a DataFrame from user input
    df_input = pd.DataFrame(data, index=[0])

    # Apply ordinal encoding
    for col in df_input.columns:
        if col in cats:
            df_input[col] = pd.Categorical(df_input[col], categories=cats[col], ordered=True)
            df_input[col] = df_input[col].cat.codes

    # Grouping medications
    for med in ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 
                'glimepiride', 'acetohexamide', 'glipizide', 'glyburide', 
                'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose', 
                'miglitol', 'troglitazone', 'tolazamide', 'examide', 
                'citoglipton', 'insulin', 'glyburide-metformin', 
                'glipizide-metformin', 'glimepiride-pioglitazone', 
                'metformin-rosiglitazone', 'metformin-pioglitazone']:
        df_input[med] = 1 if df_input[med].values[0] == 'Yes' else 0

    # Additional grouping logic 
    df_input['SU'] = df_input[['chlorpropamide', 'glimepiride', 
                                'acetohexamide', 'glipizide', 
                                'glyburide', 'tolbutamide', 
                                'tolazamide']].max(axis=1)
    df_input['mitiglinides'] = df_input[['repaglinide', 'nateglinide']].max(axis=1)
    df_input['thiazolidinediones'] = df_input[['pioglitazone', 'rosiglitazone']].max(axis=1)
    df_input['glucosidase_inh'] = df_input[['acarbose','miglitol']].max(axis=1)

    # Drop original medication columns
    df_input.drop(columns=['chlorpropamide', 'glimepiride', 'acetohexamide', 
                           'glipizide', 'glyburide', 'tolbutamide', 
                           'tolazamide', 'repaglinide', 'nateglinide', 
                           'pioglitazone', 'rosiglitazone', 'acarbose', 
                           'miglitol'], inplace=True, errors='ignore')

    # Selecting numerical features
    num_f = df_input[['time_in_hospital', 'num_lab_procedures', 
                      'num_procedures', 'num_medications']]
    
    # One-hot encoding of nominal features
    nominal_features = [col for col in ['race', 'gender', 'change', 'diabetesMed'] if col in df_input.columns]
    if nominal_features:
        nominal_f = pd.get_dummies(df_input[nominal_features])
    else:
        nominal_f = pd.DataFrame()  # Create an empty DataFrame if no nominal features are present
    
    # Concatenate all features
    X_all = pd.concat([nominal_f, num_f, df_input], axis=1)

    # Normalizing the features
    scaler = MinMaxScaler()
    X_normalized = scaler.fit_transform(X_all.values)
    
    return pd.DataFrame(X_normalized, columns=X_all.columns)

# Function for SHAP analysis
def perform_shap_analysis(X):
    # Create a SHAP explainer
    explainer = shap.Explainer(model)

    # Calculate SHAP values
    shap_values = explainer(X)

    return shap_values, explainer  # Return both shap_values and explainer

# Streamlit UI
st.title("Diabetes Readmission Prediction")

# User inputs
age = st.selectbox("Age Group:", options=cats['age'])
max_glu = st.selectbox("Max Glucose Serum:", options=cats['max_glu_serum_transformed'])
A1C = st.selectbox("A1C Result:", options=cats['A1Cresult_transformed'])
time_in_hospital = st.number_input("Time in Hospital (days):", min_value=1, max_value=365)
num_lab_procedures = st.number_input("Number of Lab Procedures:", min_value=0, max_value=100)
num_procedures = st.number_input("Number of Procedures:", min_value=0, max_value=100)
num_medications = st.number_input("Number of Medications:", min_value=1, max_value=100)

# User input for medications
medications = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 
               'glimepiride', 'acetohexamide', 'glipizide', 'glyburide', 
               'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose', 
               'miglitol', 'troglitazone', 'tolazamide', 'examide', 
               'citoglipton', 'insulin', 'glyburide-metformin', 
               'glipizide-metformin', 'glimepiride-pioglitazone', 
               'metformin-rosiglitazone', 'metformin-pioglitazone']

med_input = {med: st.selectbox(f"{med.capitalize()} (Yes/No):", ["Yes", "No"]) for med in medications}

# User inputs for categorical variables
race = st.selectbox("Race:", options=cats['race'])
gender = st.selectbox("Gender:", options=cats['gender'])
change = st.selectbox("Change in Medication:", options=cats['change'])
diabetesMed = st.selectbox("Diabetes Medication:", options=cats['diabetesMed'])

# Convert input to dictionary
user_input = {
    'age': age,
    'max_glu_serum_transformed': max_glu,
    'A1Cresult_transformed': A1C,
    'time_in_hospital': time_in_hospital,
    'num_lab_procedures': num_lab_procedures,
    'num_procedures': num_procedures,
    'num_medications': num_medications,
    'race': race,
    'gender': gender,
    'change': change,
    'diabetesMed': diabetesMed,
    **med_input
}

# Button to make predictions and perform SHAP analysis
if st.button("Predict Readmission"):
    # Preprocess the user input
    processed_input = preprocess_input(user_input)

    # Make prediction
    prediction = model.predict(processed_input)

    # Output result
    st.success("Prediction: {}".format("Readmitted" if prediction[0] == 1 else "Not Readmitted"))

    # Perform SHAP analysis
    shap_values, explainer = perform_shap_analysis(processed_input)

    # SHAP summary plot
    st.subheader("SHAP Summary Plot")
    fig, ax = plt.subplots()  # Create a new figure and axis
    shap.summary_plot(shap_values, feature_names=processed_input.columns, show=False)
    st.pyplot(fig)  # Pass the figure to st.pyplot

    # SHAP force plot for the first prediction
    st.subheader("SHAP Force Plot")
    fig2, ax2 = plt.subplots()  # Create another figure for the force plot
    # Pass the correct values to the force plot
    shap.force_plot(explainer.expected_value, shap_values.values[0], processed_input.values[0], matplotlib=True, show=False)
    st.pyplot(fig2)  # Pass the figure to st.pyplot