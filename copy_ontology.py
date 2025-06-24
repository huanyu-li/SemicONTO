#!/usr/bin/env python3
from glob import glob
import os
from rdflib import Graph
import re
import logging

# Configure root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)

def copy_ontologies():
    """Copy ontologies to web path."""
    #version = 0.1
    for version in [0.1, 0.2]:
        file_name = 'SemicONTO.ttl'
        source = f"ontology/{version}/{file_name}"
        target = f"docs/{version}/"
        os.makedirs(target, exist_ok=True)
        onto_name = file_name.split('.')[0]

        logging.debug(f"Source:\t{source}")
        logging.debug(f"FileName:\t{file_name}")
        logging.debug(f"Target:\t{target}")
        logging.debug(f"Onto_Name:\t{onto_name}")
                
        g = Graph()
        g.parse(source)
        g.serialize(destination=f"{target}{onto_name}.ttl", format="turtle")
        g.serialize(destination=f"{target}{onto_name}.rdf", format="xml")
        g.serialize(destination=f"{target}{onto_name}.owl", format="xml")
        g.serialize(destination=f"{target}{onto_name}.jsonld", format="json-ld")


if __name__ == "__main__":
    copy_ontologies()
