#An Echo server is a program that returns the data that it receives.
import socket            
class TCPServer:
    def __init__(self, host ='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print("Listening at", s.getsockname())

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            data = conn.recv(1024)

            response = self.handle_request(data)

            conn.sendall(response)
            conn.close()

    def handle_request(self, data):
        """Handles incoming data and returns a response.
        Override this in subclass.
        """
        return data
    
class HTTPServer(TCPServer):
    headers = {
        'Server': 'Basic Server',
        'Content-Type': 'text/html',
    }

    status_codes = {
        200: 'OK',
        401: 'unauthorized',
        403: 'forbidden',
        404: 'Not Found',
        504: 'gateway timeout'
    }

    def handle_request(self, data):
        """Handles the incoming request.
        Compiles and returns the response
        """

        response_line = self.response_line(status_code=200)

        response_headers = self.response_headers()

        blank_line = b"\r\n"

        response_body = b"""
            <html>
                <body>
                    <h1>Request received!</h1>
                </body>
            </html>
        """

        return b"".join([response_line, response_headers, blank_line, response_body])

    def response_line(self, status_code):
        """Returns response line"""
        reason = self.status_codes[status_code]
        line = "HTTP/1.1 %s %s\r\n" % (status_code, reason)

        return line.encode() # call encode to convert str to bytes

    def response_headers(self, extra_headers=None):
        """Returns headers
        The `extra_headers` can be a dict for sending 
        extra headers for the current response
        """
        headers_copy = self.headers.copy() # make a local copy of headers

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""

        for h in headers_copy:
            headers += "%s: %s\r\n" % (h, headers_copy[h])

        return headers.encode() # call encode to convert str to bytes
        

if __name__ == '__main__':
    server = HTTPServer()
    server.start()