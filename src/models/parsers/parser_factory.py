from src.models.parsers.reactome_parser import ReactomeParser
from src.models.parsers.yeast_parser import YeastParser


class ParserFactory:
    @staticmethod
    def create_parser(parser_type, model):
        if parser_type == "reactome":
            return ReactomeParser(model)
        elif parser_type == "yeast":
            return YeastParser(model)
        else:
            raise ValueError("Invalid parser type")