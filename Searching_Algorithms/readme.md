# Searching Algorithms in Python

This repository contains implementations of **5 popular searching algorithms** in Python. Each algorithm allows the user to input a list of numbers and a target number to search for. Some algorithms require the list to be **sorted** for correct results.


---

## 1. Linear Search

**How it works:**  
- Linear search goes through each element of the list **one by one** until it finds the target.  
- Simple, no need for the list to be sorted.  

**Complexity:**  
- Time: O(n)  
- Space: O(1)  

**Use case:**  
- Small lists or unsorted data.  

---

## 2. Binary Search

**How it works:**  
- Binary search works on a **sorted list**.  
- It repeatedly divides the search interval in half.  
- Compares the target with the middle element: if smaller, searches the left half; if larger, searches the right half.  

**Complexity:**  
- Time: O(log n)  
- Space: O(1)  

**Use case:**  
- Large, sorted datasets where fast search is needed.  

---

## 3. Interpolation Search

**How it works:**  
- Interpolation search improves binary search for **uniformly distributed sorted lists**.  
- Estimates the position of the target based on the value of the target relative to the first and last elements.  

**Complexity:**  
- Time: O(log log n) on average (best case), O(n) worst case  
- Space: O(1)  

**Use case:**  
- Efficient for large, uniformly distributed, sorted datasets.  

---

## 4. Jump Search

**How it works:**  
- Jump search works on a **sorted list**.  
- It jumps ahead by fixed steps (usually √n) to find the block where the target may exist, then performs a linear search inside the block.  

**Complexity:**  
- Time: O(√n)  
- Space: O(1)  

**Use case:**  
- Sorted arrays where jumping reduces the number of comparisons.  

---

## 5. Fibonacci Search

**How it works:**  
- Fibonacci search also works on **sorted lists**.  
- Divides the array into sections using Fibonacci numbers instead of simple halving like binary search.  
- Reduces the size of the search interval based on Fibonacci sequence.  

**Complexity:**  
- Time: O(log n)  
- Space: O(1)  

**Use case:**  
- Useful in systems where the access cost of elements varies and memory access is expensive.  

---

## How to Run

1. Open terminal/command prompt.  
2. Navigate to the `Searching_Algorithms` folder.  
3. Run any of the files with Python 3:

```bash
python linear_search.py
python binary_search.py
python interpolation_search.py
python jump_search.py
python fibonacci_search.py


## How to Use the Programs

Follow the prompts to enter:

- **Numbers (space-separated)**  
- **Target number to search**

The program will display:

- The **index of the target** if found  
- Or indicate that the **target is not found** if it does not exist in the list
