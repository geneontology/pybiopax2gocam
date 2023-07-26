import typing
import pybiopax
from pybiopax.biopax import Catalysis, Control, BioPaxObject
from collections import defaultdict
from src.models.biopax_model import Biopax, Controller, Pathway, Reaction, Term
from src.models.parsers.biopax_parser import BiopaxParser

ACCEPTED_DBS = ['reactome', 'uniprot',  'chebi']

class ReactomeParser(BiopaxParser):    
    def __init__(self, model):
        self._bp_node = None
        self._mf_map = {}
        self._controller_map = defaultdict(list)
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
                if isinstance(sp, Catalysis) or isinstance(sp, Control): 
                    self._process_controllers(sp)
                if isinstance(sp, Catalysis):
                    self._process_mfs(sp, self.model.objects[sp.uid])
   
    
    def _process_components(self, reaction:Reaction, components):
        reactions = list()
        
        for bpx_reaction in components:
            
            if not isinstance(bpx_reaction, pybiopax.biopax.BiochemicalReaction):
                continue
            
            mf_id = self._mf_map.get(bpx_reaction.uid, None)
          
                                   
            reaction = Reaction(uid=bpx_reaction.uid)  
            reaction.controllers = self._controller_map.get(bpx_reaction.uid, [])
            reaction.molecular_function = Term(id = mf_id)
           
            pc = self.model.objects[bpx_reaction.uid]

            if pc.left:
                reaction.has_inputs = self._process_mols(pc.left)

            if pc.right:
                reaction.has_outputs = self._process_mols(pc.right)
            
            reactions.append(reaction)
        
        return reactions
    
                                    
    def _process_mfs(self, sp, catalysis:Catalysis):                              
        if sp.control_type == 'ACTIVATION':    
            for xref in sp.xref:
                if xref.db == 'GENE ONTOLOGY':
                    self._mf_map[catalysis.controlled.uid] = xref.id                
                
                
    def _process_bp(self, xrefs)->Term:         
        for xref in xrefs:
            if xref.db == 'GENE ONTOLOGY':
                return Term(id = xref.id)
        
        return None
                

    def _process_mols(self, mols)->typing.List[Term]:
        small_mols = list()
        
        for mol in mols:            
            xrefs = [f'{v.db}:{v.id}' for v in mol.xref if v.db.lower() in ACCEPTED_DBS]            
            small_mol = Term(id=ReactomeParser.choose_entity(xrefs),
                            label=mol.display_name) 
            small_mols.append(small_mol)
            
        return small_mols
    
    
    def _process_controllers(self, sp):
        sp_uid = sp.controlled.uid    
        for controller in ReactomeParser.get_object_list(sp.controller):                  
            xrefs = [f'{v.db}:{v.id}' for v in controller.xref if v.db.lower() in ACCEPTED_DBS]            
            controller_item = Controller(control_type = sp.control_type, 
                            id=ReactomeParser.choose_entity(xrefs),
                            label=controller.display_name)
            self._controller_map[sp_uid].append(controller_item)     
    
        
    def _process_cc(self, xrefs): 
        pass


    # Helpers, we can moove these to util class
    @staticmethod 
    def get_object_list(val):
        if isinstance(val, BioPaxObject):
            return [val]
        elif isinstance(val, (list, set)):
            return [v for v in val if isinstance(v, BioPaxObject)]
        else:
            return []
    
    @staticmethod 
    def choose_entity(a):
        for item in a:
            if item.lower().startswith('chebi'):
                return item
        return a[0]