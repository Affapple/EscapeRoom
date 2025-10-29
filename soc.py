from escaperoom.transcript import Transcript
from escaperoom.rooms.base import GameState
from escaperoom.rooms.base import Room
import ipaddress
import re
import os

FAILED_RE = re.compile(r"Failed password .* from (\d{1,3}(?:\.\d{1,3}){3})")


class SocRoom(Room):
    def __init__(self, data_dir: str):
        super().__init__("SOC Triage Desk", "Items here: auth.log")
        self.path = os.path.join(data_dir, "auth.log")

    def solve(self, state: GameState, tr: Transcript, item: str = ""):
        if item.lower() not in ("auth.log", "auth", ""):
            print("Nothing interesting to inspect here.")
            return

        print("[Room SOC] Parsing logs...")
        subnet_counts: dict[str, int] = {}
        ip_counts: dict[str, int] = {}
        sample_line = ""
        malformed_skipped = 0
        top24 = None
        total_in_top24 = 0
        top_ip = None
        highest_count = -1
        # Reading and processing the log file
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.rstrip("\n")
                    m = FAILED_RE.search(line)
                    if not m:
                        if "Failed password" in line:
                            malformed_skipped += 1
                        continue
                    ip = m.group(1)
                    try:
                        addr = ipaddress.IPv4Address(ip)
                    except Exception:
                        malformed_skipped += 1
                        continue

                    net = ipaddress.IPv4Network(f"{addr}/24", strict=False)
                    subnet_key = f"{net.network_address}/24"
                    #counts how many failed attempts came from that subnet.
                    subnet_counts[subnet_key] = subnet_counts.get(subnet_key, 0) + 1
                    #counts repeated failed attempts from each IP.
                    ip_counts[ip] = ip_counts.get(ip, 0) + 1
                    if not sample_line:
                        sample_line = line
        except FileNotFoundError:
            print("[Warning] auth.log not found.")
            return

        if not subnet_counts:
            print("[Warning] No failed attempts found.")
            return

        # To find the subnet with the most failed attempts
        for subnet, count in subnet_counts.items():
            if count > total_in_top24:
                top24 = subnet
                total_in_top24 = count

        # To find the most frequent IP inside that subnet
        top_net = ipaddress.IPv4Network(top24, strict=False)
        for ip, count in ip_counts.items():
            if ipaddress.IPv4Address(ip) in top_net:
                if count > highest_count:
                    highest_count = count
                    top_ip = ip

        if not top_ip:
            print("[Warning] Could not determine top IP.")
            return

        last_octet = top_ip.split(".")[-1]
        token = f"{last_octet}{total_in_top24}"
        
        # Writing required output to the transcript
        tr.write(f"TOKEN[KEYPAD]={token}")
        tr.write(f"EVIDENCE[KEYPAD].TOP24={top24}")
        tr.write(f"EVIDENCE[KEYPAD].COUNT={total_in_top24}")
        if sample_line:
            tr.write(f"EVIDENCE[KEYPAD].SAMPLE={sample_line}")
        tr.write(f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={malformed_skipped}")

        #Storing token in the game state 
        state.tokens["KEYPAD"] = token

        print(f"{total_in_top24} failed attempts found in {top24}")
        print(f"Top IP is {top_ip} (last octet={last_octet})")
        print(f"Token formed: {token}")
