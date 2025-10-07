import random
import os

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome_message():
    """Prints the welcome message for the game."""
    print("=======================================")
    print("          Welcome to Hangman!          ")
    print("=======================================")
    print("Try to guess the secret word, letter by letter.")
    print("You have 6 incorrect guesses before you lose.")
    print("\nLet's begin!")
    input("Press Enter to start...")

def get_random_word():
    """Selects a random word from a predefined list."""
    word_list = [
        "PYTHON", "JAVASCRIPT", "DEVELOPER", "COMPUTER", "ALGORITHM",
        "KEYBOARD", "SOFTWARE", "INTERFACE", "DATABASE", "NETWORK",
        "SECURITY", "FRAMEWORK", "VARIABLE", "FUNCTION", "PROJECT"
    ]
    return random.choice(word_list)

def print_game_state(attempts_left, display_word, guessed_letters):
    """Prints the current state of the game (hangman art, word, guesses)."""
    stages = [
        # Final state: Head, torso, both arms, and both legs
        '''
           +---+
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        =========
        ''',
        # Head, torso, both arms, and one leg
        '''
           +---+
           |   |
           O   |
          /|\\  |
          /    |
               |
        =========
        ''',
        # Head, torso, and both arms
        '''
           +---+
           |   |
           O   |
          /|\\  |
               |
               |
        =========
        ''',
        # Head, torso, and one arm
        '''
           +---+
           |   |
           O   |
          /|   |
               |
               |
        =========
        ''',
        # Head and torso
        '''
           +---+
           |   |
           O   |
           |   |
               |
               |
        =========
        ''',
        # Head
        '''
           +---+
           |   |
           O   |
               |
               |
               |
        =========
        ''',
        # Initial empty state
        '''
           +---+
           |   |
               |
               |
               |
               |
        =========
        '''
    ]
    
    print(stages[attempts_left])
    print("\nSecret Word: ", " ".join(display_word))
    print("\nGuessed Letters: ", ", ".join(sorted(list(guessed_letters))))
    print("-" * 30)

def play_game():
    """Main function to run the Hangman game."""
    word_to_guess = get_random_word()
    guessed_letters = set()
    attempts = 6
    display_word = ["_"] * len(word_to_guess)
    game_over = False

    clear_screen()
    print_welcome_message()

    while not game_over:
        clear_screen()
        print_game_state(attempts, display_word, guessed_letters)

        # Get user input
        guess = input("Guess a letter: ").upper()

        # Input validation
        if len(guess) != 1 or not guess.isalpha():
            print("\nInvalid input. Please enter a single letter.")
            input("Press Enter to try again...")
            continue
        
        if guess in guessed_letters:
            print(f"\nYou've already guessed the letter '{guess}'.")
            input("Press Enter to try again...")
            continue

        # Add the valid guess to our set of guessed letters
        guessed_letters.add(guess)

        # Check if the guess is in the word
        if guess in word_to_guess:
            print(f"\nGood guess! '{guess}' is in the word.")
            # Update the display word
            for index, letter in enumerate(word_to_guess):
                if letter == guess:
                    display_word[index] = guess
        else:
            print(f"\nSorry, '{guess}' is not in the word.")
            attempts -= 1

        input("Press Enter to continue...")

        # Check for win/loss condition
        if "_" not in display_word:
            game_over = True
            clear_screen()
            print_game_state(attempts, display_word, guessed_letters)
            print("🎉 CONGRATULATIONS! You won! 🎉")
            print(f"The word was: {word_to_guess}")
        elif attempts == 0:
            game_over = True
            clear_screen()
            print_game_state(attempts, display_word, guessed_letters)
            print("☠️ GAME OVER! You lost. ☠️")
            print(f"The correct word was: {word_to_guess}")

if __name__ == "__main__":
    play_game()