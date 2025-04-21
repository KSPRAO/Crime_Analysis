import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="CrimePulse India", layout="wide")
st.title("CrimePulse India: State-Wise Crime Prediction (2001-2012)")
st.write("Analyze and predict crime trends across Indian states.")

# Load data for dropdowns
data_path = r"data/newtrial - Sheet 1 - 01_District_wise_crim 2.csv"
df = pd.read_csv(data_path)
states = sorted(df['STATE/UT'].unique())
years = list(range(2001, 2013))

state = st.selectbox("Select State/UT", states)
year = st.selectbox("Select Year", years)

if st.button("Predict Crime Trend"):
    payload = {'state': state, 'year': year}
    try:
        response = requests.post("http://localhost:5000/predict", json=payload, timeout=5)
        if response.status_code == 200:
            result = response.json()['predicted_crime']
            st.success(f"Predicted Dominant Crime in {state} ({year}): {result}")
        else:
            st.error(f"Server returned status code {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to Flask server at http://localhost:5000. Ensure 'app.py' is running.")
    except requests.exceptions.Timeout:
        st.error("Request timed out. Check if the Flask server is responding.")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")

st.markdown("---")
st.write("Built for analyzing Indian crime data | CrimePulse India")
