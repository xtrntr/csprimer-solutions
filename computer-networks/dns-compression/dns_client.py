import sys
import socket
import struct
import random

GOOGLE_PUBLIC_DNS = ('8.8.8.8', 53)


def parse_name(res, i):
    labels = []
    original = None
    while True:
        b = res[i]
        # start of a pointer
        if b & 0b11000000 == 0b11000000:
            if original is None:
                original = i + 2
            i = ((b & 0b00111111) << 8) | res[i + 1]
        # end of a label
        elif b == 0x00:
            if original is None:
                original = i + 1
            break
        # read the labels
        else:
            # move past length byte
            i += 1
            labels.append(res[i:i+b].decode('ascii'))
            print(f"labels {labels} append {res[i:i+b].decode('ascii')}")
            i += b
    return ".".join(labels), original


if __name__ == '__main__':
    hostname = sys.argv[1]
    rtype = sys.argv[2] if len(sys.argv) > 2 else "A"
    rtype = {
        "A": 1,
        "NS": 2
    }[rtype]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    xid = random.randint(0, 0xffff)
    flags = 0x0100
    query = struct.pack('!HHHHHH', xid, flags, 1, 0, 0, 0)
    qname = b''.join(
        len(p).to_bytes(1, 'big') + p.encode('ascii')
        for p in hostname.split('.')) + b'\x00'
    query += qname
    query += struct.pack('!HH', rtype, 1)
    s.sendto(query, GOOGLE_PUBLIC_DNS)
    # loop until we get the response to our answer
    while True:
        res, sender = s.recvfrom(4096)
        if sender != GOOGLE_PUBLIC_DNS:
            continue
        rxid, rflags, qdcount, ancount, _, _ = \
            struct.unpack('!HHHHHH', res[:12])
        if rxid == xid:
            break

    i = 12
    name, i = parse_name(res, i)  # skip name in question
    print(f"{name=}, {i=}")
    i += 4  # skip qtype and qclass
    for _ in range(ancount):
        name, i = parse_name(res, i)  # skip name in answer
        print(f"{name=}, {i=}")
        rtype, rclass, ttl, rdlength = struct.unpack('!HHIH', res[i:i+10])
        if rtype == 1:
            ip_addr = res[i+10:i+10+rdlength]
            print('.'.join(str(b) for b in ip_addr))
        elif rtype == 2:
            name, i = parse_name(res, i+10)  # skip name in answer
            print(f"{name=}, {i=}")
