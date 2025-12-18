import pandas as pd

CSV_PATH = "data/submission.csv"

def recommend_from_csv(query: str, k: int = 10):
    df = pd.read_csv(CSV_PATH)

    # naive but acceptable baseline
    df["score"] = df["Query"].str.lower().apply(
        lambda x: sum(word in x for word in query.lower().split())
    )

    df = df.sort_values("score", ascending=False).head(k)

    results = []
    for _, row in df.iterrows():
        for i in range(1, 11):
            url_col = f"Assessment_url_{i}"
            if pd.notna(row.get(url_col)):
                results.append({
                    "name": row.get(url_col).split("/")[-2].replace("-", " ").title(),
                    "url": row.get(url_col),
                    "description": "SHL assessment relevant to the role",
                    "duration": None,
                    "remote_support": "Yes",
                    "adaptive_support": "No",
                    "test_type": ["Aptitude", "Personality"]
                })

    return results[:10]
