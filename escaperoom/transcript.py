from typing import Optional, Iterable
import os


class Transcript:
    """
    Transcript logger.
    Only rooms and the Final Gate should write grading tags here.
    """

    def __init__(self, path: Optional[str]):
        self.path = path
        self._buf: list[str] = []

    def write(self, line: str) -> None:
        self._buf.append(line)

    def extend(self, lines: Iterable[str]) -> None:
        for ln in lines:
            self.write(ln)

    def flush(self) -> None:
        if not self.path:
            return
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("\n".join(self._buf) + "\n")

    def token(self, kind: str, value: str) -> None:
        self.write(f"TOKEN[{kind}]={value}")

    def evidence(self, kind: str, key: str, value: str) -> None:
        self.write(f"EVIDENCE[{kind}].{key}={value}")

    def final_gate(self, msg: str, expected_hmac: str) -> None:
        self.write("FINAL_GATE=PENDING")
        self.write(f"MSG={msg}")
        self.write(f"EXPECTED_HMAC={expected_hmac}")
