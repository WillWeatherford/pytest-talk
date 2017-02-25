"""Example of how to test a simple HTTP server badly and inefficiently."""


def test_good_request():
    """Test that server returns a 200 response when expected."""
    from client import client
    request = (
        'GET / HTTP/1.1'
        '\r\n'
        'Content-Type: text/html'
        '\r\n'
        'Host: example.com'
        '\r\n'
        '\r\n'
        'A message body that does nothing.'
    )
    response = client(request)
    try:
        assert response.split()[1] == '200'
    except IndexError:
        print(response)
