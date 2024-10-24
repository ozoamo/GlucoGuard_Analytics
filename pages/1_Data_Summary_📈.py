import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
df_gr = df.copy()

# grouping the medications according to their pharmacological properties
meds = ['metformin', 'repaglinide','nateglinide', 'chlorpropamide', 'glimepiride','acetohexamide', 'glipizide', 
                       'glyburide', 'tolbutamide', 'pioglitazone', 'rosiglitazone','acarbose', 
                       'miglitol', 'troglitazone', 'tolazamide', 'examide', 'citoglipton', 'insulin',
                       'glyburide-metformin', 'glipizide-metformin', 'glimepiride-pioglitazone',
                       'metformin-rosiglitazone','metformin-pioglitazone']
for med in meds:
    df_gr[med] = df_gr[med].apply(lambda x: 0 if x == 'No' else 1)

df_gr['SU'] = df_gr[['chlorpropamide', 'glimepiride','acetohexamide', 'glipizide', 
                       'glyburide', 'tolbutamide', 'tolazamide']].max(axis=1)
df_gr[' meglitinides'] = df_gr[['repaglinide','nateglinide']].max(axis=1)
df_gr['thiazolidinediones'] = df_gr[['pioglitazone', 'rosiglitazone','troglitazone']].max(axis=1)
df_gr['glucosidase_inh'] = df_gr[['acarbose','miglitol']].max(axis=1)
df_gr.drop(axis=1,columns=['chlorpropamide', 'glimepiride','acetohexamide', 'glipizide', 
                       'glyburide', 'tolbutamide', 'tolazamide','repaglinide','nateglinide','pioglitazone', 'rosiglitazone',
                       'acarbose','miglitol','troglitazone'],inplace=True)
pharm_grp = ['SU',' meglitinides', 'thiazolidinediones', 'glucosidase_inh','metformin', 'insulin']


st.markdown("##### Discover how patient demographics influence readmission rates in diabetic care.")

