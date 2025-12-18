import pandas as pd
from data.raw.recommend import recommend

INPUT_FILE = "data/raw/Gen_AI_Dataset.xlsx"
OUTPUT_FILE = "data/submission.csv"

def main():
    df = pd.read_excel(INPUT_FILE)

    # Fix column name if SHL used something else
    query_col = df.columns[0]

    rows = []

    for _, row in df.iterrows():
        query = str(row[query_col]).strip()

        if not query or query.lower() == "nan":
            continue

        urls = recommend(query, k=50)

        output_row = {
            "Query": query
        }

        for i in range(10):
            output_row[f"Assessment_url_{i+1}"] = urls[i] if i < len(urls) else ""

        rows.append(output_row)

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Submission file written: {OUTPUT_FILE}")
    print(f"Total rows: {len(out_df)}")


if __name__ == "__main__":
    main()
