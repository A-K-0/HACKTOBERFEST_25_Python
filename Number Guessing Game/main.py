import random

def guessing_game():
    n = random.randint(1, 100)
    guesses = 0  # counts only valid guesses

    print("Welcome to the guessing game!")
    print("Please guess a number between 1 - 100")
    print("Enter 0 anytime to quit.")

    while True:
        user_input = input("Guess the number: ")
        
        
        if not user_input.isdigit():
            print("Invalid input! Please enter a number between 1 and 100.")
            continue

        a = int(user_input)

       
        if a == 0:
            print(f"You quit the game. The number was {n}.")
            break

        
        if a < 1 or a > 100:
            print("Number out of range! Guess between 1 and 100.")
            continue

        
        guesses += 1

        # Provide hints
        if a > n:
            print("Lower number please.")
        elif a < n:
            print("Higher number please.")
        else:
            print(f"Congratulations! You guessed the number {n} correctly in {guesses} attempt(s)!")
            break

guessing_game()
