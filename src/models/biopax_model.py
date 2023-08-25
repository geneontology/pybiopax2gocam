from dataclasses import dataclass, field
from typing import List, Optional
from pydantic.dataclasses import dataclass


@dataclass
class Term:
    uid: Optional[str] = None
    instance_id: Optional[str] = None
    type: Optional[str] = None
    id: Optional[str] = None
    label: Optional[str] = None


@dataclass
class Controller(Term):
    control_type: Optional[str] = None
    relation: Optional[str] = None


@dataclass
class Reaction:
    uid: Optional[str] = ''
    controllers: List[Controller] = field(default_factory=list)
    gene_product: Optional[Term] = None
    molecular_function: Optional[Term] = None
    cellular_component: Optional[Term] = None
    has_inputs: List[Term] = field(default_factory=list)
    has_outputs: List[Term] = field(default_factory=list)


@dataclass
class Relationship:
    source_reaction_id: str
    target_reaction_id: str
    relationship_type: str
    id: str
    label: Optional[str] = None


@dataclass
class Pathway:
    uid: Optional[str] = None
    title: Optional[str] = None
    biological_process: Optional[Term] = None
    reactions: List[Reaction] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)


@dataclass
class Biopax:
    pathways: List[Pathway] = field(default_factory=list)
