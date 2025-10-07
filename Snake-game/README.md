# Snake Game

This is a classic Snake game built with Python's turtle module where you control a snake to eat food, grow longer, and try to beat your high score.

## How to Play

1. Run `main.py` using Python:
   ```
   python main.py
   ```
2. A game window will open with a green snake in the center.
3. Use the keyboard to control the snake's direction:
   - `W` or `↑` Arrow - Move Up
   - `S` or `↓` Arrow - Move Down
   - `A` or `←` Arrow - Move Left
   - `D` or `→` Arrow - Move Right
4. Guide the snake to eat the red food circles.
5. Each food eaten makes the snake grow longer and increases your score by 10 points.
6. Avoid hitting the walls or your own body, or the game will reset.
7. Try to beat your high score!

## Requirements

- Python 3.x

## Game Features

- Progressive difficulty (game speeds up as you grow)
- Score tracking with high score display
- Smooth keyboard controls
- Collision detection for walls and self

## Example Gameplay

```
Game starts with snake at center
Score: 0  High Score: 0

[Player eats food]
Score: 10  High Score: 10
Snake grows by one segment

[Player continues eating]
Score: 50  High Score: 50
Game becomes faster

[Player hits wall or body]
Game resets
Score: 0  High Score: 50
```