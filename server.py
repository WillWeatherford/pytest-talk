# -*- coding: utf-8 -*-
"""Server module to to take HTTP requests."""

import os
import socket
import sys
import time
from contextlib import closing

BUFFER_LENGTH = 8
ADDRINFO = ('127.0.0.1', 5000)

PARENT_DIR = os.path.dirname(__file__)
GRANDPARENT_DIR = os.path.join(PARENT_DIR, '..')
WEBROOT_PATH = os.path.join(GRANDPARENT_DIR, 'webroot', '')

# Unicode constants for standard re-usable parts.
CRLF = '\r\n'
GET = 'GET'
HTTP1_1 = 'HTTP/1.1'
HOST = 'Host: '
CONTENT_TYPE = 'Content-Type: {}'
CONTENT_LENGTH = 'Content-Length: {}'

TEXT_HTML = 'text/html; charset=utf-8'
TEXT_PLAIN = 'text/plain; charset=utf-8'

# Easy Reference dictionary with int keys for code/message part.
HTTP_CODES = {
    200: '200 OK',
    400: '400 Bad Request',
    404: '404 Not Found',
    405: '405 Method Not Allowed',
    505: '505 HTTP Version Not Supported',
}

# updated HTML templates to use unicode strings
HTML_TEMPLATE = '''
                <!DOCTYPE html>
                <html>
                  <head>
                    <meta charset="utf-8">
                    <title></title>
                  </head>
                  <body>
                    <h3>{header}</h3>
                    <ul>
                      {list_items}
                    </ul>
                  </body>
                </html>
                '''
HTML_LI_TEMPLATE = '''
                   <li><a href="{full_path}">{short_path}</a></li>
                   '''

# Throw 404 if request is not to one ofthese paths.
PATHS = {
    '/': ('Home page.', 'text/html'),
    '/signup': ('Signup page.', 'text/html'),
    '/login': ('Login page.', 'text/html'),
    '/pictures/python_photo.jpg': (b'', 'image/jpeg'),
}


def server():
    """Start a server using a socket at server.ADDRINFO."""
    serv_sock = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM,
                              socket.IPPROTO_TCP)

    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_sock.bind(ADDRINFO)
    serv_sock.listen(1)
    try:
        while True:
            conn, addr = serv_sock.accept()
            http_server(conn, addr)
    except Exception as e:
        print(e)
    finally:
        print('\nShutting down the server...\n')
        serv_sock.close()
        sys.exit()


def http_server(conn, addr):
    """Take HTTP requests and return appropriate HTTP response."""
    # with closing(conn):
    request_parts = []
    while True:
        part = conn.recv(BUFFER_LENGTH)
        request_parts.append(part)
        if len(part) < BUFFER_LENGTH:
            break
    # Immediately decode all of incoming request into unicode.
    # In future, may need to check Content-type of incoming request?
    request = b''.join(request_parts).decode('utf-8')
    print('Request received:\n{}'.format(request))
    try:
        uri = parse_request(request)
        # Here body might be a bytestring.
        body, content_type = resolve_uri(uri)
        body_length = len(body)
        response_headers = response_ok(content_type, body_length)

    except ValueError as e:
        err_code = e.args[0]
        response_headers = response_error(err_code)
        body = HTTP_CODES[err_code]

    # Re-encode into bytes on the way out.
    response_headers = response_headers.encode('utf-8')
    body = body.encode('utf-8')

    response = b''.join([response_headers, body])

    conn.sendall(response)
    conn.close()
    time.sleep(0.01)


def parse_request(request):
    """Parse client request."""
    method = ''
    uri = ''
    protocol = ''
    headers = ''

    # I was able to simplify this into one try/except block.
    # The key was to organize it by error type.
    try:
        headers, body = request.split(CRLF * 2)
        headers = headers.split(CRLF)
        try:
            first_line = headers[0]
        except IndexError:
            raise ValueError(400)
        method, uri, protocol = first_line.split()
        headers = headers[1:]
        for h in headers:
            if h.startswith(HOST):
                break
        else:
            raise ValueError(400)
    except ValueError:
        raise ValueError(400)
    if method != GET:
        raise ValueError(405)
    if protocol != HTTP1_1:
        raise ValueError(505)

    return uri


def resolve_uri(uri):
    """Return tuple of content and content type, or raise 404 error."""
    try:
        return PATHS[uri]
    except KeyError:
        raise ValueError(404)


# Response_ok doesn't parse body (might be bytes as for an image).
# References key 200 from HTTP_CODES reference dictionary.
def response_ok(content_type, body_length):
    """Return 'HTTP/1.1 200 OK' for when connection ok."""
    return CRLF.join([' '.join([HTTP1_1, HTTP_CODES[200]]),
                     CONTENT_TYPE.format(content_type),
                     CONTENT_LENGTH.format(body_length),
                     CRLF])


# Response_error take an int as err_code, to reference HTTP_CODES dict.
def response_error(err_code):
    """Return 'Internal Server Error' for when problem occurs."""
    return CRLF.join([' '.join([HTTP1_1, HTTP_CODES[err_code]]),
                     CONTENT_TYPE.format(TEXT_PLAIN),
                     CRLF])


if __name__ == '__main__':
    server()
