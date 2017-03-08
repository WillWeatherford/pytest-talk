"""More gooder way to test combinations of parts of test cases.

itertools.product will allow creation of every possible way all HTTP request
parts can be combined.

"""

import pytest
from itertools import product


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


TEST_CASES = product(
    METHODS, URIS, PROTOS,
    HEADERS,
    EMPTY_LINES,
    BODIES,
)


STATUS_CODE_ORDER = [
    400,
    404,
    405,
    505,
    200,
]


REASONS = {
    400: 'Bad Request',
    404: 'Not Found',
    405: 'Method Not Allowed',
    505: 'HTTP Version Not Supported',
    200: 'OK',
}


@pytest.fixture(params=TEST_CASES)
def http_request_data(request):
    """Return a new HTTPRequest object with given combination of args.

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
        'expected_reason': REASONS[expected_code],
    }


def test_http_response_code(http_request_data):
    """Test client module against all possible HTTP request combinations."""
    from client import client
    response = client(http_request_data['http_request'])
    assert int(response.split()[1]) == http_request_data['expected_code']


def test_http_response_reason(http_request_data):
    """Test client module against all possible HTTP request combinations."""
    from client import client
    response = client(http_request_data['http_request'])

    response_top_row = response.split(CRLF)[0]
    reason = ' '.join(response_top_row.split()[2:])

    assert reason == http_request_data['expected_reason']
