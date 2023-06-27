from src.models.processing_strategy import ProcessingStrategy
from ontobio.rdfgen.gocamgen.subgraphs import AnnotationSubgraph
from base import relations

class GOcamGenView(AnnotationSubgraph):
    def __init__(self):
        super().__init__()
        
    def convert(self, biopax_obj):
        self._convert_pathways(biopax_obj.pathways)

    def _convert_pathways(self, pathways):
        for pathway in pathways:
            self._convert_pathway(pathway)
            

    def _convert_pathway(self, pathway):        
        self._convert_object(pathway.biological_process)
        for reaction in pathway.reactions:
            self._convert_reaction(pathway, reaction)
            

    def _convert_reaction(self, pathway, reaction):
        bp = self._convert_object(pathway.biological_process)
        mf = self._convert_object(reaction.molecular_function, is_anchor=True)
        gp =  self._convert_object(reaction.gene_product)
        cc = self._convert_object(reaction.cellular_component)
        
        self._add_term_edge(mf, relations['enabled_by'], gp)
        self._add_term_edge(mf, relations['part_of'], bp)   
        self._add_term_edge(mf, relations['occurs_in'], cc)           
      
        self._convert_small_mols(mf, relations['ha_input'], reaction.has_inputs)
        self._convert_small_mols(mf, relations['ha_output'], reaction.has_outputs)
        

    def _convert_small_mols(self,  mf, relation, small_mols,):
        for small_mol in small_mols:
            node = self._convert_object(small_mol)
            self._add_term_edge(mf, relation, node)
            

    def _convert_object(self, obj, is_anchor=False):
        if obj and obj.id:
            return self.add_instance_of_class(obj.id, is_anchor)
          
    def _add_term_edge(self, source, relation, target):
        if source and target:
            self.add_edge(source, relation, target)
        
        return None
