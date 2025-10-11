def length_converter():
    while True:
        choice = input("Convert: 1) Meters to Kilometers 2) Kilometers to Meters: ")
        if choice == "1":
            try:
                meters = float(input("Enter meters: "))
                print(f"{meters} m = {meters / 1000} km")
                break
            except ValueError:
                print("Invalid input! Enter a number.")
        elif choice == "2":
            try:
                km = float(input("Enter kilometers: "))
                print(f"{km} km = {km * 1000} m")
                break
            except ValueError:
                print("Invalid input! Enter a number.")
        else:
            print("Please choose 1 or 2.")

def weight_converter():
    while True:
        choice = input("Convert: 1) Kilograms to Pounds 2) Pounds to Kilograms: ")
        if choice == "1":
            try:
                kg = float(input("Enter kilograms: "))
                print(f"{kg} kg = {kg * 2.20462} lb")
                break
            except ValueError:
                print("Invalid input! Enter a number.")
        elif choice == "2":
            try:
                lb = float(input("Enter pounds: "))
                print(f"{lb} lb = {lb / 2.20462} kg")
                break
            except ValueError:
                print("Invalid input! Enter a number.")
        else:
            print("Please choose 1 or 2.")

def temp_converter():
    while True:
        choice = input("Convert: 1) Celsius to Fahrenheit 2) Fahrenheit to Celsius: ")
        if choice == "1":
            try:
                c = float(input("Enter Celsius: "))
                print(f"{c}°C = {c * 9/5 + 32}°F")
                break
            except ValueError:
                print("Invalid input! Enter a number.")
        elif choice == "2":
            try:
                f = float(input("Enter Fahrenheit: "))
                print(f"{f}°F = {(f - 32) * 5/9}°C")
                break
            except ValueError:
                print("Invalid input! Enter a number.")
        else:
            print("Please choose 1 or 2.")

if __name__ == "__main__":
    while True:
        print("\nUnit Converter:")
        print("1) Length")
        print("2) Weight")
        print("3) Temperature")
        print("4) Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            length_converter()
        elif choice == "2":
            weight_converter()
        elif choice == "3":
            temp_converter()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please select 1, 2, 3, or 4.")
