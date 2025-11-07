import os
import re

from escaperoom.transcript import Transcript
from escaperoom.GameState import GameState
from escaperoom.rooms.base import Room


# S A  F  E {  digits - digits - digits }
SAFE_RE = re.compile(
    r"S\s*A\s*F\s*E\s*\{\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*\}", re.IGNORECASE
)


class VaultRoom(Room):
    """
    Room representing the Vault Corridor containing vault_dump.txt
    """

    def __init__(self, data_dir: str):
        super().__init__("Vault Corridor", "Items here: vault_dump.txt")
        self.path: str = os.path.join(data_dir, "vault_dump.txt")

    def solve(self, state: GameState, tr: Transcript, item: str = "") -> None:
        """
        Analyze vault_dump.txt for SAFE codes of the form SAFE{a-b-c}
        where a + b = c.
        
        :param state: Current game state
        :param tr: Transcript to log actions
        :param item: Item to inspect
        """
        if item.lower() not in ("vault_dump.txt", "vault", ""):
            print("Nothing interesting to inspect here.")
            return

        print("[Room Vault] Scanning dump for SAFE codes...")
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print("[Warning] vault_dump.txt not found.")
            return

        a: int = -1
        b: int = -1
        c: int = -1
        found: bool = False
        for m in SAFE_RE.finditer(text):
            a, b, c = map(int, m.groups())

            if a + b == c:
                found = True
                break

        if not found:
            print("[Warning] No valid SAFE{a-b-c} where a+b=c found.")
            return

        token = f"{a}-{b}-{c}"

        tr.write(f"TOKEN[SAFE]={token}")
        tr.write(f"EVIDENCE[SAFE].MATCH=SAFE{{{token}}}")
        tr.write(f"EVIDENCE[SAFE].CHECK={a}+{b}={c}")

        state.tokens["SAFE"] = token
        print(f"Found candidate: SAFE{{{token}}}")
        print(f"Validated: {a}+{b}={c}")
        print(f"Token formed: {token}")
