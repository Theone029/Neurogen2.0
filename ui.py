import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8001")
API_KEY = os.getenv("API_KEY", "supersecureapikey123")

st.title("AI Memory System - Search Interface")

query = st.text_input("Enter your search query:")
project = st.text_input("Project (default: NEUROGEN)", value="NEUROGEN")

if st.button("Semantic Search"):
    headers = {"API_KEY": API_KEY}
    params = {"query": query, "project": project, "limit": 5}
    response = requests.get(f"{API_URL}/semantic_recall", headers=headers, params=params)
    if response.status_code == 200:
        st.write(response.json())
    else:
        st.error(f"Error: {response.text}")
