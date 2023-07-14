import typing
import pybiopax
from src.models.biopax_model import Biopax, Pathway, Reaction, Term
from src.models.parsers.biopax_parser import BiopaxParser


class ReactomeParser(BiopaxParser):    
    def __init__(self, model):
        self.bp_node = None
        self.mf_map = {}
        super().__init__(model)          
        
    def parse(self):
        
        pathways = list()
        for pathway in self.model.get_objects_by_type(pybiopax.biopax.Pathway):
            pathways.append(self._process_pathway(pathway))
            
        return Biopax(pathways=pathways)

    def _process_pathway(self, bpx_pathway):        
        
        pathway = Pathway(uid = bpx_pathway.uid)
        
        if bpx_pathway.xref:
            pathway.biological_process = self._process_bp(bpx_pathway.xref)
        
        if bpx_pathway.pathway_order:
            self._process_step_processes(bpx_pathway.pathway_order)
        
        if bpx_pathway.pathway_component:
            pathway.reactions = self._process_components(pathway, bpx_pathway.pathway_component)
            
        return pathway
                
    
    def _process_step_processes(self, step_processes):
        for obj in step_processes:
            pc = self.model.objects[obj.uid]
            for sp in pc.step_process:
                if isinstance(sp, pybiopax.biopax.Catalysis) and sp.control_type == 'ACTIVATION':
                    self.process_mf(sp.xref, self.model.objects[sp.uid])
   
    
    def _process_components(self, reaction:Reaction, components):
        reactions = list()
        
        for bpx_reaction in components:
            mf_id = self.mf_map.get(bpx_reaction.uid, None)
            
            if not isinstance(bpx_reaction, pybiopax.biopax.BiochemicalReaction):
                continue
            
            reaction = Reaction(uid=bpx_reaction.uid)
            reaction.controller = Term(id=bpx_reaction.display_name)
            reaction.molecular_function = Term(id = mf_id)
           
            pc = self.model.objects[bpx_reaction.uid]

            if pc.left:
                reaction.has_inputs = self._process_mols(pc.left)

            if pc.right:
                reaction.has_outputs = self._process_mols(pc.right)
            
            reactions.append(reaction)
        
        return reactions
    
                                    
    def process_mf(self, xrefs, catalysis:pybiopax.biopax.Catalysis): 
        for xref in xrefs:
            if xref.db == 'GENE ONTOLOGY':
                self.mf_map[catalysis.controlled.uid] = xref.id                
                
                
    def _process_bp(self, xrefs)->Term:
         
        for xref in xrefs:
            if xref.db == 'GENE ONTOLOGY':
                return Term(id = xref.id)
        
        return None
                

    def _process_mols(self, mols)->typing.List[Term]:
        small_mols = list()
        for mol in mols:
            small_mol = Term(id=mol.display_name)
            small_mols.append(small_mol)
            
        return small_mols
    
    def _process_cc(self, xrefs): 
        pass

    