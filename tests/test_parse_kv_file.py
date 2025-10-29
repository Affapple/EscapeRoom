import os
from tests.TestRegistry import Test

from escaperoom.utils import parse_kv_file

## parse_kv_file(path: str) -> dict[str, str]:

def test_parse_kv_file(data, expected):
    """Creates a pipe to simulate a file reading scenario"""
    r, w = os.pipe()
    fw = os.fdopen(w, "w")
    fw.write(data + "\0") #Insert EOF
    fw.flush()
    fw.close()

    # Pass file descriptor to parse_kv_file
    result = parse_kv_file(r) # type: ignore 
    return result == expected
