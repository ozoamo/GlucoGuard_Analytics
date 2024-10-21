import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import numpy as np
from scipy.stats import chi2_contingency

# Load your data
df = pd.read_csv("diabetes_clean.csv")

st.set_page_config(
    page_title="GlucoGuard Dashboard",
    page_icon="./assets/Page-icon.png",
)
st.sidebar.image("./assets/glucoguard-logo.png",)

# Set the title of the Streamlit app
st.title("Glucoguard Diagnostic Dashboard")

# Heatmap for Correlation between numerical features and readmission
st.header("Correlation between Readmission and Other Features")

# Binarize some categorical features
df['readmitted'] = df['readmitted'].apply(lambda x: 0 if x == 'NO' else 1)
df['metformin'] = df['metformin'].apply(lambda x: 0 if x == 'No' else 1)
df['insulin'] = df['insulin'].apply(lambda x: 0 if x == 'No' else 1)
df['change'] = df['change'].apply(lambda x: 0 if x == 'No' else 1)
df['gender'] = df['gender'].apply(lambda x: 1 if x == 'Male' else 0)

# Convert 'age' ranges to the midpoint of the range
age_map = {
    "[0-10)": 5,
    "[10-20)": 15,
    "[20-30)": 25,
    "[30-40)": 35,
    "[40-50)": 45,
    "[50-60)": 55,
    "[60-70)": 65,
    "[70-80)": 75,
    "[80-90)": 85,
    "[90-100)": 95
}
df['age'] = df['age'].map(age_map)

# Select only numerical columns
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns

# Exclude specific features
excluded_features = ['patient_nbr', 'encounter_id']
numerical_cols = [col for col in numerical_cols if col not in excluded_features]

# Ensure 'readmitted' is part of the selected features
if 'readmitted' not in df.columns:
    st.error("The 'readmitted' feature is not in the dataset. Please check your data.")
else:
    # Add a multiselect widget for the user to choose the numerical features (excluding 'readmitted' and excluded features)
    selected_features = st.multiselect(
        'Select numerical features for the heatmap:',
        options=numerical_cols,
        default=[]  # Default to no additional features selected
    )

    # Always include 'readmitted' in the selected features
    selected_features.append('readmitted')

    # Check if at least two features are selected
    if len(selected_features) < 2:
        st.warning("Please select at least one numerical feature to display the correlation heatmap.")
    else:
        # Calculate the correlation matrix based on selected features
        corr_matrix = df[selected_features].corr()

        # Create a heatmap using Plotly with 2 decimal precision for annotations
        z = corr_matrix.values
        annotations = [[f"{value:.2f}" for value in row] for row in z]  # Format values to 2 decimal places

        fig = ff.create_annotated_heatmap(
            z=z,
            x=corr_matrix.columns.tolist(),
            y=corr_matrix.columns.tolist(),
            colorscale='RdBu',
            showscale=True,
            annotation_text=annotations,  # Use formatted annotations
            textfont=dict(color='black')  # Set text color for visibility
        )

        # Display the interactive heatmap
        st.plotly_chart(fig)

        # Display the correlation values with readmitted
        readmitted_correlation = corr_matrix['readmitted'].drop('readmitted')  # Exclude self-correlation
        correlation_values = readmitted_correlation.reset_index()
        correlation_values.columns = ['Feature', 'Correlation with Readmitted']
        
        # Key points section
        st.write("### Key Points")
        st.markdown("""
        1. None of the features have a strong correlation with readmission.
        2. The number of inpatient visits has the strongest correlation with readmission (0.2), 
            indicating that patients with more inpatient visits are more likely to be readmitted.
        3. The feature with the weakest correlation with readmission is the admission type ID, 
            which indicates the department from which the patient was admitted, 
            such as the emergency department, urgent care, or elective care, 
            with a correlation value of -0.01.
        """)

# Chi square analysis for categorical features
st.header("Chi-Square Analysis for Categorical Features with Readmission")
st.markdown("""
The Chi-Square test evaluates whether there is a significant association between two categorical variables. 
A low p-value (typically < 0.05) indicates that we can reject the null hypothesis of independence, 
suggesting a significant relationship between the variables.
""")

# Function to perform Chi-Square Test and collect results
def chi_square_test(var1, var2):
    if df[var1].dtype.kind in 'bi' and df[var2].dtype.kind in 'bi':
        contingency_table = pd.crosstab(df[var1], df[var2])
        chi2, p, dof, expected = chi2_contingency(contingency_table)
        return chi2, p, dof, contingency_table
    else:
        st.error(f"Error: Both variables must be categorical for Chi-square test")
        return None, None, None, None

# User selects a feature for Chi-Square test
selected_feature = st.selectbox("Select a categorical feature to analyze with 'readmitted':", 
                                 options=['metformin', 'insulin', 'change', 'gender'])

# Perform Chi-Square test for the selected feature
chi2, p, dof, contingency_table = chi_square_test('readmitted', selected_feature)

# Calculate Pearson Correlation Coefficients
pearson_results = {
    'Feature': ['metformin', 'insulin', 'change', 'gender'],
    'Pearson Correlation Coefficient': [
        df['readmitted'].corr(df['metformin']),
        df['readmitted'].corr(df['insulin']),
        df['readmitted'].corr(df['change']),
        df['readmitted'].corr(df['gender'])
    ]
}

# Store Chi-Square test results in a DataFrame
chi_square_results = {
    'Feature': selected_feature,
    'Chi-Square Statistic': chi2,
    'p-value': p,
    'Degrees of Freedom': dof,
}

# Combine results into a single DataFrame
combined_results = pd.DataFrame(pearson_results)
chi_square_df = pd.DataFrame([chi_square_results])
combined_results = combined_results.merge(chi_square_df, on='Feature')

# Display the combined results in Streamlit
st.markdown("### Comparison of Correlation and Chi-Square Test")
st.write(combined_results)

# Results Interpretation
st.markdown("### Key Point")
st.markdown("""
While the Pearson correlations for metformin, insulin, change, and gender with readmission are weak, 
the Chi-square tests show **significant associations**. This implies that these 
variables have a significant relationship with whether a patient is readmitted, 
even though their linear relationships are minimal.
""")
