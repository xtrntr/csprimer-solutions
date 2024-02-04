def mergesort(arr):
    pass





for arr in [
        [5, 3, 2, 7, 1, 9, 8], # odd number
        [5, 3, 2, 4, 6, 9],    # even number
        [5, 3, 2, 2, 1, 9, 1], # duplicates
]:
    assert mergesort(arr) == sorted(arr), f"expected {sorted(arr)}, got {mergesort(arr)}"
