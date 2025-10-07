def fibonacci_search(arr, target):
    n = len(arr)
    fibMMm2 = 0
    fibMMm1 = 1
    fibM = fibMMm2 + fibMMm1

    while fibM < n:
        fibMMm2, fibMMm1 = fibMMm1, fibM
        fibM = fibMMm1 + fibMMm2

    offset = -1
    while fibM > 1:
        i = min(offset + fibMMm2, n-1)
        if arr[i] < target:
            fibM, fibMMm1, fibMMm2 = fibMMm1, fibMMm2, fibM - fibMMm1
            offset = i
        elif arr[i] > target:
            fibM, fibMMm1, fibMMm2 = fibMMm2, fibMMm1 - fibMMm2, fibMMm2 - (fibMMm1 - fibMMm2)
        else:
            return i
    if fibMMm1 and offset + 1 < n and arr[offset+1] == target:
        return offset+1
    return -1

if __name__ == "__main__":
    try:
        arr = list(map(int, input("Enter numbers (space-separated): ").split()))
        arr.sort()
        target = int(input("Enter number to search: "))
        index = fibonacci_search(arr, target)
        if index != -1:
            print(f"Element found at index {index} in sorted list {arr}")
        else:
            print("Element not found")
    except ValueError:
        print("Please enter valid sorted integers.")
