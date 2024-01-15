import sys
import tty

tty.setcbreak(0)

while True:
    ch = sys.stdin.read(1)
    if ch.isdigit():
        ch = int(ch)
        for _ in range(ch):
            sys.stdout.buffer.write(b'\x07')
    else:
        print(f"{ch} is not a ch.")
