# Number Guessing Game

A beginner-friendly terminal game with difficulty levels, attempt counter, and a replay loop. Includes built-in logic tests (no extra files needed) to keep this project to only two files.

- **Language**: Python 3.8+
- **Files**:
  - `projects/guessing_game/game.py` (game + tests)
  - `projects/guessing_game/README.md` (this file)

## Features
- **Difficulty levels**: `easy` (1-10, 5 attempts), `medium` (1-50, 7 attempts), `hard` (1-100, 10 attempts)
- **Attempt counter** with feedback for too low/high
- **Replay loop** to play multiple rounds
- **Built-in tests**: run with a flag, no external test file
- **Deterministic mode** for demos via `--seed`

## Run
```bash
# Default (medium)
python projects/guessing_game/game.py

# Choose difficulty
python projects/guessing_game/game.py --difficulty easy
python projects/guessing_game/game.py --difficulty medium
python projects/guessing_game/game.py --difficulty hard

# Reproducible demo with a fixed RNG seed
python projects/guessing_game/game.py --difficulty easy --seed 123
```

## Example Gameplay
```
Difficulty: Medium | Range: 1-50 | Attempts: 7
Attempts left: 7
Enter your guess (1-50): 25
Too low!
Attempts left: 6
Enter your guess (1-50): 40
Too high!
Attempts left: 5
Enter your guess (1-50): 33
🎉 Correct! The number was 33.
Play again? (y/n): n
Thanks for playing!
```

## Built-in Tests
Run the simple logic tests with:
```bash
python projects/guessing_game/game.py --test
```
What this checks:
- `evaluate_guess()` returns `low/high/correct` appropriately
- Difficulty presets and defaulting
- A correct-guess path and an out-of-attempts path (using a fake input provider)

## Notes
- No external dependencies required.
- If you prefer strict type checking, you can run `mypy` locally, but it is not required.
- To keep this contribution simple: tests live inside `game.py` behind the `--test` flag.
