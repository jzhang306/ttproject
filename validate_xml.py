from lxml import etree

def validate_with_relaxng(xml_file, rng_file):
    xml_doc = etree.parse(xml_file)
    relaxng_doc = etree.parse(rng_file)
    relaxng = etree.RelaxNG(relaxng_doc)

    if relaxng.validate(xml_doc):
        print("✅ XML validation successful!")
    else:
        print("❌ XML validation failed!")
        for error in relaxng.error_log:
            print(error)

if __name__ == "__main__":
    validate_with_relaxng("arxiv_articles_annotated.xml", "scitermtracker.rng")

