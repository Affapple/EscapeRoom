from abc import ABCMeta, ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Set, List


@dataclass
class GameState:
    current_room: str = 'intro'
    inventory: Set[str] = field(default_factory=set)
    tokens: Dict[str, str] = field(default_factory=dict)
    flags: Dict[str, str] = field(default_factory=dict)


class Room(metaclass=ABCMeta):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def solve(self, state: GameState):
        raise NotImplementedError("Implement puzzle logic in subclasses")