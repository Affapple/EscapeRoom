import base64
import binascii
import json
import os

B64_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")


def parse_kv_file(path: str) -> dict[str, str]:
    """
    Parses a simple key=value file; ignores comments and blank lines

    :param path: Path to the file
    :return: Dictionary of key-value pairs
    """
    kv: dict[str, str] = {}
    if not os.path.exists(path):
        return kv
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            line = line.split("#", 1)[0]  # discard comments

            k, v = line.split("=", 1)
            v = v.strip()
            if v != "":
                kv[k.strip()] = v.strip()
    return kv


def b64_decode(msg: str) -> str:
    """
    Decodes a base64-encoded string, adding padding if necessary

    :param msg: Base64-encoded string
    :return: Decoded UTF-8 string
    """
    if len(msg) % 4 != 0:
        msg += "=" * (4 - (len(msg) % 4))
    try:
        return base64.b64decode(msg).decode().strip()
    except (UnicodeDecodeError, binascii.Error) as e:
        return ""


def read_jsonl(path: str) -> list[dict]:
    """
    Parses a JSONL file into a list of dictionaries
    
    :param path: Path to the JSONL file
    :return: List of dictionaries containing the parsed JSON objects
    """
    items: list[dict[str, str | int]] = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return items
