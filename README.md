# BioPAX to GO-CAM Converter in Python

The primary objective of this project is to convert BioPAX files into the GO-CAM format using Python. This serves as a modernized and optimized rewrite of the existing BioPAX to GO-CAM conversion code, which was originally implemented in Java. The goal is to produce code that is more readable, maintainable, and efficient.

## Features

- **Parsing**: Utilize the `PyBioPAX` library to parse BioPAX data.

  - inferTransportProcess
  - inferMolecularFunctionFromEnablers
  - inferOccursInFromEntityLocations
  - inferRegulatesViaOutputRegulates
  - inferRegulatesViaOutputEnables
  - inferProvidesInput
  - inferSmallMoleculeRegulators

- **Transformation/Derivation Stage**: Implement various inference steps to transform and derive new data values.
- **Transformer Classes**: Create transformer classes, such as ReactomeTransformer, potentially using the Factory pattern if multiple transformers are needed.

## Languages and Frameworks
The project is primarily developed in Python. Key libraries and frameworks include:

- [PyBioPAX:](https://github.com/indralab/pybiopax) For parsing and processing BioPAX files.
- rdflib: For working with RDF data, aiding in generating the GO-CAM models in .ttl format.
- Ontobio: Contains GO-CAM specific functions using rdflib for quick generation of GO-CAM TTL.
- OAK: Provides ontology parsing and traversal utilities for tasks requiring GO, CHEBI, and other ontologies.


## Installation

1. Clone the repository:

``` bash
git clone https://github.com/geneontology/pybiopax2gocam.git
cd pybiopax2gocam
```

3. Install the required packages:

`pip install -r requirements.txt
`
## Usage

To run the converter, use the following command:

``` bash
python3 -m src.controllers.biopax_controller -t [parser_type] -v [view_type] -i [path_to_biopax]
```

### Arguments:

- `-t, --parser_type`: Specifies the parser type. Choices are `yeast` or `reactome`.
- `-v, --view_type`: Specifies the view type. Choices are `gocamgen`, `json`, `yaml`, or `vis`.
- `-i, --biopax_path`: Path to the BioPAX file or folder containing BioPAX files.

**Example**:

`python3 -m src.controllers.biopax_controller -t reactome -v json -i resources/test_biopax/reactome/R-HSA-204174_level3.owl
`
## Data Flow

![Dataflow Diagram](https://github.com/geneontology/pybiopax2gocam/blob/main/data/dataflowdiagram.jpg?raw=true)


## Deliverables

By the end of the project, the following deliverables are expected:

1. A rewritten BioPAX to GO-CAM converter tool in Python.
2. Comprehensive documentation detailing the usage of the converter tool.
4. Validation and testing mechanisms for the converter tool.
5. Integration with existing systems.
6. A final project report detailing the development process, challenges, and outcomes.
