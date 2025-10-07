import random
import string
import argparse
import sys
import os

def generate_password_logic(length, use_uppercase, use_lowercase, use_numbers, use_symbols):
    char_sets = []
    password_chars = []

    if use_uppercase:
        char_sets.append(string.ascii_uppercase)
        password_chars.append(random.choice(string.ascii_uppercase))
    if use_lowercase:
        char_sets.append(string.ascii_lowercase)
        password_chars.append(random.choice(string.ascii_lowercase))
    if use_numbers:
        char_sets.append(string.digits)
        password_chars.append(random.choice(string.digits))
    if use_symbols:
        char_sets.append(string.punctuation)
        password_chars.append(random.choice(string.punctuation))

    if not char_sets:
        return None

    all_chars = "".join(char_sets)
    
    if len(password_chars) > length:
        password_chars = random.sample(password_chars, length)
    else:
        password_chars += random.choices(all_chars, k=length - len(password_chars))

    random.shuffle(password_chars)
    return "".join(password_chars)

def generate_passphrase_logic(wordlist_path, num_words, delimiter):
    try:
        with open(wordlist_path, 'r') as f:
            words = [line.split('\t')[1].strip() for line in f]
        
        passphrase_words = random.choices(words, k=num_words)
        return delimiter.join(passphrase_words)
    except FileNotFoundError:
        return "Error: Wordlist file not found."
    except Exception as e:
        return f"Error: {e}"

