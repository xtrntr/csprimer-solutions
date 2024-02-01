import sys
import tty


try:
    tty.setcbreak(sys.stdin.fileno()) # disables line buffering; allows program to read characters immediately without waiting for the user to press Enter.
    while True:
        ch = sys.stdin.read(1)
        if ch.isdigit():
            ch = int(ch)
            for _ in range(ch):
                sys.stdout.buffer.write(b'\x07')
        else:
            print(f"{ch} is not a ch.")
        sys.stdout.flush()
except KeyboardInterrupt as e:
    sys.exit(0)
