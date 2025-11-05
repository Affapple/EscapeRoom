import os
from tests.TestRegistry import Test

from escaperoom.utils import parse_kv_file


def test_parse_kv_file(data, expected):
    """Creates a pipe to simulate a file reading scenario"""
    r, w = os.pipe()
    fw = os.fdopen(w, "w")
    fw.write(data + "\0")  # Insert EOF
    fw.flush()
    fw.close()

    # Pass file descriptor to parse_kv_file
    result = parse_kv_file(r)  # type: ignore
    return result, result == expected


@Test
def givenValidKVFile_thenReturnDict():
    data = """
    key1=value1
    key2 = value2
    key3=value3
    """
    expected = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
    }
    result, passed = test_parse_kv_file(data, expected)
    return passed


@Test
def givenKVFileWithComments_thenIgnoreComments():
    data = """
    # This is a comment
    key1=value1 # Inline comment
    key2 = value2
    # Another comment
    key3=value3
    """

    expected = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
    }

    result, passed = test_parse_kv_file(data, expected)
    return passed


@Test
def givenKVFileWithEmptyLines_thenIgnoreEmptyLines():
    data = """

    key1=value1

    key2 = value2

    key3=value3

    """
    expected = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
    }
    result, passed = test_parse_kv_file(data, expected)
    return passed


@Test
def givenKVFileWithInvalidLines_thenIgnoreLines():
    data = """
    key1=value1
    invalid_line
    key2 = value2
    another_invalid_line
    key3=value3
    """
    expected = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
    }
    result, passed = test_parse_kv_file(data, expected)
    return passed


@Test
def givenRepeatedKeys_thenLastValueWins():
    data = """
    key1=value1
    key2=value2
    key1=value3
    key3=value4
    key2=value5
    """
    expected = {
        "key1": "value3",
        "key2": "value5",
        "key3": "value4",
    }
    result, passed = test_parse_kv_file(data, expected)
    return passed


@Test
def givenKVFileWithRepeatedEquals_thenSplitAtFirstEquals():
    data = """
    key1=value=with=equals
    key2=another=value
    key3=simplevalue
    """
    expected = {
        "key1": "value=with=equals",
        "key2": "another=value",
        "key3": "simplevalue",
    }
    result, passed = test_parse_kv_file(data, expected)
    return passed


@Test
def givenEmptyFile_thenReturnEmptyDict():
    data = ""
    expected = {}
    result, passed = test_parse_kv_file(data, expected)
    return passed


@Test
def givenSpacesAroundKeysAndValues_thenTrimSpaces():
    data = """
        key1    =    value1    
        key2=value2
        key3    =value3
        key4=    value4
    """
    expected = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
        "key4": "value4",
    }
    result, passed = test_parse_kv_file(data, expected)
    return passed

@Test
def givenIncompleteLine_thenNoValueAttributed():
    data = """
    key1 = value1
    key2 =   
    key1 =
    key3 = value3
    """
    expected = {
        "key1" : "value1",
        "key3" : "value3"
    }
    result, passed = test_parse_kv_file(data, expected)
    return passed