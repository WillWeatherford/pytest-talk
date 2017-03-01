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
    ('/', 200, ),
    ('', 400),
]

PROTOS = [
    ('HTTP/1.1', 200),
    ('HTTP/1.0', 505),
    ('jhdo%#@#4939', 505),
    ('', 400),
]

HEADERS = [
    ('Host: example.com', 200),
    ('Host: example.com', 200),
    ('Host example.com', 400),
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


@pytest.fixture(params=TEST_CASES)
def http_request(request):
    """Return a new HTTPRequest object with given combination of args.

    This function uses the `request` fixture provided by pytest.
    Note that this is some abnormal name-spacing.
    """
    parts_codes_tuples = request.param
    possible_expected_codes = {tup[1] for tup in parts_codes_tuples}

    if possible_expected_codes == {200, }:
        expected_code = 200
    if 400 in possible_expected_codes:
        expected_code = 400
    else:
        expected_code = min(possible_expected_codes)

    parts = [tup[0] for tup in parts_codes_tuples]
    top_row = ' '.join(parts[:3])
    rest = CRLF.join(parts[3:])
    http_request = CRLF.join((top_row, rest))

    return {'http_request': http_request, 'expected_code': expected_code}


def test_http_request(http_request):
    """."""
    from client import client
    response = client(http_request['http_request'])
    assert int(response.split()[1]) == http_request['expected_code']
