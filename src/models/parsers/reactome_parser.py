import typing
import pybiopax
from src.models.biopax_model import BiologicalProcess, Biopax, GeneProduct, MolecularFunction, Pathway, Reaction, SmallMol
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

    def _process_pathway(self, pathway):        
        
        reaction = Reaction()
        if pathway.xref:
            reaction.biological_process = self._process_bp(pathway.xref)

        if pathway.pathway_order:
            self._process_step_processes(reaction, pathway.pathway_order)
        
        if pathway.pathway_component:
            self._process_components(reaction, pathway.pathway_component)
            
        return reaction
                
    
    def _process_step_processes(self, reaction, step_processes):
        for obj in step_processes:
            pc = self.model.objects[obj.uid]
            for sp in pc.step_process:
                if isinstance(sp, pybiopax.biopax.Catalysis) and sp.control_type == 'ACTIVATION':
                    self.process_mf(sp.xref, self.model.objects[sp.uid])
   
    
    def _process_components(self, reaction:Reaction, components):
        for obj in components:

            reaction.gene_product = GeneProduct(id=obj.display_name)
           
            pc = self.model.objects[obj.uid]

            if isinstance(pc, pybiopax.biopax.BiochemicalReaction):
                if pc.left:
                    reaction.has_input = self._process_mols(pc.left)

                if pc.right:
                    reaction.has_output = self._process_mols(pc.right)
                
                                        
    def process_mf(self, xrefs, catalysis:pybiopax.biopax.Catalysis): 
        for xref in xrefs:
            if xref.db == 'GENE ONTOLOGY':
                self.mf_map[catalysis.controlled.uid] = xref.id

                return MolecularFunction(id = xref.id, reaction_id=catalysis.controlled.uid)
                
                
    def _process_bp(self, xrefs)->BiologicalProcess:
         
        for xref in xrefs:
            if xref.db == 'GENE ONTOLOGY':
                return BiologicalProcess(id = xref.id)
        
        return None
                

    def _process_mols(self, mols)->typing.List[SmallMol]:
        small_mols = list()
        for mol in mols:
            small_mol = SmallMol(id=mol.display_name)
            small_mols.append(small_mol)
            
        return small_mols
    
    def _process_cc(self, xrefs): 
        pass
