from abc import ABC, abstractmethod

from escaperoom.GameState import GameState
from escaperoom.transcript import Transcript
class Room(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def solve(self, state: GameState, tr: Transcript, item: str = "") -> None: ...
