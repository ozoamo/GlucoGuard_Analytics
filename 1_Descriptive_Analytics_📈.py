import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv(r"D:\Daily file\Semester 3\Project managment\Assigment 3\GlucoGuard_Analytics\diabetes_clean.csv")


# Title of the dashboard
st.write("# Descriptive Analytics of Diabetes Dataset")

# Plot categorical distribution
st.write("## Categorical Variable Distribution")

# Sidebar for selecting a categorical variable
st.sidebar.header('Select a Categorical Variable')
categorical_columns = ['age', 'race', 'gender', 'readmitted']
selected_cat_col = st.sidebar.selectbox('Select a categorical column:', categorical_columns)

# Distribution of the selected categorical column
st.write(f"## Distribution of cases of diabetes based on `{selected_cat_col}`")
cat_value_counts = df[selected_cat_col].value_counts().reset_index()
cat_value_counts.columns = [selected_cat_col, 'Count']

# Plot the distribution using Plotly
fig = px.bar(cat_value_counts, x=selected_cat_col, y='Count', 
             title=f"Distribution of {selected_cat_col}",
             labels={selected_cat_col: selected_cat_col, 'Count': 'Prevalence'},
             template="plotly_white")
st.plotly_chart(fig)

st.markdown("""
### Key Observations:
1. **Age**: The age group with the highest number of diabetes cases is 70-80 years, while 0-10 years has the lowest.
2. **Race**: Caucasians have the highest prevalence of diabetes cases.
3. **Gender**: Female patients slightly outnumber male patients.
4. **Readmission**: Patients over 30 years old have higher readmission rates.
""")

# Age distribution - Histogram
st.subheader('Age Distribution - Histogram')
age_counts = df['age'].value_counts().reset_index()
age_counts.columns = ['age', 'count']
age_counts = age_counts.sort_values('age')  # Sort by age if categorical ranges

# Plot age distribution
fig_1 = px.bar(age_counts, x='age', y='count', 
               title='Age Distribution in Dataset',
               labels={'age': 'Age Range', 'count': 'Frequency'},
               template='plotly_white')
st.plotly_chart(fig_1)

# Average Time in Hospital by Readmission Status
time_in_hospital_mean = df.groupby('readmitted')['time_in_hospital'].mean().reset_index()

# Plotting using Plotly
fig_2 = px.bar(time_in_hospital_mean, x='readmitted', y='time_in_hospital', 
               title='Average Time in Hospital by Readmission Status',
               labels={'readmitted': 'Readmission Status', 'time_in_hospital': 'Average Time in Hospital (Days)'},
               color_discrete_sequence=['skyblue'])
st.plotly_chart(fig_2)

st.markdown("""
### Key Observations:
1. Patients readmitted within 30 days have the longest average hospital stay, likely due to possible ineffective treatment or medication changes.
2. Non-readmitted patients have the shortest stays, potentially indicating effective treatments with fewer adverse effects.
""")

# Analyze readmission rates by medication change
medication_change_readmission = df.groupby('change')['readmitted'].value_counts(normalize=True).unstack().reset_index()
medication_change_readmission_melted = medication_change_readmission.melt(id_vars='change', 
                                                                          var_name='readmitted', 
                                                                          value_name='proportion')

# Plotting the medication change readmission rates
fig_3 = px.bar(medication_change_readmission_melted, x='change', y='proportion', color='readmitted', 
               title='Readmission Rates by Medication Change',
               labels={'change': 'Medication Change', 'proportion': 'Proportion of Readmissions'},
               color_discrete_sequence=['skyblue', 'salmon', 'lightgreen'], barmode='stack')
st.plotly_chart(fig_3)

st.markdown("""
### Key Observations:
1. Patients with no medication changes generally have a lower readmission rate, suggesting potential medication compliance.
2. Long-term readmitted patients often receive medication changes, hinting that ineffective treatments may contribute to long-term readmissions.
""")
