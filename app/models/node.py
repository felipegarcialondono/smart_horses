from dataclasses import dataclass
from typing import Optional
from enum import Enum

class TypeNode(Enum):
    MIN = 0
    MAX = 1

@dataclass
class Node():
    type: TypeNode
    depth: int
    utility: float
    parent: Optional['Node']
