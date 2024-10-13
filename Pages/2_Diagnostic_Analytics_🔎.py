import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv('diabetes_clean.csv')

# Streamlit app
st.title("Correlation Analysis between Numerical Variables")

# List of variables for dropdown menus
variables = ['time_in_hospital', 'num_lab_procedures', 'num_procedures', 
             'num_medications', 'number_outpatient', 'number_emergency', 
             'number_inpatient', 'number_diagnoses']

# Dropdown for selecting variables in the sidebar
st.sidebar.header("Select Variables for Pearson Correlation Analysis")
var1 = st.sidebar.selectbox('Select first variable:', variables)
var2 = st.sidebar.selectbox('Select second variable:', variables)

# Check if the variables are the same
if var1 == var2:
    st.warning('Please select two different variables.')
else:
    # Create two columns for layout
    col1, col2 = st.columns(2)

    with col1:
        # Plot linear regression
        st.write(f"Correlation between **{var1}** and **{var2}**")
        fig, ax = plt.subplots()
        sns.regplot(x=df[var1], y=df[var2], ax=ax, line_kws={"color": "red"})
        ax.set_xlabel(var1)
        ax.set_ylabel(var2)
        st.pyplot(fig)

        # Calculate Pearson correlation coefficient
        corr_coeff, _ = pearsonr(df[var1], df[var2])
        st.write(f"Pearson correlation coefficient: **{corr_coeff:.2f}**")

    with col2:
        # Key insights
        st.markdown("""
        ### Key Insights

        1. **Hospital stays** tend to increase with more medications and procedures:
           - Time in hospital has a moderate correlation with the number of medications (**0.46**) and procedures (**0.38**). 
           - Additionally, there is a moderate correlation with lab procedures (**0.32**), suggesting that these factors may work together in managing patient care.

        2. **Outpatient and emergency visits** seem to have minimal correlation with most other variables:
           - Outpatient visits have a correlation range of approximately **-0.011 to 0.091**.
           - Emergency visits show a correlation range of about **-0.039 to 0.27**.
        """)
