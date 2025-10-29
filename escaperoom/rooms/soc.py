import ipaddress
import re
import os

from escaperoom.transcript import Transcript
from escaperoom.GameState import GameState
from escaperoom.rooms.base import Room

FAILED_RE = re.compile(r"Failed password .* from (\d{1,3}(?:\.\d{1,3}){3})")


class SocRoom(Room):
    """
    Room representing the SOC Triage Desk containing auth.log
    """

    def __init__(self, data_dir: str):
        super().__init__("SOC Triage Desk", "Items here: auth.log")
        self.path = os.path.join(data_dir, "auth.log")

    def solve(self, state: GameState, tr: Transcript, item: str = ""):
        """
        Analyze auth.log for failed SSH login attempts to determine
        the most targeted /24 subnet and derive a token from it.
        :param state: Current game state
        :param tr: Transcript to log actions
        :param item: Item to inspect
        """
        if item.lower() not in ("auth.log", "auth", ""):
            print("Nothing interesting to inspect here.")
            return

        print("[Room SOC] Parsing logs...")
        subnet_counts: dict[str, int] = {}
        ip_counts: dict[str, int] = {}
        sample_line: str = ""
        malformed_skipped: int = 0

        if os.path.exists(self.path) or not os.path.isfile(self.path):
            print("[Warning] auth.log not found.")
            return

        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                m = FAILED_RE.search(line)
                if m is None:
                    if "Failed password" in line:
                        malformed_skipped += 1
                    continue
                ip: str = m.group(1)
                try:
                    addr = ipaddress.IPv4Address(ip)
                except ipaddress.AddressValueError:
                    malformed_skipped += 1
                    continue

                net = ipaddress.IPv4Network(f"{addr}/24", strict=False)
                subnet_key = f"{net.network_address}/24"
                subnet_counts[subnet_key] = subnet_counts.get(subnet_key, 0) + 1
                ip_counts[ip] = ip_counts.get(ip, 0) + 1
                if not sample_line:
                    sample_line = line

        if not subnet_counts:
            print("[Warning] No failed attempts found.")
            return

        # Top /24 by count; tie-break lexicographically
        top24, total_in_top24 = sorted(
            subnet_counts.items(), key=lambda kv: (-kv[1], kv[0])
        )[0]

        # Choose most frequent IP within that /24
        top_net = ipaddress.IPv4Network(top24, strict=False)
        top_ip = None
        best = (-1, "")
        for ip, cnt in ip_counts.items():
            if ipaddress.IPv4Address(ip) in top_net:
                key = (-cnt, ip)
                if key < best or top_ip is None:
                    best = key
                    top_ip = ip

        if not top_ip:
            print("[Warning] Could not determine top IP.")
            return

        last_octet = top_ip.split(".")[-1]
        token = f"{last_octet}{total_in_top24}"

        tr.token("KEYPAD", token)
        tr.evidence("KEYPAD", "TOP24", top24)
        tr.evidence("KEYPAD", "COUNT", str(total_in_top24))
        if sample_line:
            tr.evidence("KEYPAD", "SAMPLE", sample_line)
        tr.evidence("KEYPAD", "MALFORMED_SKIPPED", str(malformed_skipped))

        state.tokens["KEYPAD"] = token

        print(f"{total_in_top24} failed attempts found in {top24}")
        print(f"Top IP is {top_ip} (last octet={last_octet})")
        print(f"Token formed: {token}")
