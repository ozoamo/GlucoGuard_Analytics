import streamlit as st


st.set_page_config(
    page_title="GlucoGuard Dashboard",
    
    #page_icon="👋",
     page_icon="./assets/Page-icon.png",
)

# Sidebar configuration
st.sidebar.image("./assets/glucoguard-logo.png",)
#st.sidebar.success("Select a tab above.")

# # Page information

st.write("# Welcome to GlucoGuard! 👋")
st.write("## Empowering Healthcare Professionals with Data-Driven Insights.")

st.image("./assets/GIF.gif",  use_column_width=True)




st.markdown("""
Diabetes is a chronic condition characterized by either insufficient insulin production (Type 1) or the body's inability to effectively use insulin to regulate glucose levels (Type 2). 

Approximately **0.2%** of all 30-day hospital readmissions involve patients with diabetes mellitus (DM)【1】. Factors that increase the risk of readmission include:
- Comorbidities
- Repeated readmissions
- Demographic factors
- Length of stay【3】

Reducing hospital readmissions can improve healthcare outcomes while also lowering healthcare costs【2】.

This web dashboard aims to provide valuable information regarding readmission rates for diabetes 
patients, particularly for healthcare professionals such as physicians, nurses, and pharmacists.
""")
