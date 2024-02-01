"""
Objective: server must listen on port x for requests, and forward them to applications listening on port y
any response from the applications listening on port y must be in turn forwarded back to port x.
"""
import socket


MAX_CONN = 5
PROXY_ADDR = ('localhost', 8100)
UPSTREAM_ADDR = ('localhost', 9000)


def forward_request(cs, addr):
    client_request = cs.recv(4096)
    # proxy socket
    try:
        ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ps.connect(UPSTREAM_ADDR)
        ps.sendall(client_request)

        proxy_response = b""
        while True:
            part = ps.recv(4096)
            if not part:  # No more data is being sent by the client
                break
            proxy_response += part

        print(f"response from httpserver: {proxy_response}")
        cs.sendall(proxy_response)

    finally:
        cs.close()
        ps.close()



if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Set SO_REUSEADDR option
    s.bind(PROXY_ADDR)
    s.listen(MAX_CONN)

    try:
        while True:
            # client socket
            cs, addr = s.accept()
            forward_request(cs, addr)
    finally:
        s.close()
    
