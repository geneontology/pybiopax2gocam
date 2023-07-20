from src.models.processing_strategy import ProcessingStrategy
from src.models.biopax_model import Relationship


IS_SMALL_MOLECULE_REGULATOR_OF = "RO:0012004"
IS_SMALL_MOLECULE_ACTIVATOR_OF = "RO:0012005"
IS_SMALL_MOLECULE_INHIBITOR_OF = "RO:0012006"


class TransformationStrategyFactory(ProcessingStrategy):
    @staticmethod
    def create_transformation_strategy(parser_type):
        if parser_type == "reactome":
            return ReactomeTransformationStrategy()
        # TODO: elif parser_type == "yeast":
        return TransformationStrategy()


class TransformationStrategy(ProcessingStrategy):
    def execute(self, data):
        #raise NotImplementedError
        return data


class ReactomeTransformationStrategy(TransformationStrategy):
    def execute(self, data):
        new_data = self._infer_transport_process(data)
        new_data = self._infer_small_molecule_regulators(data)
        return new_data

    def _infer_transport_process(self, data):
        changed_data = data
        # raise NotImplementedError
        return changed_data

    def _infer_small_molecule_regulators(self, data):
        changed_data = data
        for pathway in data.pathways:
            for rxn in pathway.reactions:
                if isinstance(rxn.controller, list):  # We should remove this conditional after changing dataclass
                    for c in rxn.controller:
                        c_entity_type = c.control_entity.id
                        # Really this should be 'if c_entity_type is descendant of chemical entity CHEBI:24431  but not
                        # descendant of nucleic acid CHEBI:33696'. For now, just see if 'CHEBI:'
                        if c_entity_type.startswith("CHEBI:"):
                            # Also figure out if + or - from ControlType
                            rel_type = IS_SMALL_MOLECULE_REGULATOR_OF
                            if c.control_type == "ACTIVATION":
                                rel_type = IS_SMALL_MOLECULE_ACTIVATOR_OF
                            elif c.control_type == "INHIBITION":
                                rel_type = IS_SMALL_MOLECULE_INHIBITOR_OF
                           
                            c.relation = rel_type
                            c.something_to_denote_object_id = rxn.molecular_function.instance_id
                        
        return changed_data
