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
st.title("Glucoguard Diagnostic Analytics")

# Heatmap for Correlation between numerical features and readmission
st.markdown("#### Discover how different patient and clinical factors are related to the chances of readmission.")
st.header("Pearson Correlation Analysis")

st.markdown("""
The Pearson correlation coefficient measures the strength and direction of the linear relationship between two continuous variables. This statistic ranges from **-1 to 1**. 

- A value of **1** indicates a perfect **positive correlation**, meaning that as one variable increases, the other variable also increases proportionally. 
- A value of **-1** indicates a perfect **negative correlation**, where an increase in one variable results in a decrease in the other. 
- A value of **0** indicates **no linear correlation** between the variables. 
""")

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

# Mapping original column names to user-friendly labels
friendly_name_map = {
    'age': 'Age',
    'number_inpatient': 'Number of Inpatient Visits',
    'number_outpatient': 'Number of Outpatient Visits',
    'number_emergency': 'Number of Emergency Visits',
    'time_in_hospital': 'Time in Hospital',
    'num_lab_procedures': 'Number of Lab Procedures',
    'num_medications': 'Number of Medications',
    'readmitted': 'Readmitted',
    # Add more mappings as needed
}

# Reverse mapping to convert friendly names back to original column names
reverse_friendly_name_map = {v: k for k, v in friendly_name_map.items()}

# Ensure 'readmitted' is part of the selected features
if 'readmitted' not in df.columns:
    st.error("The 'readmitted' feature is not in the dataset. Please check your data.")
else:
    # Determine available options for multiselect
    options = [friendly_name_map[col] for col in numerical_cols if col in friendly_name_map]

    # Add a multiselect widget for the user to choose numerical features using friendly names
    selected_friendly_names = st.multiselect(
        '',
        options=[friendly_name_map[col] for col in numerical_cols if col in friendly_name_map],
        default=[]  # Default to no additional features selected
    )

    # Add a checkbox to select/deselect all features
    select_all = st.checkbox("Select All Features", value=False)
    
    # If "Select All Features" is checked, set default to all options, else default to none
    if select_all:
        selected_friendly_names = options

    # Map selected friendly names back to original column names
    selected_features = [reverse_friendly_name_map[name] for name in selected_friendly_names]

    # If 'readmitted' is not in the selected features, append it automatically
    if 'readmitted' not in selected_features:
        selected_features.append('readmitted')

    # Check if at least two features are selected
    if len(selected_features) < 2:
        st.info("Please select at least one feature to display the correlation heatmap.")
    else:
        # Calculate the correlation matrix based on selected features
        corr_matrix = df[selected_features].corr()

        # Create a heatmap using Plotly with 2 decimal precision for annotations
        z = corr_matrix.values
        annotations = [[f"{value:.2f}" for value in row] for row in z]  # Format values to 2 decimal places

        fig = ff.create_annotated_heatmap(
            z=z,
            x=[friendly_name_map[col] for col in corr_matrix.columns],
            y=[friendly_name_map[col] for col in corr_matrix.columns],
            colorscale='RdBu',
            showscale=True,
            annotation_text=annotations,  # Use formatted annotations
            textfont=dict(color='black')  # Set text color for visibility
        )

        # Display the interactive heatmap
        st.plotly_chart(fig)

        # Key points section
        st.write("### Interpretations")
        st.markdown("""
        1. None of the features have a strong correlation with readmission.
        2. The number of inpatient visits has the strongest correlation with readmission (0.2), 
        indicating that patients with more inpatient visits are more likely to be readmitted.
        3. The feature with the weakest correlation with readmission is age 
        with a correlation value of 0.02. The low correlation suggests that age has little 
        to no impact on the likelihood of hospital readmission for the diabetic patients.
        """)

# Chi square analysis for categorical features
st.header("Chi-Square Analysis")
st.markdown("""
The Chi-Square test evaluates whether there is a significant association between two categorical variables. 

**A low p-value** (typically < 0.05) indicates that we can reject the null hypothesis of independence, 
suggesting a **significant relationship** between the variables.
""")

# Function to perform Chi-Square Test and collect results
def chi_square_test(var1, var2):
    results = []
    for feature in var2:
        if df[var1].dtype.kind in 'bi' and df[feature].dtype.kind in 'bi':
            contingency_table = pd.crosstab(df[var1], df[feature])
            chi2, p, dof, expected = chi2_contingency(contingency_table)
            results.append((feature, chi2, p, dof, contingency_table))
        else:
            results.append((feature, None, None, None, None))  # Append None for error handling
    return results

# User selects features for Chi-Square test
features = ['metformin', 'insulin', 'change', 'gender']
selected_features = st.multiselect('',options=features)

# Place the "Select All" checkbox below the multiselect box
select_all = st.checkbox("Select All Features", value=False)

# Update selected features based on the "Select All" checkbox
if select_all:
    selected_features = features

# Only perform Chi-Square tests if at least one feature is selected
if selected_features:
    # Perform Chi-Square tests for the selected features
    chi_square_results = chi_square_test('readmitted', selected_features)

    # Calculate Pearson Correlation Coefficients for selected features
    pearson_results = {
        'Feature': [],
        'Pearson Correlation Coefficient': [],
    }

    for feature in selected_features:
        pearson_coef = df['readmitted'].corr(df[feature])
        pearson_results['Feature'].append(feature)
        pearson_results['Pearson Correlation Coefficient'].append(pearson_coef)

    # Store Chi-Square test results in a DataFrame
    chi_square_data = []
    for feature, chi2, p, dof, _ in chi_square_results:
        if chi2 is not None:  # Only add valid results
            chi_square_data.append({
                'Feature': feature,
                'Chi-Square Statistic': chi2,
                'p-value': p,
                'Degrees of Freedom': dof,
            })

    # Combine results into a single DataFrame
    chi_square_df = pd.DataFrame(chi_square_data)
    pearson_df = pd.DataFrame(pearson_results)

    # Merge results
    combined_results = pearson_df.merge(chi_square_df, on='Feature')

    # Display the combined results in Streamlit
    st.markdown("### Comparison of Correlation and Chi-Square Test")
    st.write(combined_results)

    # Results Interpretation
    st.markdown("### Interpretations")
    st.markdown("""
    While the Pearson correlations for selected features with readmission are weak, 
    the Chi-square tests show **significant associations**. This implies that these 
    variables have a significant relationship with whether a patient is readmitted, 
    even though their linear relationships are minimal.
    """)

# Optional: Display a message when no features are selected
else:
    st.info("Please select at least one feature to perform the analysis.")
