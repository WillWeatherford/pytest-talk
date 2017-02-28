"""Example of how to test a simple HTTP server badly and inefficiently.

Each test function is nearly a clone of the rest, with only small differences.

There are already over 100 lines of test code, with only 7 test cases being
covered.
"""


def test_200():
    """Test that server returns a 200 response when expected."""
    from client import client
    http_request = (
        'GET / HTTP/1.1'
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        '\r\n'
        'A message body that does nothing.'
    )
    response = client(http_request)
    assert response.split()[1] == '200'


def test_400_1():
    """Test that server returns a 400 response when expected."""
    from client import client
    http_request = (
        'GET /'  # Missing Protocol
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        '\r\n'
        'A message body that does nothing.'
    )
    response = client(http_request)
    assert response.split()[1] == '400'


def test_400_2():
    """Test that server returns a 400 response when expected."""
    from client import client
    http_request = (
        'GET / HTTP/1.1'
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        # Missing extra carriage return on blank line
        'A message body that does nothing.'
    )
    response = client(http_request)
    assert response.split()[1] == '400'


def test_400_3():
    """Test that server returns a 400 response when expected."""
    from client import client
    http_request = (
        'GET HTTP/1.1'  # Missing URI
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        '\r\n'
        'A message body that does nothing.'
    )
    response = client(http_request)
    assert response.split()[1] == '400'


def test_404():
    """Test that server returns a 404 on a path that does not exist."""
    from client import client
    http_request = (
        'GET /page_does_not_exist HTTP/1.1'  # That is not a valid path
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        '\r\n'
        'A message body that does nothing.'
    )
    response = client(http_request)
    assert response.split()[1] == '404'


def test_405():
    """Test that server returns a 405 on a disallowed HTTP method."""
    from client import client
    http_request = (
        'POST /login HTTP/1.1'  # Only GET method is allowed
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        '\r\n'
        'A message body that does nothing.'
    )
    response = client(http_request)
    assert response.split()[1] == '405'


def test_505():
    """Test that server returns a 505 on a disallowed protocol."""
    from client import client
    http_request = (
        'GET /login HTTP/1.0'  # Server only supports HTTP/1.1
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        '\r\n'
        'A message body that does nothing.'
    )
    response = client(http_request)
    assert response.split()[1] == '505'
