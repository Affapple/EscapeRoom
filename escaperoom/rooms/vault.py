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

        found_codes = []
        for m in SAFE_RE.finditer(text):
            part1, part2, part3 = m.groups()
            a = int(part1)
            b = int(part2)
            c = int(part3)
            
             # Saving (a, b, c) and the raw matched text
            raw_text = m.group(0)
            found_codes.append((a, b, c, raw_text))

        # Now keeping only those where a + b = c
        valid = []
        for (a, b, c, raw_text) in found_codes:
            if a + b == c:
                valid.append((a, b, c, raw_text))

        if len(valid) == 0:
            print("[Warning] No valid SAFE{a-b-c} where a+b=c found.")
            return

        # Picking the first valid 
        a, b, c, raw = valid[0]

        token = f"{a}-{b}-{c}"

        tr.write(f"TOKEN[SAFE]={token}")
        tr.write(f"EVIDENCE[SAFE].MATCH=SAFE{{{token}}}")
        tr.write(f"EVIDENCE[SAFE].CHECK={a}+{b}={c}")

        state.tokens["SAFE"] = token
        print(f"Found candidate: SAFE{{{token}}}")
        print(f"Validated: {a}+{b}={c}")
        print(f"Token formed: {token}")