def main():
    parser = argparse.ArgumentParser(description="A Python application to generate strong, customizable passwords and passphrases.")
    parser.add_argument('--gui', action='store_true', help="Launch the GUI application.")
    
    subparsers = parser.add_subparsers(dest='command')

    # Password subcommand
    parser_password = subparsers.add_parser('password', help='Generate a password.')
    parser_password.add_argument('-l', '--length', type=int, default=12, help="Length of the password.")
    parser_password.add_argument('--no-uppercase', dest='uppercase', action='store_false', help="Exclude uppercase letters.")
    parser_password.add_argument('--no-lowercase', dest='lowercase', action='store_false', help="Exclude lowercase letters.")
    parser_password.add_argument('--no-numbers', dest='numbers', action='store_false', help="Exclude numbers.")
    parser_password.add_argument('--no-symbols', dest='symbols', action='store_false', help="Exclude symbols.")
    parser_password.set_defaults(uppercase=True, lowercase=True, numbers=True, symbols=True)

    # Passphrase subcommand
    parser_passphrase = subparsers.add_parser('passphrase', help='Generate a passphrase.')
    parser_passphrase.add_argument('--wordlist', type=str, default='Password-Generator/eff_large_wordlist.txt', help="Path to the wordlist file.")
    parser_passphrase.add_argument('-w', '--words', type=int, default=4, help="Number of words in the passphrase.")
    parser_passphrase.add_argument('-d', '--delimiter', type=str, default='-', help="Delimiter between words.")

    args = parser.parse_args()

    if args.gui or len(sys.argv) == 1:
        import tkinter as tk
        from tkinter import messagebox, ttk, filedialog

        class PasswordGeneratorApp:
            def __init__(self, root):
                self.root = root
                self.root.title("Password & Passphrase Generator")
                self.root.geometry("450x550")
                self.root.resizable(True, True)

                style = ttk.Style(root)
                style.theme_use('clam')

                self.notebook = ttk.Notebook(root)
                self.notebook.pack(pady=10, expand=True, fill="both")

                self.password_frame = ttk.Frame(self.notebook, padding="10")
                self.passphrase_frame = ttk.Frame(self.notebook, padding="10")

                self.notebook.add(self.password_frame, text='Password')
                self.notebook.add(self.passphrase_frame, text='Passphrase')

                self.create_password_widgets()
                self.create_passphrase_widgets()

            def create_password_widgets(self):
                main_frame = self.password_frame

                self.length_var = tk.IntVar(value=12)
                self.uppercase_var = tk.BooleanVar(value=True)
                self.lowercase_var = tk.BooleanVar(value=True)
                self.numbers_var = tk.BooleanVar(value=True)
                self.symbols_var = tk.BooleanVar(value=True)

                # Length
                length_frame = ttk.LabelFrame(main_frame, text="Password Length")
                length_frame.pack(fill=tk.X, pady=10)
                
                length_spinbox = ttk.Spinbox(length_frame, from_=4, to=50, textvariable=self.length_var, width=5)
                length_spinbox.pack(pady=5, padx=10)
                self.length_var.set(12)

                # Complexity Options
                options_frame = ttk.LabelFrame(main_frame, text="Complexity Options")
                options_frame.pack(fill=tk.X, pady=10)
                ttk.Checkbutton(options_frame, text="Include Uppercase Letters (A-Z)", variable=self.uppercase_var).pack(anchor=tk.W, padx=10)
                ttk.Checkbutton(options_frame, text="Include Lowercase Letters (a-z)", variable=self.lowercase_var).pack(anchor=tk.W, padx=10)
                ttk.Checkbutton(options_frame, text="Include Numbers (0-9)", variable=self.numbers_var).pack(anchor=tk.W, padx=10)
                ttk.Checkbutton(options_frame, text="Include Symbols (!@#$%%)", variable=self.symbols_var).pack(anchor=tk.W, padx=10)

                # Generate Button
                ttk.Button(main_frame, text="Generate Password", command=self.display_password).pack(pady=10)

                # Password Display
                self.password_entry = ttk.Entry(main_frame, width=40, state='readonly', font=('Courier', 10))
                self.password_entry.pack(pady=10, padx=10, fill=tk.X)

                # Strength Indicator
                self.strength_label = ttk.Label(main_frame, text="Password Strength:")
                self.strength_label.pack()
                self.strength_bar = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
                self.strength_bar.pack(pady=5)

                # Copy Button
                ttk.Button(main_frame, text="Copy to Clipboard", command=self.copy_password_to_clipboard).pack(pady=10)

            def create_passphrase_widgets(self):
                main_frame = self.passphrase_frame

                # Wordlist
                wordlist_frame = ttk.LabelFrame(main_frame, text="Wordlist")
                wordlist_frame.pack(fill=tk.X, pady=10)
                self.wordlist_var = tk.StringVar(value="Password-Generator/eff_large_wordlist.txt")
                ttk.Entry(wordlist_frame, textvariable=self.wordlist_var, width=40).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
                ttk.Button(wordlist_frame, text="Browse...", command=self.browse_wordlist).pack(side=tk.RIGHT, padx=5)

                # Number of words
                words_frame = ttk.LabelFrame(main_frame, text="Number of Words")
                words_frame.pack(fill=tk.X, pady=10)
                self.num_words_var = tk.IntVar(value=4)
                words_spinbox = ttk.Spinbox(words_frame, from_=2, to=10, textvariable=self.num_words_var, width=5)
                words_spinbox.pack(pady=5, padx=10)
                self.num_words_var.set(4)

                # Delimiter
                delimiter_frame = ttk.LabelFrame(main_frame, text="Delimiter")
                delimiter_frame.pack(fill=tk.X, pady=10)
                self.delimiter_var = tk.StringVar(value="-")
                ttk.Entry(delimiter_frame, textvariable=self.delimiter_var, width=5).pack(padx=10)

                # Generate Button
                ttk.Button(main_frame, text="Generate Passphrase", command=self.display_passphrase).pack(pady=10)

                # Passphrase Display
                self.passphrase_entry = ttk.Entry(main_frame, width=40, state='readonly', font=('Courier', 10))
                self.passphrase_entry.pack(pady=10, padx=10, fill=tk.X)

                # Copy Button
                ttk.Button(main_frame, text="Copy to Clipboard", command=self.copy_passphrase_to_clipboard).pack(pady=10)

            def browse_wordlist(self):
                filename = filedialog.askopenfilename(title="Select a wordlist file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
                if filename:
                    self.wordlist_var.set(filename)

            def display_password(self):
                if not (self.uppercase_var.get() or self.lowercase_var.get() or self.numbers_var.get() or self.symbols_var.get()):
                    messagebox.showerror("Error", "You must select at least one character set.")
                    return

                password = generate_password_logic(
                    self.length_var.get(),
                    self.uppercase_var.get(),
                    self.lowercase_var.get(),
                    self.numbers_var.get(),
                    self.symbols_var.get()
                )
                if password:
                    self.password_entry.config(state='normal')
                    self.password_entry.delete(0, tk.END)
                    self.password_entry.insert(0, password)
                    self.password_entry.config(state='readonly')
                    
                    strength = self.calculate_strength(self.length_var.get())
                    self.strength_bar['value'] = strength

            def display_passphrase(self):
                passphrase = generate_passphrase_logic(self.wordlist_var.get(), self.num_words_var.get(), self.delimiter_var.get())
                self.passphrase_entry.config(state='normal')
                self.passphrase_entry.delete(0, tk.END)
                self.passphrase_entry.insert(0, passphrase)
                self.passphrase_entry.config(state='readonly')

            def calculate_strength(self, length):
                strength_score = 0
                if self.uppercase_var.get(): strength_score += 1
                if self.lowercase_var.get(): strength_score += 1
                if self.numbers_var.get(): strength_score += 1
                if self.symbols_var.get(): strength_score += 1

                variety_strength = (strength_score / 4) * 50

                length_strength = 0
                if length >= 16:
                    length_strength = 50
                elif length >= 12:
                    length_strength = 35
                elif length >= 8:
                    length_strength = 20

                total_strength = variety_strength + length_strength
                return min(total_strength, 100)

            def copy_password_to_clipboard(self):
                password = self.password_entry.get()
                if password:
                    self.root.clipboard_clear()
                    self.root.clipboard_append(password)
                    messagebox.showinfo("Copied", "Password copied to clipboard!")
                else:
                    messagebox.showwarning("Warning", "No password to copy!")

            def copy_passphrase_to_clipboard(self):
                passphrase = self.passphrase_entry.get()
                if passphrase:
                    self.root.clipboard_clear()
                    self.root.clipboard_append(passphrase)
                    messagebox.showinfo("Copied", "Passphrase copied to clipboard!")
                else:
                    messagebox.showwarning("Warning", "No passphrase to copy!")

        root = tk.Tk()
        app = PasswordGeneratorApp(root)
        root.mainloop()

    elif args.command == 'password':
        if not (args.uppercase or args.lowercase or args.numbers or args.symbols):
            print("Error: You must select at least one character set.")
            return
            
        password = generate_password_logic(args.length, args.uppercase, args.lowercase, args.numbers, args.symbols)
        if password:
            print(password)
        else:
            print("Error: Could not generate password.")
    
    elif args.command == 'passphrase':
        passphrase = generate_passphrase_logic(args.wordlist, args.words, args.delimiter)
        print(passphrase)

if __name__ == "__main__":
    main()