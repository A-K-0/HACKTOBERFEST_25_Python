# 🎮 Tower Defense Game

A classic tower defense game built with Python and Pygame. Place towers strategically to defend against waves of enemies!

## 🚀 Quick Start

### Installation
```bash
# Create virtual environment
python3 -m venv game_env
source game_env/bin/activate  # On Windows: game_env\Scripts\activate

# Install pygame
pip install pygame

# Run the game
python3 tower_defense.py
```

## 🎯 How to Play

1. **Select a tower** from the bottom menu
2. **Click on the green area** to place it (not on the gray path!)
3. **Click "Start Wave"** to begin
4. **Defend your base** - Don't let enemies reach the end!
5. **Press R** to restart after game over

## 🗼 Tower Types

| Tower | Cost | Damage | Range | Best For |
|-------|------|--------|-------|----------|
| **Basic** (Blue) | $100 | 20 | Medium | Balanced gameplay |
| **Sniper** (Purple) | $200 | 50 | Long | Tough enemies |
| **Cannon** (Orange) | $150 | 15 | Short | Fast firing |

## 💡 Tips

- Place towers at corners where enemies slow down
- Mix different tower types for better coverage
- Earn money by defeating enemies
- Each wave gets progressively harder

## 🐛 Troubleshooting

**"command not found: pip"**  
Use `pip3` instead: `pip3 install pygame`

**"externally-managed-environment" error**  
Use a virtual environment (see installation above)

**Game won't start**  
Verify pygame: `python3 -c "import pygame; print('OK')"`

## 📊 Game Info

- **Starting Money**: $500
- **Lives**: 20
- **Wave Bonus**: $100 per wave completed

Good luck, Commander! 🎖️