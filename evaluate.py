import pandas as pd
from data.raw.recommend import recommend

DATA_PATH = "data/raw/Gen_AI_Dataset.xlsx"  # rename if needed

def main():
    df = pd.read_excel(DATA_PATH)

    total = 0
    correct = 0

    for _, row in df.iterrows():
        query = row["Query"]
        true_url = row["Assessment_url"]

        results = recommend(query, k=10)
        predicted_urls = [r["url"] for r in results]

        if true_url in predicted_urls:
            correct += 1

        total += 1

    mean_recall = correct / total if total else 0
    print(f"Mean Recall@10: {mean_recall:.4f}")

if __name__ == "__main__":
    main()
