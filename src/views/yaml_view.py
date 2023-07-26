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
        disp_json = self._to_minimal_json(model)
        return yaml.dump(disp_json, indent=2)     
        
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
        disp_data = {
            "pathways": []
        }

        for pathway in model.pathways:
            disp_pathway = {
                pathway.uid: []
            }

            bp = {
                "bp": pathway.biological_process.id
            }
            disp_pathway[pathway.uid].append(bp)

            disp_reactions = {
                "reactions": []
            }
            disp_pathway[pathway.uid].append(disp_reactions)

            for reaction in pathway.reactions:
                disp_reaction = {
                    reaction.uid: []
                }

                disp_controller = {
                   "controllers": [c.id for c in reaction.controllers]
                }
                disp_reaction[reaction.uid].append(disp_controller)

                disp_inputs = {
                    "inputs": [input_term.id for input_term in reaction.has_inputs]
                }
                disp_reaction[reaction.uid].append(disp_inputs)

                disp_outputs = {
                    "outputs": [output_term.id for output_term in reaction.has_outputs]
                }
                disp_reaction[reaction.uid].append(disp_outputs)

                disp_reactions["reactions"].append(disp_reaction)

            disp_data["pathways"].append(disp_pathway)

        return disp_data

  