from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Biopax:
    pathways: List['Pathway'] = field(default_factory=list)

@dataclass
class Pathway:
    id: Optional[str] = None
    label: Optional[str] = None
    reactions: List['Reaction'] = field(default_factory=list)
    relationships: List['Relationship'] = field(default_factory=list)

@dataclass
class Reaction:
    id: Optional[str] = ''
    gene_product: Optional['BiologicalProcess'] = None
    molecular_function: Optional['MolecularFunction'] = None
    biological_process: Optional['BiologicalProcess'] = None
    cellular_component: Optional['CellularComponent'] = None
    has_inputs: List['GeneProduct'] = field(default_factory=list)
    has_outputs: List['GeneProduct'] = field(default_factory=list)

@dataclass
class Relationship:
    source_reaction_id: str
    target_reaction_id: str
    relationship_type: str

@dataclass
class BiologicalProcess:
    id: str
    label: Optional[str] = None

@dataclass
class MolecularFunction:
    id: str
    label: Optional[str] = None
    reaction_id: Optional[str] = None

@dataclass
class GeneProduct:
    id: str
    label: Optional[str] = None

@dataclass
class SmallMol:
    reaction_id: Optional[str] = None
    id: Optional[str] = None
    label: Optional[str] = None

@dataclass
class CellularComponent:
    id: str
    label: Optional[str] = None