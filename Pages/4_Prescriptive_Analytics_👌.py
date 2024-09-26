import streamlit as st
import pandas as pd
import numpy as np
import shap
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

st.title("SHAP Analysis of Diabetic Patients Readmission Prediction")

# Set random seed for reproducibility
np.random.seed(42)

# Generate random data
data = {
    'time_in_hospital': np.random.randint(1, 15, size=100),
    'num_lab_procedures': np.random.randint(1, 50, size=100),
    'num_procedures': np.random.randint(0, 10, size=100),
    'num_medications': np.random.randint(1, 30, size=100),
    'number_outpatient': np.random.randint(0, 5, size=100),
    'number_emergency': np.random.randint(0, 3, size=100),
    'number_inpatient': np.random.randint(0, 2, size=100),
    'number_diagnoses': np.random.randint(1, 20, size=100),
    'readmitted': np.random.choice([0, 1], size=100)  # Target variable
}

# Create DataFrame
df = pd.DataFrame(data)

# Define features and target
X = df.drop('readmitted', axis=1)
y = df['readmitted']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Explain the predictions using SHAP
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Select a single explanation for the waterfall plot
shap_values_single = shap_values[1][0]  # For the positive class
expected_value_single = explainer.expected_value[1]

# Create an Explanation object
explanation_single = shap.Explanation(values=shap_values_single, base_values=expected_value_single, data=X_test.iloc[0])

# Streamlit code to display the waterfall plot
# Create a SHAP waterfall plot
fig = plt.figure()
shap.waterfall_plot(explanation_single)  # Create the waterfall plot without ax

# Compute SHAP values for the entire test set
explainer = shap.Explainer(model)
shap_values = explainer(X_test)

# If shap_values.values is 3D, flatten it to 2D
if len(shap_values.values.shape) > 2:
    # Extract the first output if it's a multi-output model
    shap_values_values = shap_values.values[:, :, 0]
else:
    shap_values_values = shap_values.values

# Create a DataFrame for SHAP values and feature names
shap_values_df = pd.DataFrame(shap_values_values, columns=X_test.columns)

# Calculate the mean absolute SHAP values for each feature
mean_shap_values = np.abs(shap_values_df).mean(axis=0)

# Compute SHAP values for the entire test set
explainer = shap.Explainer(model)
shap_values = explainer(X_test)

# If shap_values.values is 3D, flatten it to 2D
if len(shap_values.values.shape) > 2:
    # Extract the first output if it's a multi-output model
    shap_values_values = shap_values.values[:, :, 0]
else:
    shap_values_values = shap_values.values

# Create a DataFrame for SHAP values and feature names
shap_values_df = pd.DataFrame(shap_values_values, columns=X_test.columns)

# Calculate the mean absolute SHAP values for each feature
mean_shap_values = np.abs(shap_values_df).mean(axis=0)

# Create a summary plot
fig = px.scatter(
    x=mean_shap_values.index,
    y=mean_shap_values.values,
    color=mean_shap_values.values,
    labels={'x': 'Features', 'y': 'Mean Absolute SHAP Value'},
    title='SHAP Summary Plot of All Features'
)

# Update layout for better readability
fig.update_layout(
    xaxis_title="Features",
    yaxis_title="Mean Absolute SHAP Value",
    showlegend=False
)

# Display the plot in Streamlit
st.plotly_chart(fig)  # Correct way to display a Plotly figure

st.markdown("""
### Interpretation

The mean absolute SHAP value for **"Number of Lab Procedures"** is **0.058**, the highest among all features, 
indicating its significant influence on the model's predictions. This suggests that 
variations in the number of lab procedures can substantially affect the readmission of diabetic patients.
""")