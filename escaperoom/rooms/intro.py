from escaperoom.rooms.base import Room
from escaperoom.engine import GameState
from escaperoom.transcript import Transcript


class IntroRoom(Room):
    def solve(self, state: GameState, tr: Transcript, item: str = ""):
        pass
