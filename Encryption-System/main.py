#!/usr/bin/env python3
"""
Simple Blackbit — main.py (Hacker-style UI)

This keeps the same simple behavior as before but adds:
 - ANSI color output for logs
 - typewriter-style boot banner
 - spinner + stylized messages during waits
 - hacker-like header and small UX polish

Behavior:
 - 1) Encrypt: pick file -> encrypted saved to ./encryption/, key saved to ./key/
 - 2) Decrypt: pick encrypted file -> pick key -> decrypted saved to ./decryption/
 - 3) More: show folder locations/details
 - 4) Exit
"""
import os
import sys
import time
import shutil
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple
import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet
from tqdm import tqdm

# --- Config / constants ---
BASE_DIR = Path.cwd()
ENCRYPTION_DIR = BASE_DIR / "encryption"
KEY_DIR = BASE_DIR / "key"
DECRYPTION_DIR = BASE_DIR / "decryption"
TEMP_DIR = BASE_DIR / ".blackbit_temp"

CHUNK_SIZE = 64 * 1024
FILE_MAGIC = b"BBIT1"

MIN_DISPLAY_SEC = 3.0  # visible message time minimum

# --- Terminal colors & small UI helpers ---
CSI = "\033["
RESET = CSI + "0m"
BOLD = CSI + "1m"
DIM = CSI + "2m"

FG_GREEN = CSI + "92m"
FG_RED = CSI + "91m"
FG_BLUE = CSI + "94m"
FG_CYAN = CSI + "96m"
FG_YELLOW = CSI + "93m"
FG_MAGENTA = CSI + "95m"

def slow_print(text: str, delay: float = 0.002, newline: bool = True):
    """Typewriter effect but fast enough not to annoy."""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    if newline:
        sys.stdout.write("\n")
        sys.stdout.flush()

def banner():
    art = r"""
    /==================================================================\
    ||  ██████╗ ██╗      █████╗  ██████╗██╗  ██╗██████╗ ██╗████████╗  ||
    ||  ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██║╚══██╔══╝  ||
    ||  ██████╔╝██║     ███████║██║     █████╔╝ ██████╞╝██║   ██║     ||
    ||  ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██╔══██╗██║   ██║     ||
    ||  ███████╝███████╗██║  ██║╚██████╗██║  ██╗██████╞╝██║   ██║     ||
    ||  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚═╝   ╚═╝     ||
    \==================================================================/
    """
    slow_print(FG_CYAN + art + RESET, delay=0.0008)
    slow_print(FG_GREEN + "[SECURE] Terminal session established..." + RESET, delay=0.01)

def hacker_log(msg: str):
    slow_print(FG_GREEN + "[OK]    " + RESET + msg)

def info_log(msg: str):
    slow_print(FG_BLUE + "[INFO]  " + RESET + msg)

def error_log(msg: str):
    slow_print(FG_RED + "[ERROR] " + RESET + msg)

def hint(msg: str):
    slow_print(FG_YELLOW + "[HINT]  " + RESET + msg)

# small spinner used while waiting a minimum visible time
def spinner_while(min_seconds: float, stop_event: threading.Event):
    chars = "|/-\\"
    t0 = time.time()
    i = 0
    while not stop_event.is_set():
        elapsed = time.time() - t0
        if elapsed >= min_seconds:
            break
        sys.stdout.write(FG_MAGENTA + "\r[~] " + RESET + f"finalizing {chars[i % len(chars)]} " + f"({elapsed:.1f}s)" )
        sys.stdout.flush()
        i += 1
        time.sleep(0.12)
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()

# --- Helpers (file dialogs etc.) ---
def ensure_dirs():
    for d in (ENCRYPTION_DIR, KEY_DIR, DECRYPTION_DIR, TEMP_DIR):
        d.mkdir(parents=True, exist_ok=True)

def _prepare_root():
    root = tk.Tk()
    root.withdraw()
    try:
        root.update()
        root.deiconify()
        root.lift()
        root.attributes("-topmost", True)
        root.focus_force()
    except Exception:
        pass
    return root

