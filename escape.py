import argparse
from escaperoom.engine import Engine, Room
from escaperoom.rooms.soc import SocRoom
from escaperoom.rooms.dns import DnsRoom
from escaperoom.rooms.vault import VaultRoom
from escaperoom.rooms.malware import MalwareRoom
from escaperoom.rooms.intro import IntroRoom
from escaperoom.rooms.final import FinalRoom


def build_rooms(data_dir: str):
    return {
        "intro": IntroRoom("Intro Lobby", "Doors: soc, dns, vault, malware, final"),
        "soc": SocRoom(data_dir),
        "dns": DnsRoom(data_dir),
        "vault": VaultRoom(data_dir),
        "malware": MalwareRoom(data_dir),
        "final": FinalRoom("Final Gate", "The console asks for proof."),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="intro")
    ap.add_argument("--transcript", default="run.txt")
    ap.add_argument("--data", default="data")
    args = ap.parse_args()
    engine = Engine(
        build_rooms(args.data),
        start=args.start,
        transcript_path=args.transcript,
        data_dir=args.data,
    )
    engine.run()


if __name__ == "__main__":
    main()
