from escaperoom.transcript import Transcript
from escaperoom.GameState import GameState
from escaperoom.rooms.base import Room
import os
import re

# S A  F  E {  digits - digits - digits }
SAFE_RE = re.compile(
    r"S\s*A\s*F\s*E\s*\{\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*\}", re.IGNORECASE
)


class VaultRoom(Room):
    def __init__(self, data_dir: str):
        super().__init__("Vault Corridor", "Items here: vault_dump.txt")
        self.path: str = os.path.join(data_dir, "vault_dump.txt")

    def solve(self, state: GameState, tr: Transcript, item: str = ""):
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

        a: int; b: int; c: int
        a = b = c = -1
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
