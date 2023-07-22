import argparse
import re
from ontobio.ontol_factory import OntologyFactory
import pybiopax
from pybiopax.biopax import UnificationXref
import pprint

ACCEPTED_DBS = ['reactome', 'uniprot',  'chebi']

def main():
    parser = parse_arguments()
    bp_file =  parser.bp_file
   
    model = pybiopax.model_from_owl_file(bp_file, encoding="utf8")

    terms = set()
    xrefs = model.get_objects_by_type(UnificationXref)
    
    for xref in xrefs:
        if (xref.db and xref.id):
            if xref.db.lower() in ACCEPTED_DBS:     
                cleaned_id = clean_id(xref.id)
                terms.add(f'{xref.db}:{cleaned_id}')        
            elif xref.db.lower() == 'gene ontology':
                terms.add(xref.id)  

    
    pprint.pp(terms)
    
    
def clean_id(id):
    # just realize some values have db CHEBI and id CHEBI:1234 aghhh
    clean_id = re.sub('^.*?:', '', id)
    
    return clean_id
   
    

ont = OntologyFactory().create()
label = ont.label("GO:0008150")

print(label)
def parse_arguments():
    parser = argparse.ArgumentParser(description='Description',
                                     epilog='It works!')
    parser.add_argument('-i', dest='bp_file', required=True,
                         help='Biopax File')

    return parser.parse_args()

memo = dict()
                      
if __name__ == '__main__' :
    main()


#  python3 -m playground.get_terms -i ./resources/test_biopax/reactome/R-HSA-204174_level3.owl

