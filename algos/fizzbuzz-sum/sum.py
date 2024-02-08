"""
f(33) =
33 // 3 = 11
5 * (3 + 33) + 6 * 3
198
33 // 5 = 6
5, 10, 15, 20, 25, 30
3 * (5 + 30) = 105
33 // 15 = 2
15 + 30 
"""

def sums_of_x_in_n(n, x):
    counts = n // x
    if counts == 0:
        return 0
    if counts == 1:
        return x
    pair = x + n - n % x
    if counts % 2 == 0:
        return pair * counts / 2
    return pair * (counts // 2) + (counts // 2 + 1) * x


def fizzbuzz_sum_constant(n):
    return sums_of_x_in_n(n, 3) + sums_of_x_in_n(n, 5) - sums_of_x_in_n(n, 15)


def fizzbuzz_sum_linear(n):
    rtn = 0
    for i in range(1, n+1):
        if i % 5 == 0 or i % 3 == 0:
            rtn += i
    return rtn

for n in range(1, 1000):
    assert fizzbuzz_sum_linear(n) == fizzbuzz_sum_constant(n), f"for {n=}: expected {fizzbuzz_sum_linear(n)}, got {fizzbuzz_sum_constant(n)}"

print('ok')
