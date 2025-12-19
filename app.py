import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_metadata():
    return pd.read_csv(os.path.join(BASE_DIR, "shl_assessments.csv"))

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def load_index():
    return faiss.read_index(os.path.join(BASE_DIR, "index.faiss"))

df = load_metadata()
model = load_model()
index = load_index()

st.title("Semantic Search")

query = st.text_input("Enter query")

if query:
    emb = model.encode([query])
    D, I = index.search(np.array(emb), k=5)

    results = df.iloc[I[0]]

    st.subheader("Top Matches")
    for _, row in results.iterrows():
        st.markdown(f"### {row['assessment_name']}")
        st.write(row['description'])
        st.link_button("View Assessment", row['link'])
