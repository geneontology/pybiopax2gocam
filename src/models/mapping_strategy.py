from src.models.processing_strategy import ProcessingStrategy

#needs cleanup
class MappingStrategy(ProcessingStrategy):
    def execute(self, data):
        #not yet implemented
        return data
    
    #Example of iterating the data model. it will know yeast or reactome, It will need mapping object
    def map_ids(self, biopax_obj, id_map):
        self._map_pathways(biopax_obj.pathways, id_map)

    def _map_pathways(self, pathways, id_map):
        for pathway in pathways:
            self._map_pathway(pathway, id_map)
            

    def _map_pathway(self, pathway, id_map):        
        self._map_object(pathway.biological_process, id_map)
        for reaction in pathway.reactions:
            self._map_reaction(reaction, id_map)
            

    def _map_reaction(self, reaction, id_map):
        self._map_object(reaction.gene_product, id_map)
        self._map_object(reaction.molecular_function, id_map)
        self._map_object(reaction.cellular_component, id_map)
        self._map_small_mols(reaction.has_inputs, id_map)
        self._map_small_mols(reaction.has_outputs, id_map)

    def _map_small_mols(self, small_mols, id_map):
        for small_mol in small_mols:
            self._map_object(small_mol, id_map)

    def _map_object(self, obj, id_map):
        if obj and obj.id in id_map:
            obj.id = id_map[obj.id]

