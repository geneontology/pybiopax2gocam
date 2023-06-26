import json
import os
from dataclasses import asdict

class BiopaxView:
    
    def to_json(self, obj):
            return json.dumps(asdict(obj), indent=2)
        
    def display_results(self, data):
        print("Processed BioPAX data:")
        
        print(self.to_json(data))
        

    def write_results(self, data, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for index, item in enumerate(data):
            filename = f"output_{index}.txt"
            file_path = os.path.join(output_folder, filename)

            with open(file_path, "w") as file:
                file.write(str(item))

        print(f"Processed BioPAX data written to {output_folder}")