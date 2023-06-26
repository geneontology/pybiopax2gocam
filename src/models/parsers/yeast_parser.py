from src.models.parsers.biopax_parser import BiopaxParser

class YeastParser(BiopaxParser):

    def __init__(self, model):
        self.bp_node = None
        self.mf_map = {}
        super().__init__(model)    


    def parse(self):
        raise NotImplementedError