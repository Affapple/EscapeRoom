from base64 import b64encode
from tests.TestRegistry import Test

from escaperoom.utils import b64_decode


@Test
def givenValidB64_thenReturnDecodedMessage():
    encoded = b64encode("Hello world!".encode()).decode()

    expected = "Hello world!"
    result = b64_decode(encoded)
    return result == expected

@Test
def givenInvalidB64_thenReturnEmptyLine():
    encoded = "ABdaJdhuwj!d"
    result = b64_decode(encoded)
    expected = ""
    return result == expected

@Test
def givenB64WithoutPadding_thenReturnDecodedMessage():
    expected = "Hello!!"

    encoded = b64encode(expected.encode()).decode()
    encoded = encoded.rstrip("=")  # remove padding

    result = b64_decode(encoded)
    return result == expected