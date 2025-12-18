import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"

st.title("SHL Assessment Finder")

query = st.text_area("Describe your hiring need")

if st.button("Find Assessments"):
    if len(query) < 5:
        st.error("Please enter a meaningful query")
    else:
        with st.spinner("Finding assessments..."):
            try:
                resp = requests.get(
                    API_URL,
                    params={"query": query},
                    timeout=20
                )
                resp.raise_for_status()
                data = resp.json()

                for r in data["results"]:
                    st.markdown(f"- [{r['name']}]({r['url']})")

            except Exception as e:
                st.error(f"API error: {e}")
