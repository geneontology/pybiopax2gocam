import argparse
import pybiopax
from pybiopax.biopax import BioPaxObject
from pybiopax.paths import find_objects
from typing import List, Tuple
import pprint

def main():
    parser = parse_arguments()
    bp_file =  parser.bp_file
    source_uid = parser.source_uid
    target_uid = parser.target_uid
   
    model = pybiopax.model_from_owl_file(bp_file, encoding="utf8")

    source_obj = model.objects[source_uid]
    target_obj = model.objects[target_uid]

    memo.clear()
    path = find_path_components(source_obj, target_obj)
    
    results = []

    for _, item in path:
        results.append(item)

    result_string = '/'.join(results)

    print(result_string)

    print(f'from {source_obj.uid} to {target_obj.uid}')
    if path:
        for obj in path:
            print(obj)
    else:
        print("Path not found.")
        
    pathway = model.objects[source_uid]
    objs = find_objects(pathway, result_string)
    
    print("\nPrint Object at target id\n")
    for obj in objs:
        print('%s -> %s' % (obj.uid, obj.name))
        """       if obj.name and isinstance(obj.name, list):
            has_isoform = any(['isoform' in x for x in obj.name])
            if has_isoform:
                print('%s -> %s' % (obj.uid, obj.name)) """

    


def parse_arguments():
    parser = argparse.ArgumentParser(description='Description',
                                     epilog='It works!')
    parser.add_argument('-i', dest='bp_file', required=True,
                         help='Biopax File')
    parser.add_argument('-s', dest='source_uid', required=True)
    parser.add_argument('-t', dest='target_uid', required=True)

    return parser.parse_args()

memo = dict()
     
def find_path(source_obj: BioPaxObject, target_obj: BioPaxObject) ->  List[BioPaxObject]:
    if source_obj.uid in memo:
        return memo[source_obj.uid]    
        
    if source_obj is target_obj:
        return [source_obj.uid]
    
    for attr_name in vars(source_obj):
        attr_value = getattr(source_obj, attr_name)      
        if attr_value is target_obj:
            return [source_obj.uid, target_obj.uid]            
            
        if isinstance(attr_value, list):
            for obj in attr_value:
                if isinstance(obj, BioPaxObject):
                    path = find_path( obj, target_obj) 
                    if path:
                        res = [source_obj.uid] + path
                        memo[source_obj.uid] = res
                        return res
                       
        elif isinstance(attr_value, BioPaxObject):
            path = find_path(attr_value, target_obj)
            if path:
                res = [source_obj.uid] + path
                memo[source_obj.uid] = res
                return res

    return []


def find_path_components(source_obj: BioPaxObject, target_obj: BioPaxObject) -> List[Tuple[BioPaxObject, str]]:
    if source_obj.uid in memo:
        return memo[source_obj.uid]   
     
    if source_obj is target_obj:
        return [(source_obj.uid, '--')]

    for attr_name in vars(source_obj):
        attr_value = getattr(source_obj, attr_name)
        if attr_value is target_obj:
            return [(source_obj.uid, attr_name), (target_obj.uid, attr_name)]
        if isinstance(attr_value, list):
            for obj in attr_value:
                if isinstance(obj, BioPaxObject):
                    path = find_path_components(obj, target_obj)
                    if path:
                        res = [(source_obj.uid, attr_name)] + path
                        memo[source_obj.uid] = res
                        return res
        elif isinstance(attr_value, BioPaxObject):
            path = find_path_components(attr_value, target_obj)
            if path:
                res = [(source_obj.uid, attr_name)] + path
                memo[source_obj.uid] = res
                return res

    return []

                       
if __name__ == '__main__' :
    main()


#  python3 -m playground.analysis -s Pathway1 -t SmallMolecule10 -i ./resources/test_biopax/reactome/R-HSA-204174_level3.owl


