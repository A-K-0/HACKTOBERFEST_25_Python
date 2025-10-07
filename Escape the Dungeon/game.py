def start_game():
    print("🧙 Welcome to 'Escape the Dungeon'!")
    print("You wake up in a dark dungeon. There are two doors: one to your LEFT and one to your RIGHT.")

    choice1 = input("Which door do you choose? (left/right): ").lower()

    if choice1 == "left":
        left_room()
    elif choice1 == "right":
        right_room()
    else:
        print("😵 You stand still too long... a trapdoor opens beneath you. Game Over.")

def left_room():
    print("\nYou enter a room filled with treasure! 💰 But there's a sleeping dragon. 🐉")
    choice = input("Do you try to STEAL the treasure or SNEAK past the dragon? (steal/sneak): ").lower()

    if choice == "steal":
        print("🔥 The dragon wakes up and burns you to ashes. Game Over.")
    elif choice == "sneak":
        print("😮‍💨 You sneak past the dragon and find a ladder leading out. You escaped! 🎉")
    else:
        print("❓ You hesitate and the dragon wakes up. Game Over.")

def right_room():
    print("\nYou enter a dark hallway with two things: a SWORD and a SHIELD.")
    choice = input("Which do you take? (sword/shield): ").lower()

    if choice == "sword":
        print("⚔️ You bravely walk forward but run into a heavily-armored guard. Your sword is useless. Game Over.")
    elif choice == "shield":
        print("🛡️ You block the guard's attack and run past him. There's a trapdoor. You open it and escape! 🎉")
    else:
        print("⏳ You took too long to decide. The guard finds you. Game Over.")

if __name__ == "__main__":
    start_game()
