"""
Use BFS to generate all possible permutations of a person taking 1, 2, 3 steps
If we arrive at a node where the total sum of steps accumulated == n, add that to the return value.
Ignore nodes where the total sum of steps accumulated > n.
Continue building this BFS graph until there are no more possible candidates.
"""

def permutations(n):
    queue = [0]
    rtn = 0

    while queue:
        new_level = []
        for possibility in queue:
            for step in [1, 2, 3]:
                if possibility + step < n:
                    new_level.append(possibility + step)
                elif possibility + step == n:
                    rtn += 1
        queue = new_level

    return rtn

assert permutations(1) == 1
assert permutations(2) == 2
assert permutations(3) == 4
assert permutations(4) == 7
