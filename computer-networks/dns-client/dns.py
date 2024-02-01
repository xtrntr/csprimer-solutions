"""
In this problem, you will write a basic DNS client capable of querying for A records and printing the response. The objective is to expose you to another application layer protocol (alongside HTTP) and to increase your working familiarity with the socket interface.

You will also read some of an RFC (specifically RFC 1035) which is itself an important skill. We will implement a more robust and feature-rich DNS client in a later problem, where the objective will be to understand more of the subtle details of the DNS protocol itself.
"""

import socket
import struct
import random

def dns_packet(hostname):
    # header section
    txid = random.randint(0, 65535) # any number as long as it fits into 2 bytes.
    flags = 0x0100                            # dns query. rd set to 1 (9th bit)
    qdcount = 1                               # One question
    ancount = 0                               # No answers
    nscount = 0                               # No authority records
    arcount = 0                               # No additional records
    header = struct.pack(">HHHHHH", txid, flags, qdcount, ancount, nscount, arcount)

    # question section
    query_name = b''.join([bytes([len(segment)]) + segment.encode('utf-8')
                           for segment in hostname.split('.')])
    query_name += b'\x00'                    # End of the domain name

    # Type and Class for query (A record and IN class)
    query_type = 1                           # Type A (host address)
    query_class = 1                          # Class IN (Internet)
    question = query_name + struct.pack(">HH", query_type, query_class)

    return txid, header + question


def parse_name(response, offset):
    labels = []
    while True:
        length = response[offset]
        if length & 0xC0 == 0xC0:  # Check for a pointer (two highest bits set)
            pointer = struct.unpack_from(">H", response, offset)[0]
            pointer &= 0x3FFF  # Remove the two high bits
            labels.append(parse_name(response, pointer)[0])  # Recursive call
            offset += 2  # Skip the pointer field
            return '.'.join(labels), offset
        elif length == 0:
            offset += 1  # Skip the zero length
            return '.'.join(labels), offset
        else:
            offset += 1  # Skip the length byte
            labels.append(response[offset:offset+length].decode())
            offset += length


def parse_dns_response(req_txid, response):
    header = struct.unpack(">HHHHHH", response[:12])
    resp_txid = header[0]
    assert req_txid == resp_txid
    qdcount = header[2]
    ancount = header[3]

    # Skip question section
    offset = 12
    for _ in range(qdcount):
        while response[offset] != 0:
            offset += 1
        offset += 5                          # Skip the null byte and QTYPE, QCLASS

    # Answer section
    for _ in range(ancount):
        name, new_offset = parse_name(response, offset)
        type, _class, _, _, _ = struct.unpack_from(">HHHLH", response, new_offset)
        new_offset += 10                     # Move past the RR header
        if type == 1 and _class == 1:        # If it's an A record
            ip = struct.unpack_from(">BBBB", response, new_offset)
            print(f"Domain: {name}, IP Address: {'.'.join(map(str, ip))}")
        offset += rdlength


def dns(hostname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)                          # Timeout after 5 seconds
    dns_server = ('8.8.8.8', 53)
    txid, packet = dns_packet(hostname)

    try:
        s.sendto(packet, dns_server)
        response, _ = s.recvfrom(512)  # 512 bytes is the max size of a DNS response
        parse_dns_response(txid, response)
    except socket.timeout:
        print("Request timed out")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        s.close()
    

dns("wikipedia.org")
