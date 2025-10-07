def binary_search(arr, target):
    left, right = 0, len(arr)-1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

if __name__ == "__main__":
    try:
        arr = list(map(int, input("Enter numbers (space-separated): ").split()))
        arr.sort()
        target = int(input("Enter number to search: "))
        index = binary_search(arr, target)
        if index != -1:
            print(f"Element found at index {index} in sorted list {arr}")
        else:
            print("Element not found")
    except ValueError:
        print("Please enter valid sorted integers.")
