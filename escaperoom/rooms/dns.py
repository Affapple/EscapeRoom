from escaperoom.engine import Room, GameState, Transcript
from escaperoom.utils import b64_loose_decode
import os
import string


class DnsRoom(Room):
    def __init__(self, data_dir: str):
        super().__init__("DNS Closet", "Items here: dns.cfg")
        self.path = os.path.join(data_dir, "dns.cfg")

    def solve(self, state: GameState, tr: Transcript, item: str = ""):
        if item.lower() not in ("dns.cfg", "dns", ""):
            print("Nothing interesting to inspect here.")
            return

        print("[Room DNS] Decoding hints...")
        cfg = self.__parse_cfg(self.path)
        if not cfg:
            print("[Warning] dns.cfg not found or empty.")
            return

        tag_raw = cfg.get("token_tag", "")
        tag_decoded = b64_loose_decode(tag_raw).strip()
        sel_key = f"hint{tag_decoded}" if tag_decoded.isdigit() else None
        if not sel_key or sel_key not in cfg:
            print("[Warning] token_tag did not resolve to a valid hint.")
            return

        decoded_line = b64_loose_decode(cfg[sel_key]).strip()
        if not decoded_line:
            print("[Warning] Selected hint did not decode.")
            return

        # Token: last word normalized
        last_word = decoded_line.split()[-1]
        token = last_word.strip(string.punctuation).lower()

        tr.write(f"TOKEN[DNS]={token}")
        tr.write(f"EVIDENCE[DNS].KEY={sel_key}")
        tr.write(f"EVIDENCE[DNS].DECODED_LINE={decoded_line}")
        state.tokens["DNS"] = token

        print(f'Decoded line: "{decoded_line}"')
        print(f"Token formed: {token}")

    def __parse_cfg(self, path: str) -> dict[str, str]:
        cfg: dict[str, str] = {}
        if not os.path.exists(path):
            return cfg
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                cfg[k.strip().lower()] = v.strip()
        return cfg
