# Flappy Bird

A Python implementation of the classic Flappy Bird game using Pygame. Navigate a bird through pipes by flapping to avoid obstacles and achieve the highest score!

## Features

- 🎮 Classic Flappy Bird gameplay mechanics
- 🐦 Three different bird colors (Yellow, Blue, Red) that change on restart
- 🎵 Sound effects for jumping, scoring, and collisions
- 🎨 Authentic Flappy Bird sprites and graphics
- ⚡ Particle effects on jumps and collisions
- 🏆 High score tracking (saved to file)
- ⏸️ Pause functionality
- 📊 Real-time score display
- 🌊 Animated scrolling ground
- 🎯 Smooth bird rotation based on velocity

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone this repository:
```bash
git clone https://github.com/RuumiDev/flappy-bird-project.git
cd flappy-bird-project
```

2. Install the required dependency:
```bash
pip install pygame
```

3. Run the game:
```bash
python flappy_bird.py
```

**Note:** The game will automatically download all required assets (sprites, sounds, fonts) on first run if they're not present in the `assets` folder.

## How to Play

### Controls

- **SPACE** - Flap/Jump (start game when not started)
- **P** - Pause/Unpause the game
- **ESC** - Quit the game

### Objective

- Guide the bird through the gaps between pipes
- Each pipe successfully passed increases your score by 1
- Avoid hitting pipes or the ground
- Try to beat your high score!

### Gameplay

1. Press **SPACE** to start the game
2. Press **SPACE** repeatedly to keep the bird in the air
3. Navigate through the gaps in the pipes
4. If you crash, press **SPACE** to restart with a new bird color

## Project Structure

```
flappy-bird-project/
├── flappy_bird.py      # Main game file with all game logic
├── highscore.txt       # Stores the high score
├── assets/             # Game assets (auto-downloaded)
│   ├── *.png          # Sprite images
│   ├── *.wav          # Sound effects
│   └── font.ttf       # Game font
└── README.md          # This file
```

## Game Classes

- **Bird**: Handles bird physics, animation, and rendering
- **Pipe**: Manages pipe generation, movement, and collision detection
- **Particle**: Creates visual particle effects
- **Game**: Main game controller managing game state and logic

## Credits

- Original Flappy Bird game by Dong Nguyen
- Sprites and assets from the Flappy Bird open-source community
- Sound effects from the original Flappy Bird game

## License

This is a fan recreation for educational purposes. All assets belong to their respective owners.
