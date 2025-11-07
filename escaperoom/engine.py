from dataclasses import asdict
from typing import Optional, Callable

import json
import os
from escaperoom.transcript import Transcript
from escaperoom.rooms.base import Room
from escaperoom.GameState import GameState
from escaperoom.utils import parse_kv_file


class Engine:
    """Core engine for the escape room game"""

    def __init__(
        self,
        rooms: dict[str, Room],
        start: str = "intro",
        transcript_path: Optional[str] = None,
        data_dir: str = "data",
    ):
        self.state = GameState(current_room=start)
        self.rooms = rooms
        self.tr = Transcript(transcript_path)
        self.data_dir = data_dir
        self.running = True
        self.commands: dict[str, Callable[[str], None]] = {
            "help": self.cmd_help,
            "look": self.cmd_look,
            "rooms": self.cmd_rooms,
            "exits": self.cmd_rooms,
            "where": self.cmd_rooms,
            "move": self.cmd_move,
            "inspect": self.cmd_inspect,
            "use": self.cmd_use,
            "inventory": self.cmd_inventory,
            "hint": self.cmd_hint,
            "save": self.cmd_save,
            "load": self.cmd_load,
            "quit": self.cmd_quit,
            # ergonomic aliases
            "go": self.cmd_move,
            "enter": self.cmd_move,
            "ls": self.cmd_rooms,
            "examine": self.cmd_inspect,
            "read": self.cmd_inspect,
            "open": self.cmd_inspect,
            "mv": self.cmd_move,
            "q": self.cmd_quit,
        }
        self.room_order = list(rooms.keys())

    def run(self) -> None:
        """Main loop of the escape room engine"""
        print("[Game] Cyber Escape Room started. Type 'help' for commands.")
        self.cmd_look("")
        while self.running:
            try:
                room_key = self.state.current_room
                room = self._current_room_obj()
                room_title = room.name if room else "Unknown"
                line = input(f"[{room_key}: {room_title}]> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not line:
                continue
            self.dispatch(line)
        self.tr.flush()
        print("[Game] Goodbye.")

    def dispatch(self, line: str) -> None:
        """
        Dispatch a command line to the appropriate handler
        
        :param line: The input command line
        """
        parts = line.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        handler = self.commands.get(cmd)
        if handler:
            handler(arg)
        else:
            print("Unknown command. Try 'help'.")

    def _current_room_obj(self) -> Optional[Room]:
        """
        Get the current room object

        :return: The current Room object
        """
        return self.rooms.get(self.state.current_room)

    def resolve_room(self, token: str) -> Optional[Room]:
        """Resolve a room by name or number"""
        room_name = token.strip().lower()
        if room_name.isdigit():
            idx = int(room_name) - 1
            if 0 <= idx < len(self.room_order):
                room_name = self.room_order[idx]
        return self.rooms.get(room_name)

    # Commands
    def cmd_help(self, _: str) -> None:
        """
        Display help information on std io

        :param _: Unused
        """
        print(
            "Commands: look, rooms, move <room|#>, inspect <item>, use <item>, "
            "inventory, hint, save <file>, load <file>, quit"
        )

    def cmd_rooms(self, _: str) -> None:
        """
        List available rooms on the std io

        :param _: Unused
        """
        print("Rooms:")
        for i, key in enumerate(self.room_order, start=1):
            title = self.rooms[key].name
            print(f"  {i}. {key} — {title}")
        print("Use 'move <name>' or 'move <number>' to enter.")

    def cmd_look(self, _: str) -> None:
        """
        Describe the current room on the std io

        :param _: Unused
        """
        room = self._current_room_obj()
        if room:
            print(f"You are in the {room.name}.")
            print(room.description)
        else:
            print("Nowhere in particular.")

    def cmd_move(self, room_name: str) -> None:
        """
        Move to another room specified by name or number

        :param room_name: The room name or number
        """
        token = room_name.strip()
        target_room = self.resolve_room(token)

        if not token or target_room is None:
            print("That room does not exist.")
            self.cmd_rooms("")
            return

        self.state.current_room = token
        print(f"You enter the {target_room.name}.")
        print(target_room.description)

    def cmd_inspect(self, item: str) -> None:
        """
        Inspect an item in the current room

        :param item: The item to inspect
        """
        item = item.strip()
        room = self._current_room_obj()
        if not room:
            print("No room is active.")
            return
        room.solve(self.state, self.tr, item=item)

    def cmd_use(self, item: str) -> None:
        """
        Attemps to use an item in the current room

        :param item: The item to use
        """
        tool = item.strip().lower()
        if self.state.current_room == "final" and tool in ("gate", "final", "console"):
            ordered = ", ".join(
                f"{k}={self.state.tokens.get(k, '?')}"
                for k in sorted(self.state.tokens)
            )
            if ordered:
                print("Collected tokens: " + ordered)
            self.use_final_gate()
        else:
            print("Nothing happens.")

    def use_final_gate(self) -> None:
        """
        Attempt to open the final gate with the collected tokens
        """
        final_path = os.path.join(self.data_dir, "final_gate.txt")
        cfg = parse_kv_file(final_path)
        token_order = [
            t.strip() for t in cfg.get("token_order", "KEYPAD,DNS,SAFE,PID").split(",")
        ]
        group_id = cfg.get("group_id", "?")
        expected_hmac = cfg.get("expected_hmac", "?")

        tokens_in_order = [self.state.tokens.get(k, "?") for k in token_order]
        msg = f"{group_id}|{'-'.join(tokens_in_order)}"

        print("FINAL_GATE=PENDING")
        print(f"MSG={msg}")
        print(f"EXPECTED_HMAC={expected_hmac}")

        self.tr.final_gate(msg, expected_hmac)

    def cmd_inventory(self, _: str) -> None:
        """
        List the current inventory on the std io

        :param _: Unused
        """
        if self.state.tokens:
            keys = ", ".join(sorted(self.state.tokens.keys()))
            print(f"You currently hold: {keys}")
        else:
            print("Inventory is empty.")

    def cmd_hint(self, _: str) -> None:
        """
        Provide a hint for the current room

        :param _: Unused
        """
        print("Try 'inspect' the room’s data file to gather evidence.")

    def cmd_save(self, save_file: str = "save.json") -> None:
        """
        Save the current game state to a file

        :param save_file: The file path to save to
        """
        path = save_file.strip()
        data = asdict(self.state)
        data["inventory"] = list(self.state.inventory)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print("[Game] Progress saved.")
        except FileNotFoundError:
            print("[Warning] Save failed, file not found")

    def cmd_load(self, save_file: str = "save.json") -> None:
        """
        Attempts to load a game state from a file

        :param save_file: The file path to load from
        """
        path = save_file.strip()
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.state.current_room = data.get("current_room", "intro")
            self.state.inventory = set(data.get("inventory", []))
            self.state.tokens = dict(data.get("tokens", {}))
            self.state.flags = dict(data.get("flags", {}))
            print("[Game] Progress loaded.")
        except FileNotFoundError:
            print("[Warning] Load failed, file not found")

    def cmd_quit(self, _: str) -> None:
        """
        Quit the game
        :param _: Unused
        """
        self.running = False
