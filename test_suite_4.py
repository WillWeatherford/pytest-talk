"""."""

import pytest

CRLF = '\r\n'

TEST_CASES = [
    (
        'GET / HTTP/1.1'
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        '\r\n'
        'A message body that does nothing.',

        '200'
    ),
    (
        'GET /'  # Missing Protocol
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        '\r\n'
        'A message body that does nothing.',

        '400'
    ),
    (
        'GET / HTTP/1.1'
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        # Missing extra carriage return on blank line
        'A message body that does nothing.',

        '400'
    ),
    (
        'GET HTTP/1.1'  # Missing URI
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        '\r\n'
        'A message body that does nothing.',

        '400'
    ),
    (
        'GET /page_does_not_exist HTTP/1.1'  # That is not a valid path
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        '\r\n'
        'A message body that does nothing.',

        '404'
    ),
    (
        'POST /login HTTP/1.1'  # Only GET method is allowed
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        '\r\n'
        'A message body that does nothing.',

        '405'
    ),
    (
        'GET /login HTTP/1.0'  # Server only supports HTTP/1.1
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        '\r\n'
        'A message body that does nothing.',

        '505'
    ),
]


@pytest.fixture(params=TEST_CASES)
def http_request(request):
    """Return a new HTTPRequest object with given combination of args.

    This function uses the `request` fixture provided by pytest.
    Note that this is some abnormal name-spacing.
    """
    from client import client

    parts_and_codes = request.param
    possible_expected_codes = {tup[1] for tup in parts_and_codes}

    if possible_expected_codes == {200, }:
        expected_code = 200
    if 400 in possible_expected_codes:
        expected_code = 400
    else:
        expected_code = min(possible_expected_codes)

    parts = [tup[0] for tup in parts_and_codes]
    http_request = CRLF.join(parts)

    response = client(http_request)
    assert response.split()[1] == str(expected_code)
