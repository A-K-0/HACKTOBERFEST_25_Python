# Pomodoro-Timer-CLI

A lightweight, dependency-free command-line Pomodoro timer.

## Features
- **Configurable durations** for focus, short break, and long break
- **Configurable cycles**
- **Cross-platform** (Windows/macOS/Linux) with optional sound beeps
- **No external packages** required

## Usage
Run with Python 3:

```bash
python pomodoro.py --work 25 --short 5 --long 15 --cycles 4
```

### Options
- `--work <minutes>`: Focus duration (default 25)
- `--short <minutes>`: Short break duration (default 5)
- `--long <minutes>`: Long break duration (default 15)
- `--cycles <n>`: Number of focus cycles (default 4)
- `--no-sound`: Disable sound notifications

### Examples
- Classic Pomodoro (25/5 with 15-minute long break, 4 cycles):
  ```bash
  python pomodoro.py
  ```
- Quick test run:
  ```bash
  python pomodoro.py --work 1 --short 1 --long 2 --cycles 2
  ```

## Notes
- On Windows, the app uses `winsound.Beep` when available; otherwise it falls back to a terminal bell.
- Press `Ctrl+C` to stop at any time.

## Contributing
This project is intended for Hacktoberfest. Feel free to open issues or PRs for enhancements such as:
- Pausing/resuming
- Custom sound themes
- Saving session stats
