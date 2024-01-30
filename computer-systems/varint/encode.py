import struct

"""
10010110 00000001        // Original inputs.
 0010110  0000001        // Drop continuation bits.
 0000001  0010110        // Convert to big-endian.
   00000010010110        // Concatenate.
 128 + 16 + 4 + 2 = 150  // Interpret as an unsigned 64-bit integer.
"""

def encode(unsigned):
    s = bin(unsigned)[2:] # get the string representation of unsigned
    rtn = b""
    while s:
        bstr = s[-7:]
        s = s[:-7]
        if len(bstr) < 7:
            bstr = bstr.rjust(7, '0')
        else:
            bstr = '1' + bstr
        rtn += int(bstr, 2).to_bytes(1, 'little')
    return rtn


def decode(bstr):
    rtn = []
    for i in range(len(bstr)):
        rtn.append(format(int.from_bytes(bstr[i:i+1], byteorder='big'), '08b')[1:])
    rtn = ''.join(rtn[::-1])
    return int(rtn, 2)


if __name__ == '__main__':
    cases = (
        ('1.uint64', b'\x01'),
        ('150.uint64', b'\x96\x01'),
        ('maxint.uint64', b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01'),
    )
    for fname, expectation in cases:
        with open(fname, 'rb') as f:
            n = struct.unpack('>Q', f.read())[0]
            assert encode(n) == expectation, encode(n)
            assert decode(encode(n)) == n
    for i in range(100000):
        assert decode(encode(i)) == i
    print('ok')
