import feedparser
import json
import ssl
import certifi
import functools

ssl._create_default_https_context = functools.partial(ssl.create_default_context, cafile=certifi.where())

# Choose article categories
CATEGORY = "cs.LG"
MAX_RESULTS = 1000
OUT_FILE = "arxiv_raw.json"

def collect_arxiv_data():
    base_url = 'http://export.arxiv.org/api/query?'
    query = f'search_query=cat:{CATEGORY}&start=0&max_results={MAX_RESULTS}'
    url = base_url + query

    print("Extracting data from arXiv")
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.title.strip(),
            "authors": [author.name for author in entry.authors],
            "summary": entry.summary.strip(),
            "published": entry.published,
            "source": "arXiv",
            "category": CATEGORY
        })

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(articles)} data to {OUT_FILE}")

if __name__ == "__main__":
    collect_arxiv_data()

