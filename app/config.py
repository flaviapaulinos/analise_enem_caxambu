import os
import streamlit as st

API_URL = os.getenv(
    "API_URL",
    st.secrets.get(
        "API_URL",
        "http://127.0.0.1:8000/predict"
    )
)