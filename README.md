# SHL_assessment_recommender

**Overview**

This project implements an intelligent assessment recommendation system for SHL’s product catalog.
Given a natural language query or job description, the system recommends the most relevant SHL Individual Test Solutions using semantic search powered by transformer embeddings and FAISS.

The solution is designed to replace brittle keyword-based search with a retrieval-based, context-aware recommendation pipeline.
**
Architecture
**
The system is intentionally split into two components for clarity, scalability, and evaluation:

1. API Layer (FastAPI)

Hosts the recommendation engine

Exposes SHL-compliant endpoints

Performs embedding, similarity search, and result formatting

Deployed on Hugging Face Spaces (Docker)

2. Web Application (Streamlit)

Interactive frontend for human evaluation

Accepts free-text queries

Displays ranked assessment recommendations

Deployed on Streamlit Community Cloud

User Query
   ↓
Sentence Transformer Embeddings
   ↓
FAISS Vector Search
   ↓
Metadata Mapping
   ↓
Ranked SHL Assessment Recommendations

Data Pipeline

Web Scraping

Crawled SHL Product Catalog

Extracted only Individual Test Solutions

Ignored Pre-packaged Job Solutions

Final dataset size: 377+ assessments

Data Enrichment

Combined assessment name, description, and attributes

Normalized metadata fields (URL, test type, duration, etc.)

Embedding & Indexing

Model: all-MiniLM-L6-v2 (Sentence Transformers)

Vector index: FAISS (CPU)

Each assessment mapped 1:1 to FAISS index position

Technology Stack

Language: Python

Embedding Model: Sentence Transformers

Vector Search: FAISS

API Framework: FastAPI

Frontend: Streamlit

Deployment:

API: Hugging Face Spaces (Docker)

UI: Streamlit Cloud

API Endpoints (SHL Compliant)
Health Check
GET /health


Response:

{
  "status": "healthy"
}

Assessment Recommendation
POST /recommend


Request:

{
  "query": "Java developer with strong communication skills"
}


Response:

{
  "recommended_assessments": [
    {
      "assessment_name": "...",
      "assessment_url": "...",
      "description": "...",
      "duration": 30,
      "remote_support": "Yes",
      "test_type": ["K", "P"]
    }
  ]
}

Evaluation

Used SHL-provided labeled training dataset

Metric: Mean Recall@10

Iteratively improved:

text preprocessing

embedding strategy

ranking balance between technical and behavioral assessments

Evaluation was applied at the retrieval stage, ensuring relevance before presentation.

Repository Structure
API (Hugging Face Space)
app.py
Dockerfile
requirements.txt
index.faiss
shl_assessments_enriched.json

Web App (Streamlit)
app.py
requirements.txt
index.faiss
shl_assessments_enriched.json

Live Links

API Base URL:
https://koushik0016-api_for_shl_assessment.hf.space/

Web Application:
https://shlassessmentrecommender-peheappubars78kth4kef6w.streamlit.app/

GitHub Repository:
[<GitHub repo URL>](https://github.com/koushikanasuri/SHL_assessment_recommender)

**Key Design Decisions**

**Retrieval-first architecture instead of generation-only**

**FAISS chosen for efficient similarity search over large catalog**

**Model selection optimized for semantic relevance vs. latency**

**Separation of API and UI to support automated evaluation and manual inspection**

**Notes**

The system strictly uses scraped SHL catalog data

No hardcoded recommendations

Designed to be modular, reproducible, and extensible

Author

Koushik
GenAI / ML Engineering Candidate
