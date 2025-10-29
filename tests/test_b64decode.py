from base64 import b64encode
from tests.TestRegistry import Test

from escaperoom.utils import b64_decode


@Test
def givenValidB64_thenReturnDecodedMessage():
    encoded = b64encode("Hello world!".encode()).decode()

    expected = "Hello world!"
    result = b64_decode(encoded)
    return result == expected
