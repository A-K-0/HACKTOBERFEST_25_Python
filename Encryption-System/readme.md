# 🧠💻 BlackBit - The Simple Encryption & Decryption System

> **BlackBit** is a lightweight, terminal-based file encryption & decryption system written in Python - with a hacker-style interactive interface.  
> Secure your files easily and locally using modern cryptography (Fernet AES), without cloud dependencies.  
> Built for simplicity, speed, and security. ⚡

---

## 🚀 Introduction

BlackBit is designed for developers, privacy lovers, and everyday users who want **a simple, offline, and effective** way to protect their files.

🔐 **Core Concept:**
- Select a file → Encrypt it → Auto-store encrypted file & key  
- Select an encrypted file + key → Decrypt it easily  
- No cloud. No uploads. 100% offline & secure.

✨ **Why It’s Cool**
- Hacker-style colorful terminal interface 😎  
- Auto folder management (`encryption/`, `key/`, `decryption/`)  
- Uses **Fernet (AES 128-bit)** symmetric encryption  
- Easy for beginners, powerful for pros    

---

## 🧩 Project Structure

When you run the tool, it automatically creates these folders in your working directory:

| Folder | Description |
|---------|--------------|
| 📁 `encryption/` | Stores encrypted files |
| 📁 `key/` | Stores generated encryption keys |
| 📁 `decryption/` | Stores decrypted outputs |

```
📦 BlackBit/
 ┣ 📜 main.py
 ┣ 📁 encryption/
 ┣ 📁 key/
 ┣ 📁 decryption/
 ┗ 📄 README.md
```

---

## ⚙️ How It Works

### 🔸 **1. Encryption Flow**
1. Run the program  
2. Choose option `1) Encrypt`  
3. File Manager opens → choose the file you want to encrypt  
4. BlackBit encrypts the file and saves it to the `encryption/` folder  
5. A secret key is automatically generated and saved in the `key/` folder  
6. You’ll see a success message with file locations 🎯  

---

### 🔹 **2. Decryption Flow**
1. Run the program  
2. Choose option `2) Decrypt`  
3. Select the encrypted file (`.encrypted` file)  
4. Then select the corresponding key file (`.key` file)  
5. BlackBit decrypts it and saves the file to the `decryption/` folder  
6. That’s it! Your file is back in its original form 🔓  

---

### 🧭 **3. More Menu**
Option `3) More` shows you the folder structure and their locations:

```
Location of folders (created in current working directory):
 - encryption/   (encrypted files)
 - key/          (keys for decryption)
 - decryption/   (decrypted outputs)
```

---

## 💻 Installation & Usage

### ✅ Prerequisites
- Python **3.8+**
- `cryptography` and `tqdm` libraries (install them once)

### 🔧 Install dependencies
```bash
pip install cryptography tqdm
```

### ▶️ Run the tool
```bash
python main.py
```

That’s it! You’ll be greeted with a menu like this 👇

```
=== Simple BlackBit ===

Main menu:
  1) Encrypt a file
  2) Decrypt a file
  3) More
  4) Exit
```

---

## 🧠 Example Workflow

```bash
> python main.py
/==================================================================\
||  ██████╗ ██╗      █████╗  ██████╗██╗  ██╗██████╗ ██╗████████╗  ||
||  ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██║╚══██╔══╝  ||
||  ██████╔╝██║     ███████║██║     █████╔╝ ██████╞╝██║   ██║     ||
||  ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██╔══██╗██║   ██║     ||
||  ███████╝███████╗██║  ██║╚██████╗██║  ██╗██████╞╝██║   ██║     ||
||  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚═╝   ╚═╝     ||
\==================================================================/
Main menu:
  1) Encrypt a file
  2) Decrypt a file
  3) More
  4) Exit

Choose [1-4]: 1
[ENCRYPT] Select the file to encrypt...
Encrypting... ✅
Encrypted file saved in: encryption/
Key file saved in: key/
```

---

## 🎨 Hacker-Style Terminal Experience

BlackBit adds a cyberpunk terminal aesthetic with colored text, progress bars, and dynamic messages —  
making your encryption experience **feel like a movie hacker console** 😎💚💾

> Example:
> ```
> [ENCRYPT] Processing file... ████████████████████ 100%
> [OK] Encryption complete. File saved to ./encryption/
> ```

---

## 🛠️ Tech Stack

| Component | Purpose |
|------------|----------|
| 🐍 Python 3 | Core language |
| 🔐 cryptography (Fernet) | AES-based encryption/decryption |
| 🧰 tqdm | Progress bar in terminal |
| 🖥️ tkinter | File selection dialogs |
| 🎨 colorama | Colorful terminal effects (if installed) |

---

## 💡 Why Use BlackBit?

- 🕵️‍♂️ 100% Offline  
- ⚡ Fast & lightweight  
- 🔐 Safe AES encryption  
- 🧠 Easy to use CLI  
- 🛠️ Perfect for learning or daily privacy  

---
