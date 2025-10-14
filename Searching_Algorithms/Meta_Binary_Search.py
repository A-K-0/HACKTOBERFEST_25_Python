"""
Meta Binary Search Algorithm
----------------------------
This algorithm is a variant of Binary Search that uses bit manipulation
to find the target element in a sorted array iteratively — without recursion.

It computes the result by checking bits from the most significant bit to least.

Time Complexity: O(log N)
Space Complexity: O(1)
"""

def meta_binary_search(arr, target):
    """
    Perform Meta Binary Search using bit manipulation.

    Parameters:
        arr (list): Sorted list of elements
        target (int/float): Value to be searched

    Returns:
        int: Index of target if found, otherwise -1
    """
    n = len(arr)
    if n == 0:
        return -1

    # Compute highest power of 2 less than array length
    bit = 1 << (n.bit_length() - 1)
    idx = 0

    while bit > 0:
        next_idx = idx | bit
        if next_idx < n and arr[next_idx] <= target:
            idx = next_idx
        bit >>= 1

    if arr[idx] == target:
        return idx
    return -1


if __name__ == "__main__":
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target = 23
    result = meta_binary_search(arr, target)
    print(f"Array: {arr}")
    print(f"Target: {target}")
    print(f"Result Index: {result if result != -1 else 'Not Found'}")
