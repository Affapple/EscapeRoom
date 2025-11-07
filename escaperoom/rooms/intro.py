from escaperoom.transcript import Transcript
from escaperoom.GameState import GameState
from escaperoom.rooms.base import Room


class IntroRoom(Room):
    """
    Room representing the introduction area of the escape room game
    """

    def __init__(self):
        super().__init__(
            "Intro Room", "This is the intro room. There are no items here."
        )

    def solve(self, state: GameState, tr: Transcript, item: str = ""):
        """
        Placeholder solve method for the intro room, no action needed
        
        :param state: Current game state
        :param tr: Transcript to log actions
        :param item: Item to inspect
        """
