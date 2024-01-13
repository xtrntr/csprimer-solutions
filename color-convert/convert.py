"""
You should try to solve the problem in a way where you do the hexadecimal to decimal conversion with minimal use of library functions.
"""

import sys

mapping = {
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15
}


def hex_to_rgb(hexstr):
    def convert(hex):
        if len(hex) == 1:
            hex *= 2
        rtn = mapping[hex[0]] * 16 if hex[0] in mapping else int(hex[0]) * 16
        rtn += mapping[hex[1]] if hex[1] in mapping else int(hex[1])
        return int(rtn)

    rtn = ""
    idx = 0
    while idx < len(hexstr):
        if hexstr[idx] == "#":
            # when are regexs better here?
            count = 0
            idx += 1
            while idx < len(hexstr) and (hexstr[idx].isdigit() or hexstr[idx].upper() in mapping):
                idx += 1
                count += 1
            if count == 3:
                rgb = [convert(hexstr[x].upper()) for x in range(idx-count, idx)]
                rtn += f"rgb({rgb[0]} {rgb[1]} {rgb[2]})"
            elif count == 4:
                rgb = [convert(hexstr[x].upper()) for x in range(idx-count, idx-1)]
                rtn += f"rgba({rgb[0]} {rgb[1]} {rgb[2]} / {convert(hexstr[idx-1:idx]) / 255:.5f})"
            elif count == 6:
                rgb = [convert(hexstr[x:x+2].upper()) for x in range(idx-count, idx, 2)]
                rtn += f"rgb({rgb[0]} {rgb[1]} {rgb[2]})"
            elif count == 8:
                rgb = [convert(hexstr[x:x+2].upper()) for x in range(idx-count, idx-2, 2)]
                rtn += f"rgba({rgb[0]} {rgb[1]} {rgb[2]} / {convert(hexstr[idx-2:idx]) / 255:.5f})"
            else:
                rtn += hexstr[idx-count-1:idx]
        else:
            rtn += hexstr[idx]
            idx += 1
    return rtn


if __name__ == "__main__":
    css_input = sys.stdin.read()
    sys.stdout.write(hex_to_rgb(css_input))
