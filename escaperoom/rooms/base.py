from abc import ABC, abstractmethod

from escaperoom.GameState import GameState
from escaperoom.transcript import Transcript


class Room(ABC):
    """
    Abstract base class for a room in the escape room game
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def solve(self, state: GameState, tr: Transcript, item: str = "") -> None:
        """
        Abstract method that implements the logic to solve the room's challenge
        """
        ...
