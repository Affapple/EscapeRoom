import os
import string

from escaperoom.transcript import Transcript
from escaperoom.GameState import GameState
from escaperoom.rooms.base import Room
from escaperoom.utils import b64_decode, parse_kv_file


class DnsRoom(Room):
    """
    Room representing the DNS Room in the escape room game
    """

    def __init__(self, data_dir: str):
        super().__init__("DNS Closet", "Items here: dns.cfg")
        self.path = os.path.join(data_dir, "dns.cfg")

    def solve(self, state: GameState, tr: Transcript, item: str = ""):
        """
        Solve the DNS room by decoding hints from dns.cfg

        :param state: Current game state
        :param tr: Transcript to log actions
        :param item: Item to inspect
        """
        if item.lower() not in ("dns.cfg", "dns", ""):
            print("Nothing interesting to inspect here.")
            return

        print("[Room DNS] Decoding hints...")
        cfg = parse_kv_file(self.path)
        if len(cfg) == 0:
            print("[Warning] dns.cfg not found or empty.")
            return

        tag_raw = cfg.get("token_tag", "")
        tag_decoded = b64_decode(tag_raw)
        if not tag_decoded.isdigit():
            print("[Warning] token_tag did not resolve to a valid hint.")
            return
        print(f"[Room DNS] Hint tag id is: {tag_decoded}")

        sel_key = f"hint{tag_decoded}"
        if sel_key not in cfg:
            print("[Warning] Selected hint key not found in config.")
            return
        print(f"[Room DNS] Found hint key: {sel_key}")

        print(f'[Room DNS] Decoding hint line "{cfg[sel_key]}" ...')
        decoded_line = b64_decode(cfg[sel_key])
        
        if not decoded_line:
            print("[Room DNS] Selected hint did not decode.")
            print("[Room DNS] Attempting to deobfuscate using ROT13...")
            rotated_line = self.rot13(cfg[sel_key]) 
            decoded_line = b64_decode(rotated_line)
            if not decoded_line:
                print("[Room DNS] Deobfuscation failed. No valid hint found.")
                return
        
        print(f"[Room DNS] Decoded hint line: {decoded_line}")

        # Token: last word normalized
        last_word = decoded_line.split()[-1]
        token = last_word.strip(string.punctuation).lower()

        tr.write(f"TOKEN[DNS]={token}")
        tr.write(f"EVIDENCE[DNS].KEY={sel_key}")
        tr.write(f"EVIDENCE[DNS].DECODED_LINE={decoded_line}")
        state.tokens["DNS"] = token

        print(f'Decoded line: "{decoded_line}"')
        print(f"Token formed: {token}")

    def rot13(self, text: str) -> str:
        """
        Apply ROT13 cipher to the input text

        :param text: Input string
        :return: ROT13 transformed string
        """
        rot13_trans = str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"
        )
        return text.translate(rot13_trans)