import os
from bs4 import BeautifulSoup, formatter
from pylode.profiles.vocpub import VocPub

VERSIONS = ["0.1", "0.2"]

def generate_webvowl(source_ontology_path, webvowl_json_path):
    cmd = f"java --add-opens java.base/java.lang=ALL-UNNAMED -jar owl2vowl.jar -file {source_ontology_path} -output {webvowl_json_path}"
    os.system(cmd)

def generate_html(source_ontology_path, html_path):
    onto_doc = VocPub(ontology=source_ontology_path)
    onto_doc.make_html(destination=html_path)

def add_webvowl_to_html(html_path):
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

        download_overview = BeautifulSoup(
            """
            <div class="section" id="download">
                <dl>
                    <div>
                        <dt><strong>Download Serialization</strong></dt>
                        <dd>
                            <span><a style="text-decoration:none" href="SemicONTO.ttl" target="_blank"><img src="https://img.shields.io/badge/Format-TTL-blue.svg" alt="TTL"></a></span>
                            <span><a style="text-decoration:none" href="SemicONTO.owl" target="_blank"><img src="https://img.shields.io/badge/Format-OWL-blue.svg" alt="OWL"></a></span>
                            <span><a style="text-decoration:none" href="SemicONTO.rdf" target="_blank"><img src="https://img.shields.io/badge/Format-RDF/XML-blue.svg" alt="RDF/XML"></a></span>
                            <span><a style="text-decoration:none" href="SemicONTO.jsonld" target="_blank"><img src="https://img.shields.io/badge/Format-JSON_LD-blue.svg" alt="JSON-LD"></a></span>
                        </dd>
                    </div>
                </dl>
            </div>
            <div class="section" id="overview">
                <h2>Overview</h2>
                <div class="figure">
                    <iframe width="100%" height="800px" src="webvowl/index.html#SemicONTO"></iframe>
                    <div class="caption">
                        <strong>Figure 1:</strong>
                        Ontology Overview
                    </div>
                </div>
            </div>
            """, "html.parser")

        tag = soup.find(id='classes')
        tag.insert_before(download_overview)
        html_formatter = formatter.HTMLFormatter(indent=4)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(soup.prettify(formatter=html_formatter))

def process_version(version):
    print(f"🔧 Processing version: {version}")
    base_path = f"./ontology/{version}"
    docs_path = f"./docs/{version}"
    source_ontology_path = os.path.join(base_path, "SemicONTO.ttl")
    html_path = os.path.join(docs_path, "index.html")
    webvowl_json_path = os.path.join(docs_path, "webvowl/data/SemicONTO.json")

    os.makedirs(os.path.dirname(webvowl_json_path), exist_ok=True)
    os.makedirs(os.path.dirname(html_path), exist_ok=True)

    generate_html(source_ontology_path, html_path)
    generate_webvowl(source_ontology_path, webvowl_json_path)
    add_webvowl_to_html(html_path)

def main():
    for version in VERSIONS:
        process_version(version)

if __name__ == "__main__":
    main()

