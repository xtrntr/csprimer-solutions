import math
import struct

def conceal(s):
    # first 2 bytes identifies a signaling nan
    identifier = b'\x7f' + (0xf8 ^ len(s)).to_bytes(1, 'big')
    # last 6 bytes can be used for concealing a payload
    payload = s.encode('ascii')
    assert len(payload) <= 6
    while len(payload) < 6:
        payload = b'\x00' + payload
    rtn = struct.unpack('>d', identifier + payload)[0]
    assert math.isnan(rtn), f"{rtn} is not nan"
    return rtn

def extract(s):
    assert math.isnan(s), f"{s} is not nan"
    payload = struct.pack('>d', s)[-6:]
    rtn = b''
    for i in range(len(payload)):
        if payload[i:i+1] == b'\x00':
            continue
        return payload[i:].decode('ascii')

for i in ["a", "ab", "abc", "abcd", "abcde", "abcdef"]:
    assert extract(conceal(i)) == i, f"{i} not concealed properly"
