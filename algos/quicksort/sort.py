def quicksort(arr):
    if len(arr) <= 1:
        return arr
    m, i = 0, 1
    while i < len(arr):
        # m is the index before all values that are equal or larger than arr[0]
        if arr[i] < arr[0]:
            if m + 1 == i:
                m += 1
            else:
                arr[m+1], arr[i] = arr[i], arr[m+1]
                m += 1
        i += 1
    arr[m], arr[0] = arr[0], arr[m]
    return quicksort(arr[:m]) + [arr[m]] + quicksort(arr[m+1:])


for arr in [
        [5, 3, 2, 7, 1, 9, 8], # odd number
        [5, 3, 2, 4, 6, 9],    # even number
        [5, 3, 2, 2, 1, 9, 1], # duplicates
]:
    assert quicksort(arr) == sorted(arr), f"expected {sorted(arr)}, got {quicksort(arr)}"
print("ok")
