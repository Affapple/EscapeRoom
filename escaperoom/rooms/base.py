from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from escaperoom.transcript import Transcript


@dataclass
class GameState:
    current_room: str = "intro"
    inventory: set[str] = field(default_factory=set)
    tokens: dict[str, str] = field(default_factory=dict)
    flags: dict[str, str] = field(default_factory=dict)


class Room(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def solve(self, state: GameState, tr: Transcript, item: str = "") -> None: ...
