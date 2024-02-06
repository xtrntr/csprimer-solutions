"""
exp(a, n) -> a * a * a

2 * 2 = 4 or 2^2                 10
4 * 2 = 8 or 2^3                 11
4 * 4 = 16 or 2^4               100 
16 * 2 = 32 or 2^5             1001
16 * 16 = 256 or 2^8          10000
256 * 2 = 512 or 2^9          10001

make use of the binary representation of n to reduce the amount of work done
if n = 65536, we only need 16 iterations to calculate the result
"""

def exp(a, n):
    rtn = 1
    curr = a
    while n > 0:
        if n % 2 == 1:
            rtn *= curr
        curr *= curr
        n >>= 1
    return rtn


for a in range(1, 100):
    for n in range(1, 1000):
        assert exp(a, n) == a ** n, print(f"a: {a}, n: {n}. got {exp(a, n)}, expected {a ** n}")

print('ok')
