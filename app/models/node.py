from dataclasses import dataclass
from typing import Optional, FrozenSet
from enum import Enum

class NodeType(Enum):
    MIN = 0
    MAX = 1

@dataclass
class State():
    pts_min: int
    pts_max: int
    pos_min: tuple[int]
    pos_max: tuple[int]
    destroyed_squares: set[tuple[int]]
    special_squares: dict[tuple, int]

@dataclass
class Node():
    type: NodeType
    parent: Optional['Node']
    state: State
    depth: int
    utility: int
    