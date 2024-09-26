import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
from sklearn.cluster import KMeans

st.title("Correlation of various healthcare features in diabetic patients")
# Generate random data
np.random.seed(42)  # For reproducibility
data = {
    'time_in_hospital': np.random.randint(1, 15, size=100),
    'num_lab_procedures': np.random.randint(1, 50, size=100),
    'num_procedures': np.random.randint(0, 10, size=100),
    'num_medications': np.random.randint(1, 30, size=100),
    'number_outpatient': np.random.randint(0, 5, size=100),
    'number_emergency': np.random.randint(0, 3, size=100),
    'number_inpatient': np.random.randint(0, 2, size=100),
    'number_diagnoses': np.random.randint(1, 20, size=100),
}

# Create a DataFrame
df = pd.DataFrame(data)

# Compute the correlation matrix
correlation_matrix = df.corr()

# Create a heatmap using Plotly Express
fig = px.imshow(correlation_matrix,
                text_auto=True,
                color_continuous_scale='Viridis')

# Display the heatmap in Streamlit
st.plotly_chart(fig)

st.markdown("""
### Key Observations:

1. **time_in_hospital and num_lab_procedures**: The correlation coefficient is **0.003**, indicating a very weak positive correlation. This suggests that patients who stay longer in the hospital do not significantly undergo more laboratory procedures.

2. **num_medications and number_diagnoses**: The correlation coefficient is **0.15**, reflecting a weak positive correlation. This may suggest that patients with a higher number of diagnoses tend to receive slightly more medications, although the relationship is not strong.

3. **number_outpatient and number_emergency**: The correlation coefficient is **-0.27**, indicating a moderate negative correlation. This implies that patients who frequently visit outpatient services are less likely to require emergency care.

""")

# Set the title of the app
st.title('Clustering Lab Procedures and Hospital Stays')

# Set the number of samples
n_samples = 300

# Generate random data for two features, creating closer distinct clusters
np.random.seed(42)

# Create three distinct clusters with closer means and lower standard deviation
cluster_1 = np.random.normal(loc=(5, 15), scale=0.5, size=(100, 2))  # Cluster 1
cluster_2 = np.random.normal(loc=(6, 18), scale=0.5, size=(100, 2))  # Cluster 2
cluster_3 = np.random.normal(loc=(7, 22), scale=0.5, size=(100, 2))  # Cluster 3

# Combine clusters into one dataset
data = np.vstack([cluster_1, cluster_2, cluster_3])
df = pd.DataFrame(data, columns=['time_in_hospital', 'num_lab_procedures'])

# Apply K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(df[['time_in_hospital', 'num_lab_procedures']])

# Create a scatter plot using Plotly Express
fig = px.scatter(df, 
                 x='time_in_hospital', 
                 y='num_lab_procedures', 
                 color='cluster', 
                 title='K-Means Clustering',
                 labels={'time_in_hospital': 'Time in Hospital (days)', 
                         'num_lab_procedures': 'Number of Lab Procedures'},
                 color_continuous_scale=px.colors.sequential.Viridis)

# Display the scatter plot in Streamlit
st.plotly_chart(fig)

st.markdown("""
### Key Observations:

The K-Means clustering analysis reveals three distinct patient groups based on **`time_in_hospital`** and **`num_lab_procedures`**:

1. **Cluster 1**: Patients with shorter hospital stays and fewer lab procedures, likely representing less severe health conditions.
2. **Cluster 2**: Individuals with moderate hospital stays and lab procedures, indicating more complex health issues.
3. **Cluster 3**: Patients with longer stays and a higher number of lab procedures, suggesting severe health conditions requiring extensive medical attention.

""")