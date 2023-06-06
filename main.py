import pybiopax
import networkx as nx
#import pydot
from ontobio.rdfgen.gocamgen.subgraphs import AnnotationSubgraph
import pprint
from base import relations

biopax_file = './resources/test_biopax/R-HSA-204174_level3.owl'
model = pybiopax.model_from_owl_file(biopax_file, encoding="utf8")

class GoCAM (AnnotationSubgraph):
    def __init__(self):
        self.bp_node = None
        self.mf_map = {}
        super().__init__()

    def process_pathway(self, pathway):        
            
        if pathway.xref:
            self.process_bp(pathway.xref)

        if pathway.pathway_order:
            self.process_step_processes(pathway.pathway_order, pathway)
        
        if pathway.pathway_component:
            self.process_components(pathway.pathway_component, pathway)

    
    def process_step_processes(self, step_processes, pathway):
        for obj in step_processes:
            pc = model.objects[obj.uid]
            for sp in pc.step_process:
                if isinstance(sp, pybiopax.biopax.Catalysis) and sp.control_type == 'ACTIVATION':
                    self.process_mf(sp.xref, model.objects[sp.uid])
   
    
    def process_components(self, components, pathway):
        for obj in components:
            mf = self.mf_map.get(obj.uid, None)

            if mf is None:
                continue

            mf = self.add_instance_of_class(mf, is_anchor=True)

            if self.bp_node is not None:
                self.add_edge(mf, relations['part_of'], self.bp_node)

            gp = self.add_instance_of_class(obj.display_name)
            self.add_edge(mf, relations['enabled_by'], gp)

            pc = model.objects[obj.uid]

            if pc.left:
                self.process_mols(pc.left, relations['has_input'], mf)

            if pc.right:
                self.process_mols(pc.right, relations['has_output'], mf)
                
                                        
    def process_mf(self, xrefs, catalysis:pybiopax.biopax.Catalysis)    : 
        for xref in xrefs:
            if xref.db == 'GENE ONTOLOGY':
                self.mf_map[catalysis.controlled.uid] = xref.id
                
                
    def process_bp(self, xrefs): 
        for xref in xrefs:
            if xref.db == 'GENE ONTOLOGY':
                bp = self.add_instance_of_class(xref.id)
                self.bp_node = bp
                

    def process_mols(self, mols, relation, mf):
        for mol in mols:
            sm_node = self.add_instance_of_class(mol.display_name)
            self.add_edge(mf, relation, sm_node)
            
    
    def process_cc(self, xrefs): 
        pass
                        
            
gocam = GoCAM()
for pathway in model.get_objects_by_type(pybiopax.biopax.Pathway):
    gocam.process_pathway(pathway)
pprint.pp(nx.to_dict_of_dicts(gocam))
print(gocam.mf_map)