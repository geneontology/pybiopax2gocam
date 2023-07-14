import pprint
from ontobio.rdfgen.gocamgen.subgraphs import AnnotationSubgraph
import networkx as nx
from base import relations
from src.views.biopax_view import BiopaxView

class GoCAMGenView(BiopaxView):
    def __init__(self, model):
        self.graph = AnnotationSubgraph()
        super().__init__(model)
        
    def convert(self):
        self._convert_pathways(self.model.pathways)
        return self.graph
    
    def display_results(self):
        pprint.pp(nx.to_dict_of_dicts(self.graph))

    def _convert_pathways(self, pathways):
        for pathway in pathways:
            self._convert_pathway(pathway)

    def _convert_pathway(self, pathway):
        bp_node = self._convert_object(pathway.biological_process)
        for reaction in pathway.reactions:
            self._convert_reaction(pathway, reaction, bp_node)


    def _convert_reaction(self, pathway, reaction, bp_node):
        mf = self._convert_object(reaction.molecular_function, is_anchor=True)
        gp =  self._convert_object(reaction.controller)
        cc = self._convert_object(reaction.cellular_component)
        
        self._add_term_edge(mf, relations['enabled_by'], gp)
        self._add_term_edge(mf, relations['part_of'], bp_node)
        self._add_term_edge(mf, relations['occurs_in'], cc)           
      
        self._convert_small_mols(mf, relations['has_input'], reaction.has_inputs)
        self._convert_small_mols(mf, relations['has_output'], reaction.has_outputs)


    def _convert_small_mols(self,  mf, relation, small_mols,):
        for small_mol in small_mols:
            node = self._convert_object(small_mol)
            self._add_term_edge(mf, relation, node)
            

    def _convert_object(self, obj, is_anchor=False):
        if obj and obj.id:
            return self.graph.add_instance_of_class(obj.id, is_anchor)
          
    def _add_term_edge(self, source, relation, target):
        if source and target:
            self.graph.add_edge(source, relation, target)
        
        return None
