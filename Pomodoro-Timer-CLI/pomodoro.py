#!/usr/bin/env python3
"""
Pomodoro Timer CLI

A simple command-line Pomodoro timer with configurable durations and cycles.
Works on Windows, macOS, and Linux without external dependencies.
"""

import argparse
import sys
import time


def fmt_time(seconds: int) -> str:
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"


def beep(enabled: bool = True, times: int = 1) -> None:
    if not enabled:
        return
    try:
        # winsound is available on Windows
        import winsound  # type: ignore

        for _ in range(times):
            winsound.Beep(1000, 200)
            time.sleep(0.05)
    except Exception:
        # Fallback to terminal bell
        for _ in range(times):
            print("\a", end="", flush=True)
            time.sleep(0.1)


def countdown(total_seconds: int, label: str, sound: bool) -> None:
    start = time.time()
    end = start + total_seconds
    try:
        while True:
            remaining = max(0, int(end - time.time()))
            # Draw a single-line updating timer
            sys.stdout.write(f"\r{label:<14} | {fmt_time(remaining)}    ")
            sys.stdout.flush()
            if remaining <= 0:
                break
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")
        raise
    finally:
        print()  # move to next line
    beep(sound, times=2)


def run_pomodoro(work: int, short: int, long: int, cycles: int, sound: bool) -> None:
    if work <= 0 or short <= 0 or long <= 0 or cycles <= 0:
        raise ValueError("All durations and cycle count must be positive integers.")

    try:
        for c in range(1, cycles + 1):
            print(f"\nCycle {c}/{cycles}")
            countdown(work * 60, "Focus", sound)
            if c < cycles:
                countdown(short * 60, "Short break", sound)
            else:
                countdown(long * 60, "Long break", sound)
        print("All cycles complete. Great job!")
        beep(sound, times=3)
    except KeyboardInterrupt:
        # Graceful shutdown already printed in countdown
        pass


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Run a Pomodoro timer with configurable durations and cycles.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--work", type=int, default=25, help="Focus duration in minutes")
    parser.add_argument("--short", type=int, default=5, help="Short break in minutes")
    parser.add_argument("--long", type=int, default=15, help="Long break in minutes")
    parser.add_argument("--cycles", type=int, default=4, help="Number of focus cycles")
    parser.add_argument(
        "--no-sound", action="store_true", help="Disable sound notifications"
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    run_pomodoro(args.work, args.short, args.long, args.cycles, not args.no_sound)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
