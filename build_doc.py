from pylode.profiles.vocpub import VocPub
import os
from bs4 import BeautifulSoup, formatter

source_ontology_path = './ontology/0.1/SemicONTO.ttl'
onto_json_path = './SemicONTO.json'
html_path = './docs/0.1/index.html'
webvowl_json_path = './docs/0.1/webvowl/data/SemicONTO.json'

def generate_webvowl():
    cmd = "java --add-opens java.base/java.lang=ALL-UNNAMED -jar owl2vowl.jar -file {onto} -output {output}".format(onto=source_ontology_path, output=webvowl_json_path)
    os.system(cmd)

def generate_html():
    onto_doc = VocPub(ontology=source_ontology_path)
    onto_doc.make_html(destination=html_path)

def add_webvowl_to_html():
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

        download_overview = BeautifulSoup(
            f"""
            <div class="section" id="download">
                <dl>
                    <div>
                        <dt>
                            <strong>
                                Download Serialization
                            </strong>
                        </dt>
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
                        <iframe width="100%" height ="800px" src="webvowl/index.html#SemicONTO"></iframe>
                        <div class="caption">
                            <strong>Figure 1:</strong>
                                Ontology Overview
                        </div>
                    </div>
                    </div>
            """, "html.parser")

        overview = BeautifulSoup(
             f"""
               <div class="section" id="overview">
                    <h2>Overview</h2>
                    <div class="figure">
                        <iframe width="100%" height ="800px" src="webvowl/index.html#SemicONTO"></iframe>
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

        with open(html_path, "w") as f:
            f.write(soup.prettify(formatter=html_formatter))

def main():
    generate_html()
    generate_webvowl()
    add_webvowl_to_html()

if __name__ == "__main__":
    main()