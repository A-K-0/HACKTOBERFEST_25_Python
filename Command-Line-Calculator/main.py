def run():
  print("----------------------")
  print("- 1. Sum             -")
  print("- 2. Subtraction     -")
  print("- 3. Multiplication  -")
  print("- 4. Division        -")
  print("----------------------")

  option = input(" Choose an option: ")

  print("----------------------")
  n1 = float(input("Choose a number: "))
  n2 = float(input("Choose another number: "))
  print("----------------------")

  if option == "1":
    result = n1+n2
    print(f"Result: {result}")
  
  elif option == "2":
    result = n1-n2
    print(f"Result: {result}")

  elif option == "3":
    result = n1*n2
    print(f"Result: {result}")
  
  elif option == "4":
    result = n1/n2
    print(f"Result: {result}")

if __name__ == "__main__":
  run()