import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


st.write("# Descriptive Analytics #")

# Load the dataset
df = pd.read_csv('diabetes_clean.csv')

# Title of the Streamlit app
st.title('Descriptive Analytics of Diabetes Dataset')

# Sidebar for user selection
columns = df.select_dtypes(include=['int64', 'float64']).columns
selected_column = st.sidebar.selectbox('Select a column for descriptive analysis:', columns)

# Calculate descriptive statistics
mean = df[selected_column].mean()
median = df[selected_column].median()
mode = df[selected_column].mode()[0]  # Take the first mode if there are multiple

# Display results
st.write(f"### Descriptive Analytics for `{selected_column}`")
st.write(f"**Mean**: {mean}")
st.write(f"**Median**: {median}")
st.write(f"**Mode**: {mode}")

st.markdown("""
### Key Observations:

1. **Race**: The correlation coefficient is **0.003**, indicating a very weak positive correlation. This suggests that patients who stay longer in the hospital do not significantly undergo more laboratory procedures.

2. **Age**: The correlation coefficient is **0.15**, reflecting a weak positive correlation. This may suggest that patients with a higher number of diagnoses tend to receive slightly more medications, although the relationship is not strong.

3. **Gender**: The correlation coefficient is **-0.27**, indicating a moderate negative correlation. This implies that patients who frequently visit outpatient services are less likely to require emergency care.

""")


# Plot categorical distribution
st.write("## Categorical Variable Distribution")
# Sidebar for user selection
st.sidebar.header('Select a Categorical Variable')
categorical_columns = ['age', 'race', 'gender']

# Dropdown for selecting a categorical variable
selected_cat_col = st.sidebar.selectbox('Select a categorical column:', categorical_columns)

# Plot the distribution of the selected categorical column
st.write(f"## Distribution of `{selected_cat_col}`")

# Count the values in the selected column
cat_value_counts = df[selected_cat_col].value_counts().reset_index()
cat_value_counts.columns = [selected_cat_col, 'Count']

# Create a bar chart using Plotly
fig = px.bar(cat_value_counts, x=selected_cat_col, y='Count', 
             title=f"Distribution of {selected_cat_col}",
             labels={selected_cat_col: selected_cat_col, 'Count': 'Count'},
             template="plotly_white")

# Display the plot in Streamlit
st.plotly_chart(fig)

st.markdown("""
### Key Observations:

1. **time_in_hospital and num_lab_procedures**: The correlation coefficient is **0.003**, indicating a very weak positive correlation. This suggests that patients who stay longer in the hospital do not significantly undergo more laboratory procedures.

2. **num_medications and number_diagnoses**: The correlation coefficient is **0.15**, reflecting a weak positive correlation. This may suggest that patients with a higher number of diagnoses tend to receive slightly more medications, although the relationship is not strong.

3. **number_outpatient and number_emergency**: The correlation coefficient is **-0.27**, indicating a moderate negative correlation. This implies that patients who frequently visit outpatient services are less likely to require emergency care.

""")


