import subprocess
import os

def run_xslt(input_xml, xslt_file, output_xml):
    cp_sep = ";" if os.name == "nt" else ":"
    classpath = f"utils/saxon-he.jar{cp_sep}utils/xmlresolver.jar"

    cmd = [
        "java", "-cp",
        classpath,
        "net.sf.saxon.Transform",
        f"-s:{input_xml}",
        f"-xsl:{xslt_file}",
        f"-o:{output_xml}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)
    if result.returncode != 0:
        raise RuntimeError("XSLT transformation failed")

if __name__ == "__main__":
    run_xslt("arxiv_articles_raw.xml", "annotate_terms.xsl", "arxiv_articles_annotated.xml")




