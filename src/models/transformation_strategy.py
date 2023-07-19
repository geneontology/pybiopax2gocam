from src.models.processing_strategy import ProcessingStrategy


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
        # Iterate pathways then reactions
        # If not Catalysis and ControlType == "INHIBITION", "ACTIVATION"
        #
        # Look for RO_0002429, RO_0002430 small molecules
        return changed_data
