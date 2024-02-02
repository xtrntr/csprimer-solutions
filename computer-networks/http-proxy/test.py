import re

pattern = b"^([^:]+): \s*(.*)"

class HTTPRequest:
    def __init__(self):
        self.headers = {}
        self.remaining = b""
        self.completed = False


    def ongoing(self):
        return not self.completed


    def parse(self, incoming):
        to_parse = self.remaining + incoming
        while to_parse.find(b"\r\n") != -1 and not self.completed:
            eol = to_parse.find(b"\r\n")
            if to_parse[eol:eol+4] == b"\r\n\r\n":
                self.completed = True
            line = to_parse[:eol]
            match = re.search(pattern, line)
            if match:
                self.headers[match.group(1).lower()] = match.group(2)
            to_parse = to_parse[eol+2:]
        self.remaining = to_parse



y = b'GET /favicon.ico HTTP/1.1\r\nHost: localhost:8101\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0\r\nAccept: image/avif,image/webp,*/*\r\nAccept-Language: en-GB,en;q=0.5\r\nAccept-Encoding: gzip, deflate, br\r\nDNT: 1\r\nSec-GPC: 1\r\nConnection: keep-alive\r\nReferer: http://localhost:8101/\r\nSec-Fetch-Dest: image\r\nSec-Fetch-Mode: no-cors\r\nSec-Fetch-Site: same-origin\r\n\r\n'
x = HTTPRequest()

n = 100
for i in range(0, len(y), n):
    substring = y[i:i+n]
    x.parse(substring)
    print(f"{substring}")
