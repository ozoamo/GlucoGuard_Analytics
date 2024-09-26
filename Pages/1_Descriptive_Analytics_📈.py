import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


st.write("# Descriptive Analytics #")

# Load the dataset
df = pd.read_csv('diabetes_clean.csv')

# Title p
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
categorical_columns = ['age', 'race', 'gender','readmitted']

# Dropdown for selecting a categorical variable
selected_cat_col = st.sidebar.selectbox('Select a categorical column:', categorical_columns)

# Plot the distribution of the selected categorical column
st.write(f"## Distribution of cases of diabetes based on `{selected_cat_col}`")

# Count the values in the selected column
cat_value_counts = df[selected_cat_col].value_counts().reset_index()
cat_value_counts.columns = [selected_cat_col, 'Count']

# Create a bar chart using Plotly
fig = px.bar(cat_value_counts, x=selected_cat_col, y='Count', 
             title=f"Distribution of {selected_cat_col}",
             labels={selected_cat_col: selected_cat_col, 'Count': 'Prevalence'},
             template="plotly_white")

# Display the plot 
st.plotly_chart(fig)

st.markdown("""
### Key Observations:

1.  **Age**: The data indicates age group with the highest amount of cases of diabetes is the age group between 70-80 years.The lowest amount of cases of diabetes is the age group 0-10 years old. An intresting trend that can seen is as an individual gets older,the risk of getting diabetes increases.
            
2. **Race(Ethnicity)**: The data indicates that the ethnicity with the highest amount of cases of diabetes are Caucasian.

3. **Gender**: The data indicates that the gender with the highest amount of cases of diabetes is female.

4. **Readmitted**: The data indicates that the highest amount of readmitted patients were the age of 30 or above.
            
""")

# Title 
st.subheader('Age distribution - Histogram')

# Extract the 'age' column for the histogram
age_counts = df['age'].value_counts().reset_index()
age_counts.columns = ['age', 'count']

# Sort age groups if they are in categorical ranges
age_counts = age_counts.sort_values('age')

# Plotly histogram
fig_1 = px.bar(age_counts, x='age', y='count', 
             title='Age Distribution in Dataset',
             labels={'age': 'Age Range', 'count': 'Frequency'},
             template='plotly_white')

# Display the histogram 
st.plotly_chart(fig_1)

