import streamlit as st

st.set_page_config(
    page_title="GlucoGuard Dashboard",
    page_icon="./assets/Page-icon.png",
)
st.sidebar.image("./assets/glucoguard-logo.png",)

st.write("# About #")

st.markdown(""" 
    ### **Dataset**
    Sourced from the UCI Machine Learning Repository [4], the dataset used in this analysis provides extensive records of 
    diabetes patients. Comprising 50 features that encompass various aspects of patient demographics, 
    medications, and readmission rates, the dataset includes 101,765 observations.""") 

st.markdown("### **Customer Service Contact**")

# Adding a professional touch with a mailto link
contact_email = "[glucoguard_team@su.se](mailto:glucoguard_team@su.se)"
st.markdown(f"Feel free to reach out to our customer service team at {contact_email} for any inquiries or support.")

st.markdown("### **Project Developers**")

# Create a table
developers_table = """
<div style="overflow-x:auto;">
<table style="border-collapse: collapse; width: 100%;">
    <thead>
        <tr style="background-color: #f0f0f0;">
            <th style="padding: 10px; border: 1px solid #dddddd; text-align: left;">Role</th>
            <th style="padding: 10px; border: 1px solid #dddddd; text-align: left;">Name</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 10px; border: 1px solid #dddddd;">Project Manager</td>
            <td style="padding: 10px; border: 1px solid #dddddd;">Aurelia Maria Ozora</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #dddddd;">Descriptive Data Analyst</td>
            <td style="padding: 10px; border: 1px solid #dddddd;">Prabhu Raj Singh</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #dddddd;">Diagnostic Analytics Specialist</td>
            <td style="padding: 10px; border: 1px solid #dddddd;">Pau Garcia I Morales</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #dddddd;">Machine Learning Specialist</td>
            <td style="padding: 10px; border: 1px solid #dddddd;">Muna Mohammad Ahmad Shati</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #dddddd;">Lead UI/UX Designer</td>
            <td style="padding: 10px; border: 1px solid #dddddd;">Dharani Ranasinghe</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #dddddd;">Web Application Developer</td>
            <td style="padding: 10px; border: 1px solid #dddddd;">Brian Anyau Nyeko Moini</td>
        </tr>
    </tbody>
</table>
</div>
"""

st.markdown(developers_table, unsafe_allow_html=True)

st.markdown(""" 
    ### **Scientific References**
    1. Soh JGS, Wong WP, Mukhopadhyay A, Quek SC, Tai BC. Predictors of 30-day unplanned hospital readmission among adult patients with diabetes mellitus: a systematic review with meta-analysis. BMJ Open Diabetes Res Care [Internet]. 2020;8(1):e001227. Available from: http://dx.doi.org/10.1136/bmjdrc-2020-001227 
    2. Rubin DJ. Hospital readmission of patients with diabetes. Curr Diab Rep [Internet]. 2015;15(4):17. Available from: http://dx.doi.org/10.1007/s11892-015-0584-7
    3. Zisman-Ilani Y, Fasing K, Weiner M, Rubin DJ. Exercise capacity is associated with hospital readmission among patients with diabetes. BMJ Open Diabetes Res Care [Internet]. 2020;8(1):e001771. Available from: http://dx.doi.org/10.1136/bmjdrc-2020-001771
    4. UCI machine learning repository [Internet]. Uci.edu. [cited 2024 Oct 15]. Available from: https://archive.ics.uci.edu/dataset/34/diabetes 
""")


