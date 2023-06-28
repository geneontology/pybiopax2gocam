import json
import os
from dataclasses import asdict
import pprint

class BiopaxView:
    def __init__(self, model):
        self.model = model
    
        
    def display_results(self):
        raise NotImplementedError
          
    def save(self, data, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for index, item in enumerate(data):
            filename = f"output_{index}.txt"
            file_path = os.path.join(output_folder, filename)

            with open(file_path, "w") as file:
                file.write(str(item))

        print(f"Processed BioPAX data written to {output_folder}")