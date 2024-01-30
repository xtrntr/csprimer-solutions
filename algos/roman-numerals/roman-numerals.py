"""
Change the number into a string and traverse it backwards.
For each character in the string, match it to the appropriate unit map
e.g. for the first place, match it to I, II, III...
for the third place, match it to C, CC, CCC...
Return the final string of all matches appended together.
"""

units = {
    0: "",
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
    8: "VIII",
    9: "IX",
    10: "X",
    20: "XX",
    30: "XXX",
    40: "XL",
    50: "L",
    60: "LX",
    70: "LXX",
    80: "LXXX",
    90: "XC",
    100: "C",
    200: "CC",
    300: "CCC",
    400: "CD",
    500: "D",
    600: "DC",
    700: "DCC",
    800: "DCCC",
    900: "CM",
    1000: "M",
    2000: "MM",
    3000: "MMM",
}

def to_roman(n):
    nstr = str(n)
    rtn = ""
    for i, c in enumerate(nstr[::-1]):
        rtn = units[int(c) * (10 ** i)] + rtn
    return rtn


assert to_roman(39) == "XXXIX"
assert to_roman(246) == "CCXLVI"
assert to_roman(789) == "DCCLXXXIX"
assert to_roman(2421) == "MMCDXXI"
assert to_roman(160) == "CLX"
assert to_roman(207) == "CCVII"
assert to_roman(1009) == "MIX"
assert to_roman(1066) == "MLXVI"
assert to_roman(1776) == "MDCCLXXVI"
assert to_roman(2023) == "MMXXIII"
