"""
Objective: server must listen on port x for requests, and forward them to applications listening on port y
any response from the applications listening on port y must be in turn forwarded back to port x.

Objective 2: Reuse same connection for browser->proxy, not proxy->upstream.

"""
import socket
import re
import sys
from pprint import pprint


MAX_CONN = 5
PROXY_ADDR = ('localhost', 8101)
UPSTREAM_ADDR = ('localhost', 9000)
pattern = b"^([^:]+): \s*(.*)"


def log(s):
    print(s, file=sys.stderr)


class HTTPRequest:
    def __init__(self):
        self.headers = {}
        self.remaining = b""
        self.completed = False
        self.raw = b""


    def ongoing(self):
        return not self.completed


    def parse(self, incoming):
        print(f"parsing {incoming}")
        self.raw += incoming
        to_parse = self.remaining + incoming
        while to_parse.find(b"\r\n") != -1 and not self.completed:
            eol = to_parse.find(b"\r\n")
            if to_parse[eol:eol+4] == b"\r\n\r\n":
                self.completed = True
            line = to_parse[:eol]
            if not line:
                self.completed = True
                break
            match = re.search(pattern, line)
            if match:
                self.headers[match.group(1).lower()] = match.group(2).lower()
            to_parse = to_parse[eol+2:]
        self.remaining = to_parse


    def keepalive(self):
        connection = self.headers.get(b"connection")
        if connection == b"close": return False
        return True


def handle_connection(cs, addr):
    """
    1) Read and forward all data from client socket to upstream socket until request is fully parsed.
    2) Read response from upstream socket and forward it to client socket.
    3) If it's a keepalive request, loop back to the start (open a new socket for upstream connectione) and continue from step 1.
    """
    try:
        keep_alive = True
        while keep_alive:
            client_request = HTTPRequest()
            ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ps.connect(UPSTREAM_ADDR)
            print(f"Connected to {UPSTREAM_ADDR}")

            # Forward data to upstream server
            request_complete = False
            while not request_complete:
                data = cs.recv(1024)
                log(f'-> *    {len(data)}B')
                if not data:
                    keep_alive = False
                    break
                client_request.parse(data)
                request_complete = client_request.ongoing() == False
                log(f'   * -> {len(data)}B')
                ps.send(data)

            if not keep_alive:
                break

            # Forward response back to client
            while True:
                data = ps.recv(512)
                log(f'   * <- {len(data)}B')
                if not data:
                    break
                log(f'<- *    {len(data)}B')
                cs.send(data)

            ps.close()

            # Decide on keeping the connection alive based on the parsed request
            keep_alive = client_request.keepalive()

    finally:
        cs.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Set SO_REUSEADDR option
    s.bind(PROXY_ADDR)
    s.listen(MAX_CONN)

    try:
        while True:
            # client socket
            cs, addr = s.accept()
            handle_connection(cs, addr)
    finally:
        s.close()