def choose_file_dialog(title: str = "Select file") -> Optional[Path]:
    root = _prepare_root()
    time.sleep(0.06)
    try:
        path = filedialog.askopenfilename(title=title, parent=root)
    except Exception:
        path = None
    try:
        root.destroy()
    except Exception:
        pass
    return Path(path) if path else None

def human_size(n: int) -> str:
    for unit in ("B","KB","MB","GB","TB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"

# --- Core encrypt/decrypt (streaming) ---
def encrypt_stream(inp: Path, outp: Path, key: bytes) -> float:
    ensure_dirs()
    f = Fernet(key)
    name_bytes = inp.name.encode("utf-8")
    header = len(name_bytes).to_bytes(4, "big") + name_bytes
    total = inp.stat().st_size
    t0 = time.time()
    with inp.open("rb") as inf, outp.open("wb") as outf, tqdm(total=total, unit="B", unit_scale=True, desc="Encrypting", ncols=100) as pbar:
        outf.write(FILE_MAGIC)
        outf.write(header)
        while True:
            chunk = inf.read(CHUNK_SIZE)
            if not chunk:
                break
            enc = f.encrypt(chunk)
            outf.write(len(enc).to_bytes(4, "big"))
            outf.write(enc)
            pbar.update(len(chunk))
    return time.time() - t0

def decrypt_stream(inp: Path, outdir: Path, key: bytes) -> Tuple[Path, float]:
    ensure_dirs()
    t0 = time.time()
    with inp.open("rb") as inf:
        magic = inf.read(len(FILE_MAGIC))
        if magic != FILE_MAGIC:
            raise ValueError("Invalid encrypted file format.")
        name_len_b = inf.read(4)
        if len(name_len_b) < 4:
            raise ValueError("Corrupt header.")
        name_len = int.from_bytes(name_len_b, "big")
        orig_name = inf.read(name_len).decode("utf-8", errors="replace")
        outp = outdir / orig_name
        total = inp.stat().st_size
        f = Fernet(key)
        with outp.open("wb") as outf, tqdm(total=total, unit="B", unit_scale=True, desc="Decrypting", ncols=100) as pbar:
            pbar.update(len(FILE_MAGIC) + 4 + name_len)
            while True:
                hdr = inf.read(4)
                if not hdr or len(hdr) < 4:
                    break
                size = int.from_bytes(hdr, "big")
                block = inf.read(size)
                if len(block) < size:
                    raise ValueError("Truncated encrypted block.")
                dec = f.decrypt(block)
                outf.write(dec)
                pbar.update(4 + size)
    return outp, time.time() - t0

# --- Flows (with styled output) ---
def encryption_flow():
    ensure_dirs()
    info_log("Opening file manager to choose file to encrypt...")
    inp = choose_file_dialog("Select file to encrypt")
    if not inp:
        hint("No file selected. Returning to menu.")
        return
    if not inp.exists() or not inp.is_file():
        error_log("Invalid selection. Returning.")
        return

    slow_print(FG_CYAN + f"[SELECTED] {inp} ({human_size(inp.stat().st_size)})" + RESET)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    enc_name = f"{inp.stem}_{timestamp}.encrypted"
    outp = ENCRYPTION_DIR / enc_name

    key = Fernet.generate_key()
    info_log("Encrypting — this may take a while for large files.")
    try:
        elapsed = encrypt_stream(inp, outp, key)
    except Exception as e:
        error_log(f"Encryption failed: {e}")
        if outp.exists():
            try: outp.unlink()
            except Exception: pass
        return

    # min display spinner
    if elapsed < MIN_DISPLAY_SEC:
        remaining = MIN_DISPLAY_SEC - elapsed
        stop_event = threading.Event()
        spinner_thread = threading.Thread(target=spinner_while, args=(remaining, stop_event))
        spinner_thread.start()
        time.sleep(remaining)
        stop_event.set()
        spinner_thread.join()

    # Save key automatically to key directory with matching name
    key_name = f"{inp.stem}_{timestamp}.key"
    key_path = KEY_DIR / key_name
    try:
        with key_path.open("wb") as kf:
            kf.write(key)
    except Exception as e:
        error_log(f"Could not save key automatically: {e}")
        print("Encrypted file is in:", outp)
        print("You must keep the key to decrypt.")
        return

    hacker_log("Encryption complete.")
    slow_print(FG_GREEN + f"  Encrypted file: {outp}" + RESET)
    slow_print(FG_GREEN + f"  Key file:       {key_path}" + RESET)
    slow_print(FG_YELLOW + "Files stored under folders: encryption/   key/   decryption/" + RESET)
    slow_print(FG_MAGENTA + "Return to the main menu to decrypt when ready.\n" + RESET)

def decryption_flow():
    ensure_dirs()
    info_log("Opening file manager to choose encrypted file...")
    enc = choose_file_dialog("Select encrypted file to decrypt")
    if not enc:
        hint("No file selected. Returning to menu.")
        return
    enc = Path(enc)
    if not enc.exists() or not enc.is_file():
        error_log("Invalid selection. Returning.")
        return

    info_log("Select the key file that corresponds to this encrypted file...")
    kf = choose_file_dialog("Select key file (.key)")
    if not kf:
        hint("No key selected. Returning to menu.")
        return
    try:
        with open(kf, "rb") as f:
            key = f.read()
    except Exception as e:
        error_log(f"Failed reading key file: {e}")
        return

    info_log("Decrypting — this may take a while for large files.")
    try:
        outp, elapsed = decrypt_stream(enc, DECRYPTION_DIR, key)
    except Exception as e:
        error_log(f"Decryption failed: {e}")
        try:
            if 'outp' in locals() and outp.exists():
                outp.unlink()
        except Exception:
            pass
        return

    if elapsed < MIN_DISPLAY_SEC:
        remaining = MIN_DISPLAY_SEC - elapsed
        stop_event = threading.Event()
        spinner_thread = threading.Thread(target=spinner_while, args=(remaining, stop_event))
        spinner_thread.start()
        time.sleep(remaining)
        stop_event.set()
        spinner_thread.join()

    hacker_log("Decryption complete.")
    slow_print(FG_GREEN + f"  Decrypted file: {outp}" + RESET)
    slow_print(FG_YELLOW + f"  Saved in:       {DECRYPTION_DIR.resolve()}\n" + RESET)

def more_info():
    ensure_dirs()
    slow_print(FG_CYAN + "\nLocation of folders (created in current working directory):" + RESET)
    slow_print(FG_GREEN + f" - encryption/   (encrypted files)    -> {ENCRYPTION_DIR.resolve()}" + RESET)
    slow_print(FG_GREEN + f" - key/          (keys for decryption) -> {KEY_DIR.resolve()}" + RESET)
    slow_print(FG_GREEN + f" - decryption/   (decrypted outputs)   -> {DECRYPTION_DIR.resolve()}\n" + RESET)
    input(FG_MAGENTA + "Press Enter to return to the main menu..." + RESET)

# --- Main menu ---
def main_menu():
    ensure_dirs()
    banner()
    while True:
        slow_print(FG_CYAN + "\nMain menu:" + RESET)
        slow_print(FG_YELLOW + "  1) Encrypt a file" + RESET)
        slow_print(FG_YELLOW + "  2) Decrypt a file" + RESET)
        slow_print(FG_YELLOW + "  3) More" + RESET)
        slow_print(FG_YELLOW + "  4) Exit" + RESET)
        choice = input(FG_MAGENTA + "Choose [1-4]: " + RESET).strip()
        if choice == "1":
            encryption_flow()
        elif choice == "2":
            decryption_flow()
        elif choice == "3":
            more_info()
        elif choice == "4":
            slow_print(FG_GREEN + "Exiting. Stay secure. ✨" + RESET)
            break
        else:
            error_log("Invalid choice. Choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        slow_print("\n" + FG_YELLOW + "Interrupted. Exiting." + RESET)
