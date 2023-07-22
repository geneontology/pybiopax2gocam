from dataclasses import asdict
import yaml
from src.models.biopax_model import Biopax
from src.views.biopax_view import BiopaxView

class YamlView(BiopaxView):
    def __init__(self, model: Biopax):
        super().__init__(model)
        self.json_obj = self.to_yaml(model)
        
    def to_yaml(self, model):
        #clean_json = self._clean_json(asdict(obj))
        min_json = self._to_minimal_json(model)
        return yaml.dump(min_json, indent=2)     
        
    def convert(self):
        pass
        
    def display_results(self):
        print(self.json_obj)
        
    def _clean_json(self, json_obj):
        if isinstance(json_obj, dict):
            return {k: self._clean_json(v) for k, v in json_obj.items() if v is not None}
        elif isinstance(json_obj, list):
            return [self._clean_json(item) for item in json_obj if item is not None]
        else:
            return json_obj
        
        
    def _to_minimal_json(self, model: Biopax):
        slim_data = {
            "pathways": []
        }

        for pathway in model.pathways:
            min_pathway = {
                pathway.uid: []
            }

            bp = {
                "bp": pathway.biological_process.id
            }
            min_pathway[pathway.uid].append(bp)

            slim_reactions = {
                "reactions": []
            }
            min_pathway[pathway.uid].append(slim_reactions)

            for reaction in pathway.reactions:
                slim_reaction = {
                    reaction.uid: []
                }

                slim_controller = {
                    "control_type": reaction.control_type if reaction.control_type else '',
                    "controller": [
                        reaction.controller.id,
                        reaction.controller.relation
                    ]
                }
                slim_reaction[reaction.uid].append(slim_controller)

                slim_inputs = {
                    "inputs": [input_term.id for input_term in reaction.has_inputs]
                }
                slim_reaction[reaction.uid].append(slim_inputs)

                slim_outputs = {
                    "outputs": [output_term.id for output_term in reaction.has_outputs]
                }
                slim_reaction[reaction.uid].append(slim_outputs)

                slim_reactions["reactions"].append(slim_reaction)

            slim_data["pathways"].append(min_pathway)

        return slim_data

  