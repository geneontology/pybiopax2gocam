from src.models.processing_strategy import ProcessingStrategy

#needs cleanup
class MappingStrategy(ProcessingStrategy):
    def execute(self, data):
        #not yet implemented
        return data
    
    #Example of iterating the data model. it will know yeast or reactome, It will need mapping object
    def map_ids(self, biopax_obj, id_map):
        for pathway in biopax_obj.pathways:
            self.map_pathway(pathway, id_map)


    def map_pathway(self, pathway, id_map):
        if pathway.biological_process and pathway.biological_process.id in id_map:
            pathway.biological_process.id = id_map[pathway.biological_process.id]
       
        for reaction in pathway.reactions:
            self.map_reaction(reaction, id_map)        
        
       
    def map_reaction(self, reaction, id_map):
       
        if reaction.gene_product and reaction.gene_product.id in id_map:
            reaction.gene_product.id = id_map[reaction.gene_product.id]
             
        if reaction.molecular_function and reaction.molecular_function.id in id_map:
            reaction.molecular_function.id = id_map[reaction.molecular_function.id]
         
        if reaction.cellular_component and reaction.cellular_component.id in id_map:
            reaction.cellular_component.id = id_map[reaction.cellular_component.id]

        self.map_small_mols(reaction.has_inputs, id_map)
        self.map_small_mols(reaction.has_outputs, id_map)
              
   
    def map_small_mols(self, small_mols, id_map):
        for small_mol in small_mols:
            if small_mol.id in id_map:
                small_mol.id = id_map[small_mol.id]
