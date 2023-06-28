from dataclasses import asdict
import json
from src.views.biopax_view import BiopaxView

class JSONView(BiopaxView):
    def __init__(self, model):
        super().__init__(model)
        self.json_obj = self.to_json(model)
    def to_json(self, obj):
        return json.dumps(asdict(obj), indent=2)
        
    def convert(self):
        pass
        
    def display_results(self):
        print(self.json_obj)

  