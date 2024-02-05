def merge(arr1, arr2):
    print(f"merging arr1: {arr1}, arr2: {arr2}")
    p1 = p2 = 0
    rtn = []
    while p1 < len(arr1) and p2 < len(arr2):
        if arr1[p1] > arr2[p2]:
            rtn.append(arr2[p2])
            p2 += 1
        else:
            rtn.append(arr1[p1])
            p1 += 1
    if p1 < len(arr1):
        rtn += arr1[p1:]
    else:
        rtn += arr2[p2:]
    return rtn


def mergesort(arr):
    print(f"mergesort call on {arr}")
    length = len(arr)
    if length > 1:
        return merge(mergesort(arr[:length//2]), mergesort(arr[length//2:]))
    return arr


for arr in [
        [5, 3, 2, 7, 1, 9, 8], # odd number
        [5, 3, 2, 4, 6, 9],    # even number
        [5, 3, 2, 2, 1, 9, 1], # duplicates
]:
    assert mergesort(arr) == sorted(arr), f"expected {sorted(arr)}, got {mergesort(arr)}"
print("ok")
