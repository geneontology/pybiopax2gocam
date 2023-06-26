import argparse
import pybiopax
from pybiopax.biopax import BioPaxObject
from typing import List
import networkx as nx
import pprint

def main():
    #parser = parse_arguments()
    #bp_file =  parser.bp_file
    bp_file  = './resources/test_biopax/LIPASYN-PWY-1.owl'

    model = pybiopax.model_from_owl_file(bp_file, encoding="utf8")

    source_obj = model.objects['Pathway26234']
    target_obj = model.objects['BiochemicalReaction26361']

    path = find_path(source_obj, target_obj)

    if path:
        for obj in path:
            print(obj)
    else:
        print("Path not found.")
        
    return path

    


def parse_arguments():
    parser = argparse.ArgumentParser(description='Description',
                                     epilog='It works!')
    parser.add_argument('-i', dest='bp_file', required=True,
                         help='Biopax File')

    return parser.parse_args()


def find_path(source_obj: BioPaxObject, target_obj: BioPaxObject) -> List[BioPaxObject]:
  
    if source_obj is target_obj:
        return [source_obj]

    for attr_name in dir(source_obj):
        attr_value = getattr(source_obj, attr_name)
        if attr_value is target_obj:
            return [source_obj, target_obj]
        if isinstance(attr_value, list):
            for obj in attr_value:
                if isinstance(obj, BioPaxObject):
                    path = find_path(obj, target_obj)
                    if path:
                       return [source_obj] + path
        if isinstance(attr_value, BioPaxObject):
            path = find_path(attr_value, target_obj)
            if path:
                return [source_obj] + path

    return []


if __name__ == '__main__' :
    main()
