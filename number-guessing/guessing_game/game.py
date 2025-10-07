#!/usr/bin/env python3
"""
Number Guessing Game (single-file)
- Difficulty levels
- Attempt counter
- Replay loop
- Built-in logic tests (run with: python game.py --test)

This file is self-contained to satisfy the "two files only" constraint
(Python + README). No external dependencies required.
"""
from __future__ import annotations
import argparse
import random
from typing import Callable, Tuple


DIFFICULTY_PRESETS = {
    "easy": {"low": 1, "high": 10, "attempts": 5},
    "medium": {"low": 1, "high": 50, "attempts": 7},
    "hard": {"low": 1, "high": 100, "attempts": 10},
}


def get_bounds_and_attempts(difficulty: str) -> Tuple[int, int, int]:
    """Return (low, high, attempts) for a difficulty. Defaults to 'medium' if unknown."""
    d = DIFFICULTY_PRESETS.get(difficulty.lower(), DIFFICULTY_PRESETS["medium"])
    return d["low"], d["high"], d["attempts"]


def evaluate_guess(secret: int, guess: int) -> str:
    """Compare a guess to the secret number.
    Returns one of: 'low', 'high', 'correct'.
    """
    if guess < secret:
        return "low"
    if guess > secret:
        return "high"
    return "correct"


def prompt_for_guess(low: int, high: int, input_func: Callable[[str], str]) -> int:
    """Prompt the user for an integer guess within [low, high]. Re-prompt on invalid input."""
    while True:
        raw = input_func(f"Enter your guess ({low}-{high}): ")
        try:
            val = int(raw.strip())
            if low <= val <= high:
                return val
            print(f"Please enter a number between {low} and {high}.")
        except ValueError:
            print("That's not a valid integer. Try again.")


def play_round(difficulty: str,
               input_func: Callable[[str], str] = input,
               print_func: Callable[[str], None] = print,
               rng: random.Random | None = None) -> bool:
    """Play a single round. Returns True if the player wants to replay, else False."""
    rng = rng or random.Random()
    low, high, attempts = get_bounds_and_attempts(difficulty)
    secret = rng.randint(low, high)

    print_func(f"\nDifficulty: {difficulty.capitalize()} | Range: {low}-{high} | Attempts: {attempts}")

    remaining = attempts
    while remaining > 0:
        print_func(f"Attempts left: {remaining}")
        guess = prompt_for_guess(low, high, input_func)
        outcome = evaluate_guess(secret, guess)
        if outcome == "correct":
            print_func(f"🎉 Correct! The number was {secret}.")
            break
        elif outcome == "low":
            print_func("Too low!")
        else:
            print_func("Too high!")
        remaining -= 1

    if remaining == 0:
        print_func(f"❌ Out of attempts. The number was {secret}.")

    # replay prompt
    while True:
        ans = input_func("Play again? (y/n): ").strip().lower()
        if ans in {"y", "yes"}:
            return True
        if ans in {"n", "no"}:
            return False
        print_func("Please enter 'y' or 'n'.")


def game_loop(difficulty: str,
              input_func: Callable[[str], str] = input,
              print_func: Callable[[str], None] = print,
              rng: random.Random | None = None) -> None:
    """Main game loop handling replay."""
    while True:
        replay = play_round(difficulty, input_func, print_func, rng)
        if not replay:
            print_func("Thanks for playing!")
            return


# ------------------------
# Built-in simple logic tests
# ------------------------

def _make_input_provider(responses):
    """Create a fake input function that pops items from 'responses'."""
    data = list(responses)

    def _inp(prompt: str) -> str:
        if not data:
            raise AssertionError(f"No more responses left for prompt: {prompt}")
        return data.pop(0)
    return _inp


def run_tests() -> None:
    print("Running tests...")

    # evaluate_guess tests
    assert evaluate_guess(50, 25) == "low"
    assert evaluate_guess(50, 75) == "high"
    assert evaluate_guess(42, 42) == "correct"

    # difficulty presets
    assert get_bounds_and_attempts("easy") == (1, 10, 5)
    assert get_bounds_and_attempts("medium") == (1, 50, 7)
    assert get_bounds_and_attempts("hard") == (1, 100, 10)
    # unknown difficulty defaults to medium
    assert get_bounds_and_attempts("unknown") == (1, 50, 7)

    # deterministic round: user guesses correctly on second try, then declines replay
    rng = random.Random(123)
    low, high, _ = get_bounds_and_attempts("easy")
    secret = rng.randint(low, high)  # peek for constructing inputs
    # First guess: wrong; Second: correct; Replay: no
    first_guess = str(secret - 1 if secret - 1 >= low else secret + 1)
    second_guess = str(secret)
    inputs = [first_guess, second_guess, "n"]

    logs = []
    def collector(msg: str):
        logs.append(msg)

    replay = play_round("easy", input_func=_make_input_provider(inputs), print_func=collector, rng=rng)
    assert replay is False
    assert any("Too" in m for m in logs), "Should provide feedback for wrong guess"
    assert any("Correct" in m for m in logs), "Should congratulate on correct guess"

    # Out-of-attempts scenario
    rng2 = random.Random(999)
    low2, high2, attempts2 = get_bounds_and_attempts("easy")
    # Provide 'attempts2' wrong guesses in range, then 'n' for replay
    wrong = str(low2) if low2 != high2 else str(low2)
    inputs2 = [wrong] * attempts2 + ["n"]

    logs2 = []
    replay2 = play_round("easy", input_func=_make_input_provider(inputs2), print_func=logs2.append, rng=rng2)
    assert replay2 is False
    assert any("Out of attempts" in m for m in logs2), "Should show out-of-attempts message"

    print("All tests passed!")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Number Guessing Game")
    parser.add_argument("--difficulty", choices=list(DIFFICULTY_PRESETS.keys()), default="medium",
                        help="Choose difficulty level.")
    parser.add_argument("--seed", type=int, default=None, help="Seed the RNG for reproducible play.")
    parser.add_argument("--test", action="store_true", help="Run built-in logic tests and exit.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.test:
        run_tests()
        return

    rng = random.Random(args.seed) if args.seed is not None else None
    game_loop(args.difficulty, rng=rng)


if __name__ == "__main__":
    main()
