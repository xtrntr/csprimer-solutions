import socket

if __name__ == "__main__":
    # server socket
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ss.bind(('127.0.0.1', 8090))

    try:
        while True:
            data, cs = ss.recvfrom(1024)
            ss.sendto(data.upper(), cs)

    finally:
        ss.close()


