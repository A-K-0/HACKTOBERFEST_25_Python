Simple GUI based mood logger
Had built this a while back but decided to upload for hacktoberfest

It is a simple desktop app to record your daily mood and short notes.
It saves your entries to a local file (mood_log.json) and shows your recent logs.

 Features

    Choose your mood (Happy, Calm, Motivated, Tired, Stressed, Neutral)

    Write an optional short note (up to 400 characters)

    View your 3 most recent mood entries

    Data automatically saved in mood_log.json

🧩 Requirements

No external dependencies — only Python’s built-in libraries:

    tkinter

    json

    os

    datetime

    (On Linux, if Tkinter isn’t installed, run: sudo apt install python3-tk)

🗂️ Files Created

    mood_logger.py → main program

    mood_log.json → stores your entries
