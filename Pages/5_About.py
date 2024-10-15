import streamlit as st

st.set_page_config(
    page_title="GlucoGuard Dashboard",
    page_icon="./assets/Page-icon.png",
)
st.sidebar.image("./assets/glucoguard-logo.png",)

st.write("# About #")

st.markdown(""" 
    ### **Dataset**
    The dataset contains information about diabetes patients records including; the medication taken and the readmission rates [4].
    The dataset have 50 features and 101765 observations. 
            
    ### **Scientific references**:
    1. Soh JGS, Wong WP, Mukhopadhyay A, Quek SC, Tai BC. Predictors of 30-day unplanned hospital readmission among adult patients with diabetes mellitus: a systematic review with meta-analysis. BMJ Open Diabetes Res Care [Internet]. 2020;8(1):e001227. Available from: http://dx.doi.org/10.1136/bmjdrc-2020-001227 
    2. Rubin DJ. Hospital readmission of patients with diabetes. Curr Diab Rep [Internet]. 2015;15(4):17. Available from: http://dx.doi.org/10.1007/s11892-015-0584-7
    3. Zisman-Ilani Y, Fasing K, Weiner M, Rubin DJ. Exercise capacity is associated with hospital readmission among patients with diabetes. BMJ Open Diabetes Res Care [Internet]. 2020;8(1):e001771. Available from: http://dx.doi.org/10.1136/bmjdrc-2020-001771
    4. UCI machine learning repository [Internet]. Uci.edu. [cited 2024 Oct 15]. Available from: https://archive.ics.uci.edu/dataset/34/diabetes 
""")

st.markdown("### **Group Members and Contact Information:**")
st.markdown("""
- Pau Garcia I Morales (paga3834@student.su.se)
- Brian Anyau Nyeko Moini (brny3781@student.su.se)
- Aurelia Maria Ozora (auoz0688@student.su.se)
- Dharani Ranasinghe (dhra0020@student.su.se)
- Muna Mohammad Ahmad Shati (mush9472@student.su.se)
- Prabhu Raj Singh (prsi5558@student.su.se)
""")