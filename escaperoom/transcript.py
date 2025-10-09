from escaperoom.utils import TokenType


class Transcript:
    def __init__(self, filename: str):
        self.filename = filename

    def write_token(self, type: TokenType, token: str):
        pass

    def write_evidence(self, evidence: str):
        pass

    def build_final_gate_key(self):
        pass