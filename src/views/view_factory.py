
from src.models.parsers.yeast_parser import YeastParser
from src.views.gocamgen_view import GoCAMGenView
from src.views.json_view import JSONView
from src.views.vis_view import VisView
from src.views.yaml_view import YamlView


class ViewFactory:
    @staticmethod
    def create_view(view_type, model): 
        if view_type == "json":
            return JSONView(model)
        if view_type == "yaml":
            return YamlView(model)
        elif view_type == "gocamgen":
            return GoCAMGenView(model)
        elif view_type == "vis":
            return VisView(model)
       
        else:
            raise ValueError("Invalid view type")