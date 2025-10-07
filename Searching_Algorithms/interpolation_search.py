def interpolation_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high and arr[low] <= target <= arr[high]:
        if arr[high] == arr[low]:
            if arr[low] == target:
                return low
            return -1
        pos = low + ((target - arr[low]) * (high - low) // (arr[high] - arr[low]))
        if arr[pos] == target:
            return pos
        if arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1

if __name__ == "__main__":
    try:
        arr = list(map(int, input("Enter numbers (space-separated): ").split()))
        arr.sort()
        target = int(input("Enter number to search: "))
        index = interpolation_search(arr, target)
        if index != -1:
            print(f"Element found at index {index} in sorted list {arr}")
        else:
            print("Element not found")
    except ValueError:
        print("Please enter valid sorted integers.")
