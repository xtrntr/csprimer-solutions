"""
Ultimately, your objective will be to determine which percentage of
incoming SYN messages captured in the file were ACKed.
"""

GLOBAL_HEADER_SIZE = 24
PACKET_HEADER_SIZE = 16
LL_HEADER_SIZE = 4

f = open("synflood.pcap", 'rb')
data = f.read()

little_endian = data[:4] == b'\xd4\xc3\xb2\xa1'
endian = 'little' if little_endian else 'big'
global_header = data[:GLOBAL_HEADER_SIZE]
i = GLOBAL_HEADER_SIZE
count = ack_count = syn_count = 0

while i < len(data):
    header = data[i : i + PACKET_HEADER_SIZE]
    captured_size = int.from_bytes(header[8:12], endian)
    untruncated_size = int.from_bytes(header[12:16], endian)
    assert captured_size == untruncated_size, "packet was truncated?"
    packet_contents = data[i + PACKET_HEADER_SIZE : i + PACKET_HEADER_SIZE + captured_size]

    assert int.from_bytes(packet_contents[:LL_HEADER_SIZE], endian) == 2, "packet is not ipv4?"
    ip_header_length = (int.from_bytes(packet_contents[4:5], endian) & 0x0f) * 4
    tcp_header = packet_contents[ip_header_length + LL_HEADER_SIZE:]

    # switch to big endian now that it's TCP
    source = int.from_bytes(tcp_header[:2], 'big')
    dest = int.from_bytes(tcp_header[2:4], 'big')
    seqnum = int.from_bytes(tcp_header[4:8], 'big')
    acknum = int.from_bytes(tcp_header[8:12], 'big')
    flags = int.from_bytes(tcp_header[13:14], 'big')
    ack = flags & 0x10
    syn = flags & 0x02
    if ack != 0 and dest != 80:
        ack_count += 1
    if syn != 0 and dest == 80:
        syn_count += 1

    count += 1
    i += PACKET_HEADER_SIZE + captured_size

print(f"{count} packets parsed")
print(f"{ack_count} packets acked")
print(f"{syn_count} incoming syn packets")
print(f"{ack_count/syn_count:5f} packets acked")
