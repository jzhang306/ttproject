from pymongo import MongoClient
from collections import Counter
from datetime import datetime
import json

# connection
client = MongoClient("mongodb://localhost:27017/")
db = client["sciterm_db"]
collection = db["articles"]

def term_first_appearance(term):
    #first appearance
    result = collection.find({"terms": term}).sort("date", 1).limit(1)
    for doc in result:
        return doc["date"]
    return None

def term_frequency_over_time(term):
    #times
    cursor = collection.find({"terms": term})
    year_counts = Counter()
    for doc in cursor:
        try:
            year = datetime.strptime(doc["date"], "%Y-%m-%d").year
            year_counts[year] += 1
        except Exception:
            continue
    return dict(sorted(year_counts.items()))

def term_usage_by_field(term):
    #frequency
    cursor = collection.find({"terms": term})
    field_counts = Counter()
    for doc in cursor:
        if doc.get("discipline"):
            field_counts[doc["discipline"]] += 1
    return dict(field_counts.most_common())

def compare_terms(term1, term2):
    #comparison 
    freq1 = term_frequency_over_time(term1)
    freq2 = term_frequency_over_time(term2)
    return freq1, freq2

def main():
    terms = [
        "neural network",
        "deep learning",
        "gradient descent",
        "transformer",
        "backpropagation"
    ]

    # first appearance for each term
    for term in terms:
        first_date = term_first_appearance(term)
        print(f"Term '{term}' first appears on: {first_date}")

    # trend
    term = "neural network"
    freq = term_frequency_over_time(term)
    print(f"Frequency over years for '{term}':")
    print(freq)

    # 
    usage = term_usage_by_field(term)
    print(f"Usage of '{term}' by discipline:")
    print(usage)

    # 示
    freq1, freq2 = compare_terms("neural network", "deep learning")
    print(f"Comparison of 'neural network' and 'deep learning':")
    print("neural network:", freq1)
    print("deep learning:", freq2)

    # json
    output = {
        "first_appearance": {t: term_first_appearance(t) for t in terms},
        "frequency": {t: term_frequency_over_time(t) for t in terms}
    }
    with open("term_stats.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("Saved summary stats to term_stats.json")

if __name__ == "__main__":
    main()
