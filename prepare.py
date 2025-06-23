from lxml import etree
from lxml.etree import Element, SubElement

# Term list to annotate
TERM_LIST = [
    "neural network",
    "deep learning",
    "gradient descent",
    "transformer",
    "backpropagation",
    "reinforcement learning",
    "convolutional network",
    "support vector machine",
    "random forest",
    "unsupervised learning"
]

IN_FILE = "arxiv_raw.json"
OUT_FILE = "arxiv_articles_raw.xml"

def annotate_terms(text, terms):
    for term in sorted(terms, key=lambda x: -len(x)):
        text = text.replace(term, f"<term>{term}</term>")
    return text

def build_xml(articles):
    root = Element("articles")

    for art in articles:
        article = SubElement(root, "article")

        SubElement(article, "title").text = art["title"]
        SubElement(article, "author").text = ", ".join(art["authors"])
        SubElement(article, "date").text = art["published"][:10]
        SubElement(article, "discipline").text = art["category"]
        SubElement(article, "source").text = art["source"]

        abstract_text = art["summary"].replace("\n", " ")
        annotated = annotate_terms(abstract_text, TERM_LIST)

        abstract_elem = SubElement(article, "abstract")
        try:
            wrapper = etree.fromstring(f"<wrapper>{annotated}</wrapper>")
            if wrapper.text and wrapper.text.strip():
                abstract_elem.text = wrapper.text
            for node in wrapper:
                abstract_elem.append(node)
        except etree.XMLSyntaxError:
            abstract_elem.text = abstract_text

    return root

def save_pretty_xml(root, filename):
    xml_bytes = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)
    with open(filename, "wb") as f:
        f.write(xml_bytes)
    print(f"Saved XML to {filename}")

def main():
    import json
    with open(IN_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)
    print(f"Loaded {len(articles)} articles from {IN_FILE}")

    root = build_xml(articles)
    save_pretty_xml(root, OUT_FILE)

if __name__ == "__main__":
    main()