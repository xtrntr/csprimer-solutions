import select
import socket
import sys
import re


pattern = b"^([^:]+): \s*(.*)"
PROXY_ADDR = ('localhost', 8200)
UPSTREAM_ADDR = ('localhost', 9000)
MAX_CONN = 5


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


if __name__ == "__main__":
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Set SO_REUSEADDR option
    ss.bind(PROXY_ADDR)
    ss.listen(MAX_CONN)

    # Sockets which are ready to read from
    inputs = [ss]
    # Sockets that are ready for writing to
    outputs = []
    # Ongoing requests
    requests = {}

    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        for s in readable:
            if s == ss:
                cs, addr = s.accept()
                cs.setblocking(False)
                inputs.append(cs)
                requests[cs] = HTTPRequest()
            else:
                assert s in inputs
                data = s.recv(1024)
                req = requests[s]
                if data:
                    req.parse(data)
                    if s not in outputs and req.ongoing() == False:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)

                    del requests[s]

        for s in writable:
            ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ps.connect(UPSTREAM_ADDR)
            print(f"Connected to {UPSTREAM_ADDR}")
            ps.sendall(requests[s].raw)

            # Forward response back to client
            while True:
                data = ps.recv(512)
                log(f'   * <- {len(data)}B')
                if not data:
                    break
                log(f'<- *    {len(data)}B')
                s.send(data)

            ps.close()
            requests[s] = HTTPRequest()
            outputs.remove(s)
            if not req.keepalive():
                inputs.remove(s)
                s.close()

            print(f"open connections: {len(inputs) - 1}")

