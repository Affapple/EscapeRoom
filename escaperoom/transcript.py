from typing import Optional, Iterable
import os


class Transcript:
    """
    Transcript logger
    Only rooms and the Final Gate should write here
    """

    def __init__(self, path: Optional[str]):
        self.path = path
        self._buf: list[str] = []

    def write(self, line: str) -> None:
        """
        Write a single lie to the transcript buffer
        
        :param line: Line to write
        """
        self._buf.append(line)

    def extend(self, lines: Iterable[str]) -> None:
        """
        Write multiple lines to the transcript buffer

        :param lines: Iterable object containing lines to write on the buffer
        """
        for ln in lines:
            self.write(ln)

    def flush(self) -> None:
        """
        Flush the transcript buffer to a file
        """
        if not self.path:
            return
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("\n".join(self._buf) + "\n")

    def token(self, kind: str, value: str) -> None:
        """
        Write a token entry to the transcript

        :param kind: Token kind
        :param value: Token value
        """
        self.write(f"TOKEN[{kind}]={value}")

    def evidence(self, kind: str, key: str, value: str) -> None:
        """
        Write an evidence entry to the transcript

        :param kind: Evidence kind
        :param key: Evidence key
        :param value: Evidence value
        """
        self.write(f"EVIDENCE[{kind}].{key}={value}")

    def final_gate(self, msg: str, expected_hmac: str) -> None:
        """
        Write the final gate attempt to the transcript

        :param msg: Final gate message
        :param expected_hmac: Expected HMAC value
        """
        self.write("FINAL_GATE=PENDING")
        self.write(f"MSG={msg}")
        self.write(f"EXPECTED_HMAC={expected_hmac}")
