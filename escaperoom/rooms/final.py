from escaperoom.transcript import Transcript
from escaperoom.rooms.base import GameState
from escaperoom.rooms.base import Room


class FinalRoom(Room):
    def __init__(self):
        super().__init__(
            "Final Room", "This is the final room. There are no items here."
        )

    def solve(self, state: GameState, tr: Transcript, item: str = ""):
        pass
