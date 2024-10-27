# GlucoGuard Analytics web dashboard

The objective of the project is to develop a web-based dashboard designed to
present the results of analyzing the diabetic patient dataset from the UCI Repository
(https://archive.ics.uci.edu/dataset/34/diabetes). 

The dashboard consist of detailed information regarding the dataset, results from descriptive and diagnostic
analytics, a prediction engine, and SHAP analysis. 
The targeted end users are healthcare professionals to better understand diabetic patient characteristics and outcomes, particularly hospital readmission.

### Dependencies

Tested on Python 3.10 with the following packages:
  - Jupyter v1.1.1
  - Streamlit v1.38.0
  - Seaborn v0.13.2
  - Plotly v5.24.0
  - Scikit-Learn v1.5.1
  - shap v0.46.0

### Installation

Run the commands below in a terminal to configure the project and install the package dependencies for the first time.

If you are using Mac, you may need to follow install Xcode. Check the official Streamlit documentation [here](https://docs.streamlit.io/get-started/installation/command-line#prerequisites). 

1. Create the environment with `python -m venv env`
2. Activate the virtual environment for Python
   - `source env/bin/activate` [in Linux/Mac]
   - `.\env\Scripts\activate.bat` [in Windows command prompt]
   - `.\env\Scripts\Activate.ps1` [in Windows PowerShell]
3. Make sure that your terminal is in the environment (`env`) not in the global Python installation
4. Install required packages `pip install -r ./requirements.txt`
5. Check that everything is ok running `streamlit hello`

### Execution

To run the dashboard execute the following command:

```
> streamlit run Dashboard.py
# If the command above fails, use:
> python -m streamlit run Dashboard.py
```