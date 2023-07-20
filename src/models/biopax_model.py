from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Biopax:
    pathways: List['Pathway'] = field(default_factory=list)

@dataclass
class Pathway:
    uid: Optional[str] = None
    title: Optional[str] = None
    biological_process: Optional['Term'] = None
    reactions: List['Reaction'] = field(default_factory=list)
    relationships: List['Relationship'] = field(default_factory=list)

@dataclass
class Reaction:
    uid: Optional[str] = ''
    control_type: List[str] = field(default_factory=list)
    controller: Optional['Controller'] = None
    molecular_function: Optional['Term'] = None
    cellular_component: Optional['Term'] = None
    has_inputs: List['Term'] = field(default_factory=list)
    has_outputs: List['Term'] = field(default_factory=list)

@dataclass
class Term:
    uid: Optional[str] = None
    instance_id: Optional[str] = None
    type: Optional[str] = None
    id: Optional[str] = None
    label: Optional[str] = None

@dataclass
class Relationship:
    source_reaction_id: str
    target_reaction_id: str
    relationship_type: str
    id: str
    label: Optional[str] = None
    
    
@dataclass
class Controller (Term):
    relation: Optional[str] = None
    something_to_denote_object_id: Optional[str] = None
    