
from src.models.parsers.yeast_parser import YeastParser
from src.views.gocamgen_view import GoCAMGenView
from src.views.json_view import JSONView


class ViewFactory:
    @staticmethod
    def create_view(view_type, model): 
        if view_type == "json":
            return JSONView(model)
        elif view_type == "gocamgen":
            return GoCAMGenView(model)
       
        else:
            raise ValueError("Invalid view type")