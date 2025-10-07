import math

def jump_search(arr, target):
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0
    while prev < n and arr[min(step, n)-1] < target:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1
    for i in range(prev, max(prev-int(math.sqrt(n)), -1), -1):
        if arr[i] == target:
            return i
    return -1

if __name__ == "__main__":
    try:
        arr = list(map(int, input("Enter numbers (space-separated): ").split()))
        arr.sort()
        target = int(input("Enter number to search: "))
        index = jump_search(arr, target)
        if index != -1:
            print(f"Element found at index {index} in sorted list {arr}")
        else:
            print("Element not found")
    except ValueError:
        print("Please enter valid sorted integers.")
