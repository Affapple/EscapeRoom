from escaperoom.transcript import Transcript
from escaperoom.GameState import GameState
from escaperoom.rooms.base import Room


class IntroRoom(Room):
    def __init__(self):
        super().__init__(
            "Intro Room", "This is the intro room. There are no items here."
        )

    def solve(self, state: GameState, tr: Transcript, item: str = ""):
        pass
