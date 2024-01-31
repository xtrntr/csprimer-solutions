import socket
import sys
import os
import json


def handle_client(cs, addr):
    try:
        while True:
            data = cs.recv(4096)
            if not data:
                break

            headers = data.decode().split("\r\n")[1:]
            headers = [h.split(":", 1) for h in headers if len(h.split(":", 1)) > 1]
            headers_json = {h[0]: h[1] for h in headers}

            content = json.dumps(headers_json)
            length = len(content)
            response = f"""\
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: {length}

{content}
""".encode("utf-8")

            print("Sending back message:", response)
            cs.sendto(response, addr)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    finally:
        cs.close()

if __name__ == "__main__":
    # server socket
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.bind(('127.0.0.1', 8110))
    ss.listen(5)

    try:
        while True:
            # client socket
            cs, addr = ss.accept()
            handle_client(cs, addr)

    finally:
        ss.close()
