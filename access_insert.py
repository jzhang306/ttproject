import xml.etree.ElementTree as ET
from pymongo import MongoClient

# Connection to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["sciterm_db"]
collection = db["articles"]

# Clean old data
collection.delete_many({})

# Read XML file
tree = ET.parse("arxiv_articles_annotated.xml")
root = tree.getroot()

inserted = 0

def extract_abstract_text(elem):
    parts = []
    if elem.text:
        parts.append(elem.text)
    for node in elem:
        if node.tag == "term":
            parts.append(node.text or "")
        else:
            if node.text:
                parts.append(node.text)
        if node.tail:
            parts.append(node.tail)
    return "".join(parts).strip()

# Go over articles
for art in root.findall("article"):
    doc = {
        "title": art.findtext("title"),
        "author": art.findtext("author"),
        "date": art.findtext("date"),
        "discipline": art.findtext("discipline"),
        "source": art.findtext("source"),
        "terms": [],
        "abstract": ""
    }

    abstract_elem = art.find("abstract")
    doc["abstract"] = extract_abstract_text(abstract_elem)

    # Extract terms
    for term in abstract_elem.findall(".//term"):
        if term.text:
            doc["terms"].append(term.text)

    collection.insert_one(doc)
    inserted += 1

print(f"{inserted} data inserted.")

