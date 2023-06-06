import pybiopax
from collections import Counter
import pprint

biopax_file = './resources/test_biopax/R-HSA-204174_level3.owl'
model = pybiopax.model_from_owl_file(biopax_file, encoding="utf8")
for obj in model.objects.values():
  #pprint.pp (obj)
  pass
 
stats = Counter([obj.__class__.__name__  for uid, obj in model.objects.items()]).most_common(10)
pprint.pp(stats)

for reaction in model.get_objects_by_type(pybiopax.biopax.BiochemicalReaction):
    print('%s -> %s' % (reaction.left, reaction.right))

for pathway in model.get_objects_by_type(pybiopax.biopax.Pathway):
    name = pathway
    print(name.uid)
    #[pprint.pp(src.display_name) for src in pathway.data_source]
    #print(pathway.controller_of(pybiopax.biopax.PathwayStep))
    pprint.pp(pathway.__dict__)
    #print(pathway.pathway_order)
    for obj in pathway.pathway_component:
        pprint.pp('%s -> %s' % (obj.uid, obj.display_name))
        pc = model.objects[obj.uid]       
            
        for l in pc.left:
            print('\t %s -> %s' % ('has_input',  l.display_name))
            
        for r in pc.right:
            print('\t %s --> %s' % ('has_output',  r.display_name))