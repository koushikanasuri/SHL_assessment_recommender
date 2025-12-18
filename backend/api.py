from fastapi import FastAPI, Query
from backend.recommend import recommend

app = FastAPI(title="SHL Assessment Recommender")

@app.get("/recommend")
def recommend_api(
    query: str = Query(..., min_length=5),
    k: int = Query(10, ge=1, le=10)
):
    results = recommend(query, k)
    return {"results": results}
