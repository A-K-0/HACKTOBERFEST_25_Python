import json
import hashlib
import getpass
import os

# Define the name of the file to store user data
USER_DATA_FILE = 'users.json'

def load_users():
    """Loads user data from the JSON file. If the file doesn't exist, returns an empty dictionary."""
    if not os.path.exists(USER_DATA_FILE):
        return {}
    try:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        # If the file is empty or corrupted, start fresh
        return {}

def save_users(users_data):
    """Saves the user data dictionary to the JSON file."""
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users_data, file, indent=4)

def hash_password(password):
    """Hashes a password using SHA-256 for secure storage."""
    # A salt could be added here for even better security
    return hashlib.sha256(password.encode()).hexdigest()

def signup():
    """Handles the user signup process."""
    print("\n--- Create a New Account ---")
    username = input("Enter a new username: ").lower()
    
    users = load_users()
    
    if username in users:
        print("Username already exists. Please try a different one.")
        return
        
    while True:
        password = getpass.getpass("Enter a new password: ")
        password_confirm = getpass.getpass("Confirm your password: ")
        
        if password == password_confirm:
            break
        else:
            print("Passwords do not match. Please try again.")

    # Hash the password before storing
    hashed_password = hash_password(password)
    
    # Add new user data, including an empty list for notes
    users[username] = {
        "password_hash": hashed_password,
        "notes": []
    }
    
    save_users(users)
    print(f"Account for '{username}' created successfully!")

def login():
    """Handles the user login process and returns the username on success."""
    print("\n--- Login to Your Account ---")
    username = input("Enter your username: ").lower()
    password = getpass.getpass("Enter your password: ")
    
    users = load_users()
    
    # Check if user exists and if the hashed password matches
    if username in users and users[username]['password_hash'] == hash_password(password):
        print(f"\nWelcome back, {username}!")
        return username  # Return username to start the session
    else:
        print("Invalid username or password.")
        return None

def user_session(username):
    """Manages the logged-in user's session (add/view notes)."""
    while True:
        print("\n--- Your Personal Notes ---")
        print("1. Add a new note")
        print("2. View my notes")
        print("3. Logout")
        
        choice = input("Choose an option (1-3): ")
        
        users = load_users() # Load the most recent data
        
        if choice == '1':
            note = input("Enter your note: ")
            users[username]['notes'].append(note)
            save_users(users)
            print("Note saved!")
        
        elif choice == '2':
            user_notes = users[username].get('notes', [])
            if not user_notes:
                print("\n You have no notes yet.")
            else:
                print("\n--- Your Saved Notes ---")
                for i, note in enumerate(user_notes, 1):
                    print(f"{i}. {note}")
        
        elif choice == '3':
            print("Logging you out. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please select a valid option.")

def main():
    """The main function to run the application."""
    while True:
        print("\n====== Welcome to the App ======")
        print("1. Signup")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == '1':
            signup()
        elif choice == '2':
            logged_in_user = login()
            if logged_in_user:
                user_session(logged_in_user) # Start the user session
        elif choice == '3':
            print("Thank you for using the app!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()