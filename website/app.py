import streamlit as st
import requests

API_URL = "https://YOUR-BACKEND-URL.onrender.com/recommend"

st.title("SHL Assessment Recommendation Engine")

query = st.text_area("Enter hiring requirement")

if st.button("Find Assessments"):
    if len(query.strip()) < 5:
        st.error("Please enter at least 5 characters")
    else:
        with st.spinner("Finding best assessments..."):
            response = requests.get(API_URL, params={"query": query})
            data = response.json()

            for item in data["results"]:
                st.markdown(f"- [{item['name']}]({item['url']})")
