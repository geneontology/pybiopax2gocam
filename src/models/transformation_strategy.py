from src.models.processing_strategy import ProcessingStrategy
from src.models import biopax_model


IS_SMALL_MOLECULE_REGULATOR_OF = "RO:0012004"
IS_SMALL_MOLECULE_ACTIVATOR_OF = "RO:0012005"
IS_SMALL_MOLECULE_INHIBITOR_OF = "RO:0012006"


class TransformationStrategyFactory(ProcessingStrategy):
    @staticmethod
    def create_transformation_strategy(parser_type: str):
        if parser_type == "reactome":
            return ReactomeTransformationStrategy()
        # TODO: elif parser_type == "yeast":
        return TransformationStrategy()


class TransformationStrategy(ProcessingStrategy):
    def execute(self, data: biopax_model.Biopax):
        #raise NotImplementedError
        return data


class ReactomeTransformationStrategy(TransformationStrategy):
    def execute(self, data: biopax_model.Biopax):
        new_data = self._infer_transport_process(data)
        new_data = self._infer_small_molecule_regulators(data)
        return new_data

    def _infer_transport_process(self, data: biopax_model.Biopax):
        changed_data = data
        # raise NotImplementedError
        return changed_data

    def _infer_small_molecule_regulators(self, data: biopax_model.Biopax):
        changed_data = data
        for pathway in data.pathways:
            for rxn in pathway.reactions:
                if isinstance(rxn.controllers, list):  # We should remove this conditional after changing dataclass
                    for c in rxn.controllers:
                        c_entity_type = c.id
                        # Really this should be 'if c_entity_type is descendant of chemical entity CHEBI:24431  but not
                        # descendant of nucleic acid CHEBI:33696'. For now, just see if 'CHEBI:'
                        if c_entity_type.lower().startswith("chebi:"):
                            # Also figure out if + or - from ControlType
                            rel_type = IS_SMALL_MOLECULE_REGULATOR_OF
                            if c.control_type == "ACTIVATION":
                                rel_type = IS_SMALL_MOLECULE_ACTIVATOR_OF
                            elif c.control_type == "INHIBITION":
                                rel_type = IS_SMALL_MOLECULE_INHIBITOR_OF
                           
                            c.relation = rel_type
                        
        return changed_data
