import argparse
import os
from pybiopax.api import model_from_owl_file
from src.models.mapping_strategy import MappingStrategy
from src.models.derivation_strategy import DerivationStrategy
from src.models.parsers.parser_factory import ParserFactory
from src.views.biopax_view import BiopaxView


class BiopaxController:
    def __init__(self):
        self.parser_factory = ParserFactory()
        self.mapping_strategy = MappingStrategy()
        self.derivation_strategy = DerivationStrategy()
        self.view = BiopaxView()

    def process_biopax_files(self, parser_type, path):
        if os.path.isfile(path):
            biopax_data = self.process_biopax_file(parser_type, path)
        elif os.path.isdir(path):
            # Process files in a folder
            file_paths = self.get_biopax_files(path)
            biopax_data = []
            for file_path in file_paths:
                data = self.process_biopax_file(parser_type, file_path)
                biopax_data.append(data)
        else:
            print(f"Invalid path: {path}")
            return

        mapped_data = self.mapping_strategy.execute(biopax_data)
        derived_data = self.derivation_strategy.execute(mapped_data)
        self.view.display_results(derived_data)

    def process_biopax_file(self, parser_type, file_path):
        model = model_from_owl_file(file_path, encoding="utf8")
        parser = self.parser_factory.create_parser(parser_type, model)
        return parser.parse()

    def get_biopax_files(self, folder):
        biopax_files = []
        for file_name in os.listdir(folder):
            if file_name.endswith(".owl"):
                file_path = os.path.join(folder, file_name)
                biopax_files.append(file_path)
        return biopax_files


def main():
    parser = argparse.ArgumentParser(description="BioPAX Parser")
    parser.add_argument('-t', dest='parser_type', required=True, help="Parser type (e.g., yeast, reactome)")
    parser.add_argument('-i', dest='biopax_path', required=True, help="File or Folder containing BioPAX file(s)")
    args = parser.parse_args()

    controller = BiopaxController()
    biopax_path = args.biopax_path

    if os.path.isdir(biopax_path):
        print(f'{biopax_path} is a directory containing BioPAX files.')
        controller.process_biopax_files(args.parser_type, biopax_path)
    elif os.path.isfile(biopax_path):
        print(f'{biopax_path} is a BioPAX file.')
        controller.process_biopax_files(args.parser_type, biopax_path)
    else:
        print(f"Invalid path: {biopax_path}")


if __name__ == '__main__':
    main()