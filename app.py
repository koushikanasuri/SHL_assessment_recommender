import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def load_index():
    return faiss.read_index("index.faiss")

st.title("Semantic Search")

model = load_model()
index = load_index()

query = st.text_input("Enter query")

if query:
    emb = model.encode([query])
    D, I = index.search(np.array(emb), k=5)
    st.write("Results:", I)
