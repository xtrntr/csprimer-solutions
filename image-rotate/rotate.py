f = open("teapot.bmp", 'rb')
data = f.read()

bitmap_file_header = data[0:2]
assert bitmap_file_header == b'BM'

img_size = data[2:6]
starting_address = int.from_bytes(data[10:14], "little")
header_size = int.from_bytes(data[14:18], "little")

assert header_size + 14 == starting_address

img_width      = int.from_bytes(data[18:22], "little")
img_height     = int.from_bytes(data[22:26], "little")
bits_per_pixel = int.from_bytes(data[28:30], "little")

# skipping sanity checks on extracted values
rotated = []
"""
0, 419         419, 419


0, 0           419, 0

clockwise rotation
original (419, 0) should be rotated (0, 0)
original (418, 0) should be rotated (0, 1)
...
original (1, 0) should be rotated (0, 418)
original (0, 0) should be rotated (0, 419)

original (0, 1) should be rotated (1, 419)
original (0, 2) should be rotated (2, 419)
...
original (0, 418) should be rotated (418, 419)
original (0, 419) should be rotated (419, 419)
"""

rotated = []
# o and r for original and rotated respectively
for rx in range(img_width):
    for ry in range(img_height):
        oy = rx
        ox = img_width - ry - 1 # -1 is necessary because it's 0,419 not 0,419
        n = starting_address + 3 * (img_width * ox + oy)
        #print(f"{ox}, {oy} rotated to {rx}, {ry}")
        rotated.append(data[n:n+3])
rotated = b''.join(rotated)

with open("output.bmp", 'wb') as f:
    f.write(data[:starting_address])
    f.write(rotated)
