"""More scalable way to to test many combinations of test cases.

`itertools.product` will allow creation of every possible way all HTTP request
parts can be combined.

`pytest.fixture` creates a re-usable object containing test case information.

The `params` keyword argument to `pytest.fixture` allows the test runner to
iterate over a given iterable of test cases.
"""

import pytest
import itertools


CRLF = '\r\n'


METHODS = [
    ('GET', 200),
    ('POST', 405),
    ('DELETE', 405),
    ('jslalsijhr;;', 405),
]

URIS = [
    ('/', 200),
    ('/' + CRLF, 400),
    ('', 400),
]

PROTOS = [
    ('HTTP/1.1' + CRLF, 200),
    ('HTTP/1.1', 400),
    ('HTTP/1.0'  + CRLF, 505),
    ('vhdo%#@#4939'  + CRLF, 505),
    ('', 400),
]

HEADERS = [
    ('Host: example.com' + CRLF, 200),
    ('Host: example.com' + CRLF + 'Content-Type: text/html' + CRLF, 200),
    ('Host example.com'  + CRLF, 400),
    ('', 400),
]

EMPTY_LINES = [
    (CRLF, 200),
    ('p40kdnad', 400),
    ('', 400),
]

BODIES = [
    ('', 200),
    ('Some HTML', 200),
]


# Create iterator of every possible combination of HTTP request parts.
# This ensures that our HTTP server is robust enough to correctly parse a huge
# variety of incorrectly formed HTTP requests.

TEST_CASES = itertools.product(
    METHODS, URIS, PROTOS,
    HEADERS,
    EMPTY_LINES,
    BODIES,
)


# The design of our HTTP server specifies that HTTP error codes should be
# returned with a particular priority order.
# e.g. if a HTTP request is so bad that it could return a 400, 404 or 405, it
# should return a 400.
# We should be and are testing to make sure this priority order is correct.
STATUS_CODE_ORDER = [
    400,
    404,
    405,
    505,
    200,
]


@pytest.fixture(params=TEST_CASES)
def http_request_data(request):
    """Return a dictionary of data pertaining to the current test case.

    This function uses the `request` fixture provided by pytest. `request`
    gives access to meta information about the tests being run.

    request.param is one item in the iterable passed to the `params` keyword
    argument to `pytest.fixture` decorator.
    """
    parts_codes_tuples = request.param

    possible_expected_codes = {tup[1] for tup in parts_codes_tuples}
    parts = [tup[0] for tup in parts_codes_tuples]

    # Some logic to simply determine which HTTP status code is expected, based
    # on predetermined constant.
    for code in STATUS_CODE_ORDER:
        if code in possible_expected_codes:
            expected_code = code
            break

    top_row = ' '.join(parts[:3])
    rest = ''.join(parts[3:])
    http_request = top_row + rest

    return {
        'http_request': http_request,
        'expected_code': expected_code,
    }


def test_http_response(http_request_data):
    """Test client module against all possible HTTP request combinations."""
    from client import client
    response = client(http_request_data['http_request'])
    assert int(response.split()[1]) == http_request_data['expected_code']
