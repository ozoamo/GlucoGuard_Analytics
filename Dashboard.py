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

st.markdown("""
Diabetes is a chronic condition characterized by either insufficient insulin production (Type 1) or the body's inability to effectively use insulin to regulate glucose levels (Type 2). 

Approximately **0.2%** of all 30-day hospital readmissions involve patients with diabetes mellitus (DM)【1】. Factors that increase the risk of readmission include:
- Comorbidities
- Repeated readmissions
- Demographic factors
- Length of stay【3】

Reducing hospital readmissions can improve healthcare outcomes while also lowering healthcare costs【2】.

This web dashboard provides valuable insights into the factors influencing the readmission of diabetes patients, 
designed specifically for healthcare professionals such as physicians, nurses, and pharmacists.

Please watch the video below to learn more about the functionality offered in this web dashboard.
""")

# Embed a video from a local file
video_file = open('./assets/WhatsApp Video 2024-10-23 at 01.43.43_f39b376a.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)