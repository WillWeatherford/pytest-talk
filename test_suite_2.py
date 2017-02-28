"""A must better test suite for server.py using parameterize decorator.


"""

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
        'GET /'
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
        'A message body that does nothing.',
        400
    ),
    (

    ),
    (

    ),
]


def test_server(request, expected_code):
    from client import client
    response = client(request)
    assert response.split()[1] == '200'


def test_400_2():
    """Test that server returns a 200 response when expected."""
    from client import client
    request = (
        'GET / HTTP/1.1'
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        'A message body that does nothing.'
    )
    response = client(request)
    assert response.split()[1] == '400'


def test_400_3():
    """Test that server returns a 200 response when expected."""
    from client import client
    request = (
        'GET / HTTP/1.1'
        '\r\n'
        'Content-Type:'
        '\r\n'
        'Host: example.com'
        '\r\n'
        'A message body that does nothing.'
    )
    response = client(request)
    assert response.split()[1] == '400'


def test_404():
    from client import client
    request = (
        'GET /page_does_not_exist HTTP/1.1'
        '\r\n'
        'Content-Type:'
        '\r\n'
        'Host: example.com'
        '\r\n'
        'A message body that does nothing.'
    )
    response = client(request)
    assert response.split()[1] == '404'


def test_405():
    from client import client
    request = (
        'POST /login HTTP/1.1'
        '\r\n'
        'Content-Type:'
        '\r\n'
        'Host: example.com'
        '\r\n'
        'A message body that does nothing.'
    )
    response = client(request)
    assert response.split()[1] == '405'


def test_405():
    from client import client
    request = (
        'POST /login NotSoGreatProtocol'
        '\r\n'
        'Content-Type:'
        '\r\n'
        'Host: example.com'
        '\r\n'
        'A message body that does nothing.'
    )
    response = client(request)
    assert response.split()[1] == '505'
