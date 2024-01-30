import sys

f = open('cases', 'rb')
lines = f.readlines()

for l in lines:
    to_truncate = int(l[0])
    cursor = 1
    count = 0
    newl = b''

    while cursor < len(l):
        b1 = int.from_bytes(l[cursor:cursor+1], 'big')
        # Determine the length of the UTF-8 character
        if (b1 & (0b1 << 7)) == 0:
            char_len = 1
        elif (b1 & (0b111 << 5)) == (0b110 << 5):
            char_len = 2
        elif (b1 & (0b1111 << 4)) == (0b1110 << 4):
            char_len = 3
        else:
            char_len = 4

        # Check if adding this character exceeds the truncation limit
        if cursor + char_len - 1 > to_truncate:
            break

        newl += l[cursor:cursor+char_len]
        cursor += char_len

    sys.stdout.buffer.write(newl + b'\n')
