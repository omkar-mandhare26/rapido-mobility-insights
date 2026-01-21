import streamlit as st
from components import (
    dashboard,
    visualization_outputs,
    business_outputs,
    prediction_models
)

st.set_page_config(layout="wide")

st.sidebar.title("Rapido Mobility Insights")
option = st.sidebar.radio(
    "Check Out", ("Dashboard", "Visualization Outputs", "Business Outputs", "Prediction Models")
)

if option == "Dashboard": 
    dashboard(st)
elif option == "Visualization Outputs": 
    visualization_outputs(st)
elif option == "Business Outputs": 
    business_outputs(st)
elif option == "Prediction Models": 
    prediction_models()