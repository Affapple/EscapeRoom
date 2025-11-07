from escaperoom.transcript import Transcript
from escaperoom.GameState import GameState
from escaperoom.rooms.base import Room


class FinalRoom(Room):
    """
    Room representing the final area of the escape room game
    """

    def __init__(self):
        super().__init__(
            "Final Room", "This is the final room. There are no items here."
        )

    def solve(self, state: GameState, tr: Transcript, item: str = ""):
        """
        Placeholder solve method for the final room, no action needed
        
        :param state: Current game state
        :param tr: Transcript to log actions
        :param item: Item to inspect
        """
