"""
Iterate over the string character by character.
For each character, we note whether it is an opening or closing bracket.
If it's an opening bracket, we add it to the stack.
If it's a closing bracket, we check if the last added item to the stack is a match. If not, we return False
When we reach the end of this string, if the stack is empty, we have a valid string.
"""

def is_valid(s):
    stack = []
    match = {
        "{": "}",
        "[": "]",
        "(": ")"
    }
    for c in s:
        if c in match:
            stack.append(c)
        else:
            if (not stack) or match[stack.pop()] != c:
                return False

    return (not stack)

test_cases = [
    ("{}", True),
    ("{[()]}", True),
    ("{[()]", False),
    ("}", False),
    ("{", False),
    ("{)", False)
]

for given, expected in test_cases:
    assert is_valid(given) == expected, f"expected {expected} but got {is_valid(given)}"
