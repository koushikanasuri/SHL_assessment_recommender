import requests
from bs4 import BeautifulSoup
import json
import time
from tqdm import tqdm
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os

# -------------------- CONFIG --------------------

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/products/product-catalog/"
MAX_LINKS = 600          # hard cap, intentional
PAGE_SIZE = 12           # SHL pagination size
SLEEP_SECONDS = 1.5

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -------------------- SESSION --------------------

session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)
session.mount("https://", HTTPAdapter(max_retries=retries))

# -------------------- HELPERS --------------------

def get_soup(url):
    r = session.get(
        url,
        headers=HEADERS,
        timeout=60,
        verify=False
    )
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

# -------------------- LINK EXTRACTION (WORKING VERSION) --------------------

def extract_assessment_links():
    links = set()
    start = 0

    while True:
        url = f"{CATALOG_URL}?start={start}"
        try:
            soup = get_soup(url)
        except Exception as e:
            print(f"Stopping pagination at start={start} due to error:", e)
            break

        cards = soup.select("a[href*='/products/']")
        if not cards:
            break

        for a in cards:
            href = a.get("href")
            if href and "/products/" in href:
                links.add(BASE_URL + href)

        print(f"Collected links so far: {len(links)}")

        if len(links) >= MAX_LINKS:
            print("Reached link cap, stopping.")
            break

        start += PAGE_SIZE
        time.sleep(SLEEP_SECONDS)

    # persist links immediately (important)
    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/assessment_links.json", "w", encoding="utf-8") as f:
        json.dump(list(links), f, indent=2)

    return list(links)

# -------------------- PAGE PARSING --------------------

def parse_assessment(url):
    try:
        soup = get_soup(url)
    except Exception as e:
        print(f"Skipping assessment page {url} due to error:", e)
        return None

    def safe_text(selectors):
        for selector in selectors:
            el = soup.select_one(selector)
            if el:
                text = el.get_text(strip=True)
                if text:
                    return text
        return None

    # Name is usually stable
    name = safe_text(["h1", "h1 span"])

    # Description varies a LOT on SHL pages
    description = safe_text([
        "div.product-description",
        "div.cmp-text",
        "div.rich-text",
        "section div",
        "main p"
    ])

    # Test type extraction (best-effort)
    test_type = []
    for li in soup.select("li"):
        text = li.get_text(strip=True)
        if "Test Type" in text:
            test_type = [t.strip() for t in text.split(":")[-1].split(",")]

    return {
        "name": name,
        "url": url,
        "description": description,
        "test_type": test_type,
        "duration": None,
        "remote_support": None,
        "adaptive_support": None
    }


# -------------------- CRAWL --------------------

def crawl():
    # if links already exist, reuse them
    links_path = "data/raw/assessment_links.json"
    if os.path.exists(links_path):
        with open(links_path, "r", encoding="utf-8") as f:
            links = json.load(f)
        print(f"Loaded {len(links)} links from cache")
    else:
        links = extract_assessment_links()

    results = []

    for link in tqdm(links):
        data = parse_assessment(link)
        if data and data["name"] :
            results.append(data)
        time.sleep(1)

    return results

# -------------------- MAIN --------------------

if __name__ == "__main__":
    assessments = crawl()
    print(f"Total assessments scraped: {len(assessments)}")

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/shl_assessments.json", "w", encoding="utf-8") as f:
        json.dump(assessments, f, indent=2, ensure_ascii=False)
