"""
(2-1*(2+3))

iterate over char by char

if:
    the current char is an opening bracket or operator, add it to the stack
    the current char is a number, add it to the stack
    the current char is a number and the last item on a stack is also a number, concatenate both strings and add it to the stack.
    the current char is a closing bracket, pop the stack until an opening char is popped. evaluate all operands
"""

def calc(s):
    stack = []
    for c in s:
        if c in "(*/+-":
            stack.append(c)
        elif c.isdigit():
            if stack[-1].isdigit():
                stack.append(stack.pop() + c)
            else:
                stack.append(c)
        elif c == ")":
            expr = ""
            while stack[-1] != "(":
                expr = stack.pop() + expr
            stack.pop()
            stack.append(str(int(eval(expr))))
    assert len(stack) == 1
    return int(stack[0])

for expr, expected in [
        ("(2-1)", 1),
        ("(21-1)", 20),
        ("(21-1*3)", 18),
        ("(2-1*(2+3))", -3),
        ("((1-1)*(2+3))", 0),
        ("((5-1)/(1+1))", 2),
        ("((5-1)/2)", 2),
        ("(4/2/2)", 1),
        ("(3*(2*(1)))", 6),
]:
    assert calc(expr) == expected, f"got {calc(expr)}, expected {expected}"

print("ok")
