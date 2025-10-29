import base64
import json
import ipaddress
import os

B64_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")


def parse_kv_file(path: str) -> dict[str, str]:
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
            kv[k.strip()] = v.strip()
    return kv


def b64_decode(msg: str) -> str:
    if len(msg) % 4 != 0:
        msg += "=" * (4 - (len(msg) % 4))
    try:
        return base64.b64decode(msg).decode("utf-8", errors="ignore").strip()
    except Exception as e:
        print(f"[Warning] Base64 decoding failed. {e}")
        return ""


def read_jsonl(path: str) -> list[dict]:
    """
    Reads JSON-lines; skips malformed lines
    """
    items: list[dict[str, str | int]] = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except Exception:
                continue
    return items


def ipv4_in_cidr(ip: str, cidr: str) -> bool:
    try:
        return ipaddress.IPv4Address(ip) in ipaddress.IPv4Network(cidr, strict=False)
    except Exception:
        return False


def ipv4_cidr24(ip: str) -> str:
    """
    Returns the /24 CIDR string for a valid IPv4, or raises if invalid.
    """
    addr = ipaddress.IPv4Address(ip)
    net = ipaddress.IPv4Network(f"{addr}/24", strict=False)
    return f"{net.network_address}/24"
