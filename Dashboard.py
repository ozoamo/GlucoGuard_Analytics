import streamlit as st

st.set_page_config(
    page_title="GlucoGuard Dashboard",
    
    #page_icon="👋",
     page_icon="./assets/Page-icon.png",
)

# Sidebar configuration
st.sidebar.image("./assets/glucoguard-logo.png",)
st.sidebar.success("Select a tab above.")

# # Page information

st.write("# Welcome to GlucoGuard! 👋")

st.markdown(
"""
    Diabetes is a chronic condition, where either not enough insulin is being produced or the body(Type 1) is not able to use insulin to stabilise the glucose levels(Type 2). About 0.2% of all 30-day hospital readmissions consists on patients with diabetes mellitus(DM)[1]. Factors that increase the risk of being readmitted include comorbidities, repeated readmissions, demographics and length of stay[3].  By reducing hospital readmissions there is a potential of improving healthcare whilst reducing the healthcare costs[2]. 
    
    The web dashboard will provide the end user(healthcare professionals(Physicians, Nurses, Dieticians), Patients, healthcare providers and hospital management) with information concerning the readmission rates for diabetes patients. 


    
"""
)

# You can also add text right into the web as long comments (""")






### UNCOMMENT THE CODE BELOW TO SEE EXAMPLE OF INPUT WIDGETS

# DATAFRAME MANAGEMENT
