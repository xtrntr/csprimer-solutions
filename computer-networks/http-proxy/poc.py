import select
import socket
import re


pattern = b"^([^:]+): \s*(.*)"
PROXY_ADDR = ('localhost', 9000)
MAX_CONN = 5


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
    requests = {}

    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        for s in readable:
            print(f"processing readable socket {s}")
            if s == ss:
                cs, addr = s.accept()
                cs.setblocking(False)
                inputs.append(cs)
                requests[cs] = HTTPRequest()
            else:
                assert s in inputs
                data = s.recv(1024)
                if data:
                    req = requests[s]
                    req.parse(data)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del requests[s]
        for s in writable:
            print(f"processing writable socket {s}")
            s.send(b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n")
            outputs.remove(s)
        for s in exceptional:
            print(f"processing exceptional socket {s}")
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del requests[s]

