from pylode.profiles.vocpub import VocPub
import os
from bs4 import BeautifulSoup, formatter

source_ontology_path = './semiconto.ttl'
onto_json_path = './semiconto.json'
html_path = './docs/index.html'
webvowl_json_path = './docs/webvowl/data/semiconto.json'

def generate_webvowl():
    cmd = "java --add-opens java.base/java.lang=ALL-UNNAMED -jar owl2vowl.jar -file {onto} -output {output}".format(onto=source_ontology_path, output=webvowl_json_path)
    os.system(cmd)
    #mv_cmd = "mv -f {onto_json} {output}".format(onto_json=onto_json_path, output=webvowl_json_path)
    #os.system(mv_cmd)

def generate_html():
    onto_doc = VocPub(ontology=source_ontology_path)
    onto_doc.make_html(destination=html_path)

def add_webvowl_to_html():
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        overview = BeautifulSoup(
             f"""
               <div class="section" id="overview">
                    <h2>Overview</h2>
                    <div class="figure">
                        <iframe width="100%" height ="800px" src="webvowl/index.html#semiconto"></iframe>
                        <div class="caption">
                            <strong>Figure 1:</strong>
                                Ontology Overview
                        </div>
                    </div>
                    </div>
                """, "html.parser")
        tag = soup.find(id='classes')
        tag.insert_before(overview)
        html_formatter = formatter.HTMLFormatter(indent=4)
        with open(html_path, "w") as f:
            f.write(soup.prettify(formatter=html_formatter))

def main():
    generate_html()
    generate_webvowl()
    add_webvowl_to_html()

if __name__ == "__main__":
    main()