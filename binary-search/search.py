"""
Binary search. Return -1 when given n cannot be found, return the index if n can be found.
The idea here is to divide the search space into 2 on every iteration. We can do this by
checking the middle point of the array on every iteration.

Let x be the size of the array

The middle point of an odd number would be x // 2 (x = 3, middle = 1)
The middle point of an even number would also be x // 2 (x = 4, middle = 2)

if n > middle, then we can take the right half of the array without middle.
if n < middle, then we can take the left half of the array without middle.
if n == middle, that's our return value (the index)

We use low and high in our implementation so as to keep track of the index.
"""

def binary(n, arr):
    low, high = 0, len(arr) - 1
    while (low <= high):
        mid = ((high - low) // 2) + low
        if arr[mid] == n:
            return mid
        if arr[mid] > n:
            low = mid + 1
        if arr[mid] < n:
            high = mid - 1
    return -1

tests = [
    (4, [-5, -3, 0, 4, 20], 3), # can find right side
    (0, [-5, -3, 0, 4, 20], 2) # can find immediately
    (-3, [-5, -3, 0, 4, 20], 1), # can find left side
    (3, [-5, -3, 0, 4, 20], -1), # can't find something in the middle
    (21, [-5, -3, 0, 4, 20], -1), # can't find something larger than max
    (-6, [-5, -3, 0, 4, 20], -1), # can't find something smaller than min
    (-5, [-5, -3, 0, 4, 20], -1) # can find left side
]

for (n, arr, expected) in tests:
    assert binary(n, arr) == expected
