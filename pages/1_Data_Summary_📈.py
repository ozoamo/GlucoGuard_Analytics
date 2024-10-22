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

st.markdown("##### Discover how patient demographics influence readmission rates in diabetic care.")

# Decrease the size of the label text using Markdown
st.markdown("#### Select a patient characteristic to explore readmission trends:")

# Define the original list of categorical columns
original_columns = ['age', 'race', 'gender', 'readmitted']

# Create a capitalized version for display in the dropdown
display_columns = [col.capitalize() for col in original_columns]

# Create a mapping between display names and actual column names
column_mapping = dict(zip(display_columns, original_columns))

# Add the selectbox without columns
selected_display_col = st.selectbox('', display_columns)

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

# Create two columns for side-by-side display
col1, col2 = st.columns(2)

# Display the plot in the first column 
with col1:
    st.plotly_chart(fig)

# Display key observations in the second column
with col2:
    # Add space to push the text lower
    st.write("")  # You can add more empty strings for more space if needed
    st.write("")  # Adding two empty lines for spacing
    
    if selected_cat_col == 'age':
        st.markdown("""
        #### Key Observations:
        
        1. The data indicates that the age group with the highest number of diabetes cases is between 70-80 years.
        2. The lowest number of diabetes cases is in the age group 0-10 years.
        3. As individuals get older, the risk of developing diabetes increases.
        """)
        
    elif selected_cat_col == 'race':
        st.markdown("""
        #### Key Observation:
        
        The data indicates that the ethnicity with the highest number of diabetes cases is Caucasian.
        """)
        
    elif selected_cat_col == 'gender':
        st.markdown("""
        #### Key Observation:
        
        The data indicates that the gender with the highest number of diabetes cases is female.
        """)
        
    elif selected_cat_col == 'readmitted':
        st.markdown("""
        #### Key Observation:
        
        The data indicates that most of the admissions are not readmissions.
        """)

st.markdown("## Other Main Observation")

# Group by readmission and calculate the average time in hospital
time_in_hospital_mean = df.groupby('readmitted')['time_in_hospital'].mean()
time_in_hospital_mean_df = time_in_hospital_mean.reset_index()

# Plotting the average time in hospital by readmission status using Plotly
fig_2 = px.bar(time_in_hospital_mean_df, 
                x='readmitted', 
                y='time_in_hospital', 
                title='Average Time in Hospital by Readmission Status',
                labels={'readmitted': 'Readmitted (<30: short-term readmission, >30: long-term readmission, NO: No readmission)', 
                        'time_in_hospital': 'Average Time in Hospital (Days)'},
                color_discrete_sequence=['skyblue'])

# Create two columns for side-by-side display for the first plot and interpretation
col1, col2 = st.columns(2)

# Display the plot in the first column 
with col1:
    st.plotly_chart(fig_2)

# Display the interpretations in the second column
with col2:
    st.markdown("""
    ##### Key Observations:

    1. The highest average time by readmission status was short term readmission. The reason short term readmission has the highest average time could be possibly due to ineffective treatments (changes in medication).

    2. The lowest average time by readmission status was no readmission. This may be due to proper treatment and fewer adverse effects, which could be the main cause behind the low probability of being readmitted for a long time.

    3. Patients readmitted within 30 days have the longest average hospital stay, likely due to possible ineffective treatment or medication changes.
    """)

# Add a spacer between the sections
st.markdown("<br>", unsafe_allow_html=True)  # Add a line break for spacing

# Analyze readmission rates by medication change
medication_change_readmission = df.groupby('change')['readmitted'].value_counts(normalize=True).unstack()
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
                labels={'change': 'Medication Change', 
                        'proportion': 'Proportion of Readmissions'},
                color_discrete_sequence=['skyblue', 'salmon', 'lightgreen'],
                barmode='stack')

# Create two columns for side-by-side display for the second plot and interpretation
col3, col4 = st.columns(2)

# Display the second plot in the first column 
with col3:
    st.plotly_chart(fig_3)

# Display the interpretations in the second column
with col4:
    st.markdown("""
    ##### Key Observations:

    1. The high proportion of no readmission patients receiving no medication changes may suggest that possibly patient compliance may be the cause behind the high proportion rate of no readmission patients receiving no changes in their medication.

    2. The high proportion of long-term readmitted patients receiving medication changes may suggest that possibly the ineffective treatments of the long-term readmitted patients may be the cause behind the high proportion of long-term readmitted patients receiving medication changes.  
    """)