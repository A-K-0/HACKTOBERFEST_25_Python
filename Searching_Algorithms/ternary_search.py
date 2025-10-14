def ternary_search(arr, target):
    """
    Perform Ternary Search on a sorted array.

    Parameters:
        arr (list[int]): Sorted list of integers.
        target (int): Value to search for.

    Returns:
        int: Index of target if found, else -1.
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        # Split into three parts
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3

        if arr[mid1] == target:
            return mid1
        if arr[mid2] == target:
            return mid2

        if target < arr[mid1]:
            right = mid1 - 1
        elif target > arr[mid2]:
            left = mid2 + 1
        else:
            left = mid1 + 1
            right = mid2 - 1
    return -1


# ✅ Example usage
if __name__ == "__main__":
    data = [2, 4, 6, 8, 10, 12, 14, 16]
    target = 12
    result = ternary_search(data, target)
    print(f"Element {target} found at index {result}" if result != -1 else "Not found")
