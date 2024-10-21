import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="GlucoGuard Dashboard",
    page_icon="./assets/Page-icon.png",
)
st.sidebar.image("./assets/glucoguard-logo.png",)

# Title
st.title('Glucoguard Descriptive Analytics')

# Load the dataset
df = pd.read_csv('diabetes_clean.csv')

# Plot categorical distribution
#st.write("## Categorical Variable Distribution")
# Sidebar for user selection
#st.sidebar.header('Select a Categorical Variable')

st.markdown("##### Discover how patient demographics influence readmission rates in diabetic care.")


# Decrease the size of the label text using Markdown
st.markdown("#### Select a patient characteristic to explore readmission trends:")


# Add the dropdown directly in the middle of the page (no columns)
#categorical_columns = ['age', 'race', 'gender', 'readmitted']



# Add the selectbox without columns
#selected_cat_col = st.selectbox('', categorical_columns)


# Count the values in the selected column
#cat_value_counts = df[selected_cat_col].value_counts().reset_index()
#cat_value_counts.columns = [selected_cat_col, 'Count']

# Create a bar chart using Plotly
#fig = px.bar(cat_value_counts, x=selected_cat_col, y='Count', 
           # title=f"Distribution of {selected_cat_col}",
            #labels={selected_cat_col: selected_cat_col, 'Count': 'Number of Cases'},
            #template="plotly_white")

# Display the plot 
#st.plotly_chart(fig)


# Define the original list of categorical columns
original_columns = ['age', 'race', 'gender', 'readmitted']

# Create a capitalized version for display in the dropdown
display_columns = [col.capitalize() for col in original_columns]

# Create a mapping between display names and actual column names
column_mapping = dict(zip(display_columns, original_columns))

# Add the selectbox without columns
selected_display_col = st.selectbox('Select a patient characteristic:', display_columns)

# Map the selected display name back to the original column name
selected_cat_col = column_mapping[selected_display_col]

# Plot the distribution of the selected categorical column
cat_value_counts = df[selected_cat_col].value_counts().reset_index()
cat_value_counts.columns = [selected_cat_col, 'Count']

# Create a bar chart using Plotly
fig = px.bar(cat_value_counts, x=selected_cat_col, y='Count', 
             title=f"Distribution of {selected_display_col}",
             labels={selected_cat_col: selected_display_col, 'Count': 'Number of Cases'},
             template="plotly_white")

# Display the plot 
st.plotly_chart(fig)


#st.markdown("""
### Key Observations:

#1.  **Age**: The data indicates age group with the highest amount of cases of diabetes is the age group between 70-80 years.The lowest amount of cases of diabetes is the age group 0-10 years old. An intresting trend that can seen is as an individual gets older,the risk of getting diabetes increases.
            
#2. **Race(Ethnicity)**: The data indicates that the ethnicity with the highest amount of cases of diabetes are Caucasian.

#3. **Gender**: The data indicates that the gender with the highest amount of cases of diabetes is female.

#4. **Readmitted**: The data indicates that the highest amount of readmitted patients were the age of 30 or above.
            
#""")
# Display key observations based on the selected category
if selected_cat_col == 'age':
    st.markdown("""
    #### Key Observations for Age:
    
    1. The data indicates that the age group with the highest number of diabetes cases is between 70-80 years.
    2. The lowest number of diabetes cases is in the age group 0-10 years.
    3. As individuals get older, the risk of developing diabetes increases.
    """)
    
elif selected_cat_col == 'race':
    st.markdown("""
    #### Key Observations for Race (Ethnicity):
    
    1. The data indicates that the ethnicity with the highest number of diabetes cases is Caucasian.
    """)
    
elif selected_cat_col == 'gender':
    st.markdown("""
    #### Key Observations for Gender:
    
    1. The data indicates that the gender with the highest number of diabetes cases is female.
    """)
    
elif selected_cat_col == 'readmitted':
    st.markdown("""
    #### Key Observations for Readmitted Patients:
    
    1. The data indicates that the most of the admissions are not readmissions.
    """)


st.markdown("<h2 style='color: #1f77b4; font-size:24px; margin-top: 30px;'>Other Main Observations</h2>", unsafe_allow_html=True)
# Group by readmission and calculate the average time in hospital
time_in_hospital_mean = df.groupby('readmitted')['time_in_hospital'].mean()

# Convert the result to a DataFrame for Plotly
time_in_hospital_mean_df = time_in_hospital_mean.reset_index()

# Plotting the average time in hospital by readmission status using Plotly
fig_2 = px.bar(time_in_hospital_mean_df, 
             x='readmitted', 
             y='time_in_hospital', 
             title='Average Time in Hospital by Readmission Status',
             labels={'readmitted': 'Readmitted(<30: short-term readmission, >30:long-term readmission, NO: No readmission)', 'time_in_hospital': 'Average Time in Hospital (Days)'},
             color_discrete_sequence=['skyblue'])

# Streamlit component to display the plot
st.plotly_chart(fig_2)





st.markdown("""
##### Interpretations:

1. The highest average time by readmission status were <30(Short term readmission). The reason to why <30(Short term readmission) had the highest average time could be possibly due to ineffective treatments(changes in medication). This could be the cause to the high probability of being readmitted for short term treatments.

2. The lowest average time by readmission status were NO(no readmission). This may be due to proper treatment and fewer adverse effect, which could be the main cause behind the low probability of being readmitted for a long time.

3. Patients readmitted within 30 days have the longest average hospital stay, likely due to possible ineffective treatment or medication changes.

4.Non-readmitted patients have the shortest stays, potentially indicating effective treatments with fewer adverse effects.    
        """)

# Analyze readmission rates by medication change
medication_change_readmission = df.groupby('change')['readmitted'].value_counts(normalize=True).unstack()

# Convert the results to a DataFrame for Plotly
medication_change_readmission_df = medication_change_readmission.reset_index()

# Melt the DataFrame for easier plotting with Plotly
medication_change_readmission_melted = medication_change_readmission_df.melt(id_vars='change', 
                                                                            value_vars=medication_change_readmission.columns, 
                                                                            var_name='readmitted', 
                                                                            value_name='proportion')

# Plotting the results using Plotly
fig_3 = px.bar(medication_change_readmission_melted, 
             x='change', 
             y='proportion', 
             color='readmitted', 
             title='Readmission Rates by Medication Change',
             labels={'change': 'Medication Change', 'proportion': 'Proportion of Readmissions'},
             color_discrete_sequence=['skyblue', 'salmon', 'lightgreen'],
             barmode='stack')

# Streamlit component to display the plot
st.plotly_chart(fig_3)

st.markdown("""
##### Interpretations:

1. The high proportion of NO(No readmission) patient recieving no medication changes may suggest that possibly the patient complience may be the cause behind the high proportion rate of NO (No readmission) patients reciving no changes in their medication.

2. The high proportion of >30(long-term readmitted) recieving medication changes may suggest that possibly the ineffective treatments of the long-term readmitted patients may be the cause behind the high proportion of long-term readmitted patients receviing medication changes.  
            
""")