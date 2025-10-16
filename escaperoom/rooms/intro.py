from escaperoom.rooms.base import Room
from escaperoom.engine import GameState
from escaperoom.transcript import Transcript


class IntroRoom(Room):
    def __init__(self):
        super().__init__(
            "Intro Room", "This is the intro room. There are no items here."
        )

    def solve(self, state: GameState, tr: Transcript, item: str = ""):
        pass