# Decrease the size of the label text using Markdown
st.markdown("#### Select a patient characteristic to explore its distribution:")

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
        
        The data indicates that the gender with the highest number of diabetes cases is the female gender.
        """)
        
    elif selected_cat_col == 'readmitted':
        st.markdown("""
        #### Key Observation:
        
        The data indicates that almost half of the admitted patients have been admitted before.
        """)

st.markdown("## More Data Insights..")

# Define a mapping for age categories to numerical values
age_mapping = {
    '[0-10)': 5,
    '[10-20)': 15,
    '[20-30)': 25, 
    '[30-40)': 35, 
    '[40-50)': 45,
    '[50-60)': 55,
    '[60-70)': 65,
    '[70-80)': 75,
    '[80-90)': 85,
    '[90-100)': 95
}

# Map the age categories to their corresponding numeric values
df_gr['age_numeric'] = df_gr['age'].map(age_mapping)


# Melt the DataFrame
df_melted2 = pd.melt(df_gr, id_vars=['age', 'readmitted','age_numeric'], 
                    value_vars=pharm_grp, 
                    var_name='Pharmacological Group', 
                    value_name='Medication Use')

# Filter rows where Medication Use is 1 (i.e., the medication was used)
df_filtered2 = df_melted2[df_melted2['Medication Use'] == 1].copy()  # Make a copy to avoid SettingWithCopyWarning

# Set readmitted as a categorical variable using .loc
df_filtered2['readmitted_binary'] = df_filtered2['readmitted'].apply(lambda x: 0 if x == 'NO' else 1)

# Define the correct order for the age categories
age_order = ['[0-10)', '[10-20)', '[20-30)', '[30-40)', '[40-50)', '[50-60)', '[60-70)', '[70-80)', '[80-90)', '[90-100)']

# Group by readmission and calculate the average time in hospital
time_in_hospital_mean = df.groupby('readmitted')['time_in_hospital'].mean()
time_in_hospital_mean_df = time_in_hospital_mean.reset_index()

# Melt the DataFrame to reshape it for the box plot
df_melted3 = pd.melt(df_gr, id_vars=['time_in_hospital'], 
                    value_vars=pharm_grp, 
                    var_name='Pharmacological Group', 
                    value_name='Medication Use')

# Analyze readmission rates by medication change
medication_change_readmission = df.groupby('change')['readmitted'].value_counts(normalize=True).unstack()
medication_change_readmission_df = medication_change_readmission.reset_index()

# Melt the DataFrame for easier plotting with Plotly
medication_change_readmission_melted = medication_change_readmission_df.melt(id_vars='change', 
                                                                            value_vars=medication_change_readmission.columns, 
                                                                            var_name='readmitted', 
                                                                            value_name='proportion')

# Filter rows where Medication Use is 1 (i.e., the medication was used)
df_filtered3 = df_melted3[df_melted3['Medication Use'] == 1]

# Create a dropdown menu to select which plot to display
plot_option = st.selectbox(
    'Select the plot you want to display:',
    ('Distribution of Age by Medication Group Usage', 
     'Distribution of Age by Readmission Status', 
     'Average Time in Hospital by Readmission Status', 
     'Time in Hospital by Medication Group Usage', 
     'Readmission Rates by Medication Change')
)

# Conditional logic to display the selected plot and its explanation
if plot_option == 'Distribution of Age by Medication Group Usage':
    # Create the violin plot
    figv = px.violin(df_filtered2, 
                    x='Pharmacological Group', 
                    y='age_numeric', 
                    color='readmitted_binary', 
                    title='',
                    category_orders={'age': age_order},  # Order age categories
                    color_discrete_sequence=px.colors.qualitative.Set1,
                    labels={
                     'Pharmacological Group': 'Antidiabetic Medication Group',  # Custom x-axis title
                     'age_numeric': 'Age (Years)',  # Custom y-axis title
                     'readmitted_binary': ''  # Legend label for color
                 }
                    )
    figv.update_layout(
        width=1200,  # Set plot width
        height=470,  # Set plot height
        xaxis_tickangle=-45,  # Rotate x-axis labels for readability
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",  # Align legend to the bottom
            y=1.02,  # Push legend up
            xanchor="center",  # Center the legend
            x=0.5  # Set legend position
            )
        )
    figv.update_traces(width=0.9)
    figv.for_each_trace(lambda trace: trace.update(name='Readmitted' if trace.name == '1' else 'Not Readmitted'))

    # Create two columns for side-by-side display
    col1, col2 = st.columns(2)

    # Display the plot in the first column 
    with col1:
        st.plotly_chart(figv, use_container_width=True)

    # Display the interpretations in the second column
    with col2:
        st.markdown("""
        #### Key Observations:
        
        1. The data shows that patients who received glucosidase inhibitors were less likely to be readmitted regardless of their age.  
        2. Older patients (70-80 years of age) on sulfonylureas were more likely to be readmitted than younger patients. This endorses current knowledge of the risk of hypoglycemia in the elderly receiving this type of medication [5].
        """)

elif plot_option == 'Distribution of Age by Readmission Status':
    plt.figure(figsize=(8, 4))
    sns.histplot(data=df, x='age', hue='readmitted', bins=20, kde=True)
    plt.xlabel('Age', fontsize=12)
    plt.ylabel('Count', fontsize=12)

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(plt)

    with col2:
        st.markdown("""
        #### Key Observations:
        
        1. The data shows that elderly patients (> 60 years) were more likely to be readmitted than younger patients.  
        2. Most readmissions occurred after more than 30 days of the last admission.
        3. More than two-thirds of elderly patients were readmitted after their preceding hospitalization.
        """)

elif plot_option == 'Average Time in Hospital by Readmission Status':
    # Bar plot
    fig_2 = px.bar(time_in_hospital_mean_df, 
                   x='readmitted', 
                   y='time_in_hospital', 
                   title='',
                   labels={'readmitted': 'Readmitted (<30: short-term readmission, >30: long-term readmission, NO: No readmission)', 
                           'time_in_hospital': 'Average Time in Hospital (Days)'},
                   color_discrete_sequence=['skyblue'])
    
    fig_2.update_layout(width=1000, height=400)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_2)

    with col2:
        st.markdown("""
        #### Key Observations:

        1. Patients who have not been previously admitted have the shortest average hospital stay, which may be attributed to their relatively well-controlled diabetes that doesn't necessitate prolonged hospitalization.
        2. Patients readmitted within 30 days of their previous admission have the longest average hospital stay, possibly due to recent changes in their medications or treatment plans after the last discharge.
        """)

elif plot_option == 'Time in Hospital by Medication Group Usage':
    # Create the box plot
    figbx = px.box(df_filtered3,  
                   x='Pharmacological Group', 
                   y='time_in_hospital', 
                   title='',
                   labels={'time_in_hospital': 'Time in Hospital (Days)', 
                           'Pharmacological Group': 'Antidiabetic Medication Group'})  

    figbx.update_layout(width=1000, height=400)
    figbx.update_layout(xaxis_tickangle=-45)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(figbx, use_container_width=True)

    with col2:
        st.markdown("""
        #### Key Observations:
        1. The data show that most medications had similar box plots. This may be due to drug combinations, as diabetic patients rarely receive only one type of medication.
        2. Meglitinides lead to slightly longer hospital stays than other drugs; however, the median aligns with the medians of the other plots, indicating that this difference may not be significant. 
        """)

elif plot_option == 'Readmission Rates by Medication Change':
    # Create the bar plot
    fig_3 = px.bar(medication_change_readmission_melted, 
                   x='change', 
                   y='proportion', 
                   color='readmitted', 
                   title='',
                   labels={'change': 'Medication Change', 
                           'proportion': 'Proportion of Readmissions'},
                   color_discrete_sequence=['skyblue', 'salmon', 'lightgreen'],
                   barmode='stack')

    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(fig_3)

    with col4:
        st.markdown("""
        #### Key Observations:

        1. The proportion of patients readmitted after a recent medication change is slightly larger than those without any changes in their medications. Nearly half of the readmissions occurred following a recent adjustment in medications.
        2. However, almost half of the patients were readmitted regardless of whether their medications had recently been changed. This suggests that other factors clearly play a role in diabetes management and, consequently, the need for hospital admission and urgent medical care.
        """)