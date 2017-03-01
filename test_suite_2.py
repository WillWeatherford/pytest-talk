"""A better test suite for server.py using pytest's parameterize decorator.

"""

# Using pytest.mark.parametrize decorator
import pytest


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
        200
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
        400
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
        400
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
        400
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
        404
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
        405
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
        505
    ),
]


@pytest.mark.parametrize('http_request, expected_code', TEST_CASES)
def test_server(http_request, expected_code):
    """Test all cases in one parameterized function."""
    from client import client
    response = client(http_request)
    assert response.split()[1] == str(expected_code)
