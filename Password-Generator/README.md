# Advanced Password and Passphrase Generator

A Python application to generate strong, customizable passwords and passphrases, with both a graphical user interface (GUI) and a command-line interface (CLI).

## Features

-   **Dual Mode:** Generate either random passwords or memorable passphrases.
-   **GUI and CLI modes:** Use the application through a user-friendly graphical interface or from the command line.
-   **Tabbed Interface:** Easily switch between password and passphrase generation in the GUI.
-   **Password Generation:**
    -   Customizable password length (4-50 characters).
    -   Selectable character sets: Uppercase, Lowercase, Numbers, and Symbols.
    -   Password strength indicator.
-   **Passphrase Generation:**
    -   Generate passphrases using a provided wordlist (e.g., the EFF wordlists).
    -   Customizable number of words.
    -   Customizable delimiter to separate the words.
-   **Copy to Clipboard:** Easily copy the generated password or passphrase to your clipboard.
-   **Resizable Window:** The application window is resizable to fit your screen.

## Setup

For the passphrase generation feature, you will need a wordlist file. This application is designed to work with the EFF's wordlists.

1.  **Download the wordlist:** You can download the `eff_large_wordlist.txt` file from the EFF's website:
    [https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt](https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt)

2.  **Place the file:** Save the file as `eff_large_wordlist.txt` inside the `Password-Generator` directory. The application will look for it there by default. Alternatively, you can specify the path to the wordlist using the `--wordlist` option in the CLI or the "Browse..." button in the GUI.

## Usage

### GUI Mode

To run the application in GUI mode, simply run the script without any arguments:

```bash
python3 Password-generator.py
```

or with the `--gui` flag:

```bash
python3 Password-generator.py --gui
```

The GUI has two tabs: "Password" and "Passphrase". Click on the desired tab to generate either a password or a passphrase.

### Command-Line Interface (CLI) Mode

The CLI uses subcommands to switch between generating passwords and passphrases.

#### Generating Passwords

**Syntax:**

```bash
python3 Password-generator.py password [options]
```

**Options:**

| Flag              | Description                  | Default |
| ----------------- | ---------------------------- | ------- |
| `-l`, `--length`  | Set the password length.     | 12      |
| `--no-uppercase`  | Exclude uppercase letters.   |         |
| `--no-lowercase`  | Exclude lowercase letters.   |         |
| `--no-numbers`    | Exclude numbers.             |         |
| `--no-symbols`    | Exclude symbols.             |         |

**Example:**

```bash
python3 Password-generator.py password -l 16 --no-symbols
```

#### Generating Passphrases

**Syntax:**

```bash
python3 Password-generator.py passphrase [options]
```

**Options:**

| Flag              | Description                       | Default                               |
| ----------------- | --------------------------------- | ------------------------------------- |
| `--wordlist`      | Path to the wordlist file.        | `Password-Generator/eff_large_wordlist.txt` |
| `-w`, `--words`   | Number of words in the passphrase.| 4                                     |
| `-d`, `--delimiter`| Delimiter between words.          | `-`                                   |

**Example:**

```bash
python3 Password-generator.py passphrase --words 5 --delimiter _
```

## Screenshot

![Screenshot of the Password and Passphrase Generator GUI](placeholder.png)
*A screenshot of the application's tabbed interface will be added here.*