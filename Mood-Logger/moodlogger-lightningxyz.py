import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "mood_log.json"
MAX_PREVIEW = 3
MAX_NOTE_CHARS = 400

MOODS = {
    "happy": ("Happy", "#FFD54F", "#2B2B2B"),
    "calm": ("Calm", "#90CAF9", "#0B3142"),
    "motivated": ("Motivated", "#A5D6A7", "#073B1A"),
    "tired": ("Tired", "#B0BEC5", "#1B1B1B"),
    "stressed": ("Stressed", "#EF9A9A", "#330000"),
    "neutral": ("Neutral", "#ECEFF1", "#121212"),
}

def load_logs():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_logs(logs):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def add_entry(mood_key, note):
    logs = load_logs()
    entry = {"mood": mood_key, "note": note.strip(), "timestamp": datetime.utcnow().isoformat() + "Z"}
    logs.insert(0, entry)
    save_logs(logs)

class MoodLoggerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mood Logger")
        self.resizable(False, False)
        self.style = ttk.Style(self)
        self._build_ui()
        self.update_preview()

    def _build_ui(self):
        pad = 10
        frm = ttk.Frame(self, padding=pad)
        frm.grid(row=0, column=0, sticky="nsew")

        moods_frame = ttk.LabelFrame(frm, text="How are you feeling?")
        moods_frame.grid(row=0, column=0, padx=pad, pady=(0, pad), sticky="ew")
        self.selected_mood = tk.StringVar(value="neutral")
        col = 0
        for key, (label, bg, fg) in MOODS.items():
            b = ttk.Radiobutton(moods_frame, text=label, variable=self.selected_mood, value=key, command=self._apply_theme)
            b.grid(row=0, column=col, padx=6, pady=6)
            col += 1

        note_frame = ttk.Frame(frm)
        note_frame.grid(row=1, column=0, sticky="ew")
        ttk.Label(note_frame, text="Short note (optional):").grid(row=0, column=0, sticky="w")
        self.note_text = tk.Text(note_frame, width=48, height=6, wrap="word")
        self.note_text.grid(row=1, column=0, pady=6)
        self.char_count_label = ttk.Label(note_frame, text=f"0 / {MAX_NOTE_CHARS}")
        self.char_count_label.grid(row=2, column=0, sticky="e")
        self.note_text.bind("<<Modified>>", self._on_text_change)

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=2, column=0, pady=(6, 0), sticky="ew")
        save_btn = ttk.Button(btn_frame, text="Save Mood", command=self._on_save)
        save_btn.grid(row=0, column=0, padx=(0, 6))
        clear_btn = ttk.Button(btn_frame, text="Clear Note", command=self._clear_note)
        clear_btn.grid(row=0, column=1)

        preview_frame = ttk.LabelFrame(frm, text="Recent entries")
        preview_frame.grid(row=3, column=0, pady=(pad, 0), sticky="ew")
        self.preview_box = tk.Text(preview_frame, width=60, height=8, state="disabled", wrap="word")
        self.preview_box.grid(row=0, column=0, padx=6, pady=6)

        self._apply_theme()

    def _apply_theme(self):
        key = self.selected_mood.get()
        _, bg, fg = MOODS.get(key, MOODS["neutral"])
        self.configure(bg=bg)
        self.preview_box.configure(bg="white")
        self.note_text.configure(bg="white")
        self.current_bg = bg
        self.current_fg = fg

    def _on_text_change(self, event=None):
        self.note_text.edit_modified(False)
        text = self.note_text.get("1.0", "end-1c")
        if len(text) > MAX_NOTE_CHARS:
            self.note_text.delete("1.0", "end")
            self.note_text.insert("1.0", text[:MAX_NOTE_CHARS])
            messagebox.showinfo("Limit", f"Note truncated to {MAX_NOTE_CHARS} characters.")
        self.char_count_label.config(text=f"{len(self.note_text.get('1.0','end-1c'))} / {MAX_NOTE_CHARS}")

    def _clear_note(self):
        self.note_text.delete("1.0", "end")
        self._on_text_change()

    def _on_save(self):
        mood = self.selected_mood.get()
        note = self.note_text.get("1.0", "end-1c").strip()
        add_entry(mood, note)
        messagebox.showinfo("Saved", "Mood saved successfully!")
        self._clear_note()
        self.update_preview()

    def update_preview(self):
        logs = load_logs()
        display = []
        for entry in logs[:MAX_PREVIEW]:
            mood_key = entry.get("mood", "neutral")
            mood_label = MOODS.get(mood_key, ("Neutral", "#ECEFF1", "#000"))[0]
            ts = entry.get("timestamp", "")
            try:
                dt = datetime.fromisoformat(ts.replace("Z", ""))
                ts_f = dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                ts_f = ts
            note = entry.get("note", "")
            display.append(f"[{ts_f}] {mood_label}\n{note}\n" + "-"*40)
        preview_text = "\n".join(display) if display else "No entries yet. Add your mood above."
        self.preview_box.configure(state="normal")
        self.preview_box.delete("1.0", "end")
        self.preview_box.insert("1.0", preview_text)
        self.preview_box.configure(state="disabled")

if __name__ == "__main__":
    app = MoodLoggerApp()
    app.mainloop()
