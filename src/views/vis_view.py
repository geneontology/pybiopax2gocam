from pyvis import network as net
from base import find_relation_meta
from src.views.biopax_view import BiopaxView
from src.views.gocamgen_view import GoCAMGenView
from IPython.display import display, display_svg, display_png, display_jpeg

class VisView(BiopaxView):
    def __init__(self, model):
        super().__init__(model)
          
    def convert(self):
        pass
        
    def display_results(self):
        
        gocam = GoCAMGenView(self.model)
        gocamGraph = gocam.convert()
        
        g = net.Network(notebook=True, directed=True)

        g.from_nx(gocamGraph)
        for edge in g.edges:
            edge['color'] = find_relation_meta(edge['relation'])['color']
        
        #downloads a local untracked folder
        display(g.show('nx.html', notebook=False))

  