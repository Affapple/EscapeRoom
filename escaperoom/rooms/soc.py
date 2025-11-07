import ipaddress
import re
import os

from escaperoom.transcript import Transcript
from escaperoom.GameState import GameState
from escaperoom.rooms.base import Room



class SocRoom(Room):
    """
    Room representing the SOC Triage Desk containing auth.log
    """

    def __init__(self, data_dir: str):
        super().__init__("SOC Triage Desk", "Items here: auth.log")
        self.path = os.path.join(data_dir, "auth.log")

    def solve(self, state: GameState, tr: Transcript, item: str = "") -> None:
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

        if not os.path.exists(self.path) or not os.path.isfile(self.path):
            print("[Warning] auth.log not found.")
            return

        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                attempt_data = self._get_attempt_data(line)
                has_missing_data = any(key not in attempt_data for key in ["for", "from", "port", "protocol"])
                if has_missing_data:
                    malformed_skipped += 1
                    continue

                was_succesful = "Accepted" in attempt_data
                if was_succesful:
                    continue

                ip: str = attempt_data["from"]
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

        # To find the subnet with the most failed attempts
        top24: str = ""
        total_in_top24: int = 0
        for subnet, count in subnet_counts.items():
            if count > total_in_top24:
                top24 = subnet
                total_in_top24 = count


        # To find the most frequent IP inside that subnet
        highest_count = -1
        top_ip: str = ""
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

    def _get_attempt_data(self, line: str) -> dict[str, str]:
        """
        Transforms the line of a login attempt of auth.log
        into a key-value pairs specifying

        :param line: A line of the auth.log matching its pattern
        :return dict: Dictionary with key-value pairs of login data
        """
        try:
            daemon_info, access_data = line.split(": ", 1)
            daemon_info = daemon_info.strip()
            access_data = access_data.strip()
        except ValueError:
            return {}

        # If ssh info doesnt match pattern DATE LAB SSHD[ID]
        match = re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|([+-]\d{2}:\d{2}))? .+ sshd\[\d{1,5}\]", daemon_info)
        if not match:
            return {}
        
        data_iterator = iter(access_data.split())
        data = dict(zip(data_iterator, data_iterator))

        return data