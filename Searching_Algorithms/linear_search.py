def linear_search(arr, target):
    for i, num in enumerate(arr):
        if num == target:
            return i
    return -1

if __name__ == "__main__":
    try:
        arr = list(map(int, input("Enter numbers (space-separated): ").split()))
        target = int(input("Enter number to search: "))
        index = linear_search(arr, target)
        if index != -1:
            print(f"Element found at index {index}")
        else:
            print("Element not found")
    except ValueError:
        print("Please enter valid integers.")
