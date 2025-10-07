import random
import os
import time

def clear_screen():
    """Clears the terminal screen for a better user experience."""
    os.system('cls' if os.name == 'nt' else 'clear')

def deal_card():
    """Returns a random card from the deck."""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]  # 11 is Ace, 10s are J/Q/K
    return random.choice(cards)

def calculate_score(cards):
    """
    Calculates the score of a given hand of cards.
    Handles the special case for Aces (can be 1 or 11).
    """
    # Check for Blackjack (an Ace and a 10-value card)
    if sum(cards) == 21 and len(cards) == 2:
        return 0  # Represents Blackjack

    # If the score is over 21 and there is an Ace, change the Ace's value from 11 to 1
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
        
    return sum(cards)

def compare_scores(player_score, dealer_score):
    """Compares the player and dealer scores to determine the winner."""
    if player_score == dealer_score:
        return "It's a draw! 🙃"
    elif dealer_score == 0:
        return "You lose, opponent has Blackjack! 😱"
    elif player_score == 0:
        return "You win with a Blackjack! 😎"
    elif player_score > 21:
        return "You went over. You lose! 😭"
    elif dealer_score > 21:
        return "Opponent went over. You win! 😁"
    elif player_score > dealer_score:
        return "You win! 😃"
    else:
        return "You lose! 😤"

def play_game():
    """The main function to play a round of Blackjack."""
    player_cards = []
    dealer_cards = []
    is_game_over = False

    # Deal initial two cards to player and dealer
    for _ in range(2):
        player_cards.append(deal_card())
        dealer_cards.append(deal_card())

    # --- Player's Turn ---
    while not is_game_over:
        player_score = calculate_score(player_cards)
        dealer_score = calculate_score(dealer_cards)
        
        print(f"    Your cards: {player_cards}, current score: {player_score}")
        print(f"    Dealer's first card: {dealer_cards[0]}")

        # Check for immediate end conditions
        if player_score == 0 or dealer_score == 0 or player_score > 21:
            is_game_over = True
        else:
            # Ask player to hit or stand
            user_should_deal = input("Type 'y' to get another card, type 'n' to pass: ").lower()
            if user_should_deal == 'y':
                player_cards.append(deal_card())
            else:
                is_game_over = True
        
        # Add a small pause for better flow
        time.sleep(1)
        clear_screen()

    # --- Dealer's Turn ---
    print("--- Final Hand ---")
    while calculate_score(dealer_cards) != 0 and calculate_score(dealer_cards) < 17:
        dealer_cards.append(deal_card())
        
    # --- Show Final Results ---
    final_player_score = calculate_score(player_cards)
    final_dealer_score = calculate_score(dealer_cards)
    
    print(f"    Your final hand: {player_cards}, final score: {final_player_score}")
    print(f"    Dealer's final hand: {dealer_cards}, final score: {final_dealer_score}")
    print(compare_scores(final_player_score, final_dealer_score))


# --- Game Start ---
while input("Do you want to play a game of Blackjack? Type 'y' or 'n': ").lower() == 'y':
    clear_screen()
    play_game()
    print("\n" + "-"*30 + "\n")

print("Thanks for playing!")
