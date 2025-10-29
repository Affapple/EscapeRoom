import os
from tests.TestRegistry import Test

from escaperoom.utils import read_jsonl

## read_jsonl(path: str) -> list[dict]:

def test_read_jsonl(data, expected):
    """Creates a pipe to simulate a file reading scenario"""
    r, w = os.pipe()
    fw = os.fdopen(w, "w")
    fw.write(data + "\0") #Insert EOF
    fw.flush()
    fw.close()

    # Pass file descriptor to read_jsonl
    result = read_jsonl(r) # type: ignore
    return result == expected

@Test
def givenValidJson_thenReturnsList():
    data ="""
    { "key1": "value1", "key2": "value2", "key3": "value3" }
    { "cfg" : "data1", "num": 42}
    {}
    """
    expected = [
        {"key1": "value1", "key2": "value2", "key3": "value3"},
        {"cfg": "data1", "num": 42},
        {}
    ]
    return test_read_jsonl(data, expected)

@Test
def givenMalformedJson_thenSkipsLines():
    data ="""
    { "key1": "value1", "key2": "value2", "key3": "value3" }
    { "cfg" : "data1", "num": 42
    Not a JSON line
    {}
    """
    expected = [
        {"key1": "value1", "key2": "value2", "key3": "value3"},
        {},
    ]
    return test_read_jsonl(data, expected)

@Test
def givenEmptyJson_thenReturnsEmptyList():
    data = ""
    expected = []
    return test_read_jsonl(data, expected)

@Test
def givenOnlyMalformedJson_thenReturnsEmptyList():
    data ="""
    Not a JSON line
    Another bad line {
    Yet another one ]
    """
    expected = []
    return test_read_jsonl(data, expected)

@Test
def GiveTwoJsonInSameLine_thenReturnNoJson():
    data ="""
    { "key1": "value1", "key2": "value2", "key3": "value3" } { "cfg" : "data1", "num": 42}
    {}
    """
    expected = [{}]
    return test_read_jsonl(data, expected)