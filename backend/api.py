from fastapi import FastAPI
from pydantic import BaseModel
from data.raw.recommend import recommend_api

app = FastAPI(title="SHL Assessment Recommender")

class RecommendRequest(BaseModel):
    query: str

@app.post("/recommend")
def recommend_endpoint(req: RecommendRequest):
    return {
        "query": req.query,
        "results": recommend_api(req.query)
    }

@app.get("/")
def root():
    return {"status": "ok"}
