# Task 2: Tic-Tac-Toe AI (Unbeatable)

An unbeatable desktop Tic-Tac-Toe game featuring a modern dark theme interface, human-vs-AI gameplay, and a decision engine driven by the Minimax algorithm with Alpha-Beta pruning.

---

## Overview

This project delivers an interactive desktop Tic-Tac-Toe game where the computer opponent represents an optimal agent. By using the Minimax search algorithm, the AI evaluates all possible future moves on the 3x3 grid, making it completely unbeatable. The game will always end in either an AI victory or a draw.

---

## Features

- **Unbeatable AI Opponent**: Driven by the Minimax algorithm with Alpha-Beta pruning to keep computation times negligible.
- **Scoreboard Tracking**: Real-time scoreboard counts Human wins, AI wins, and Draws within the match session.
- **Dynamic Highlights**: The three winning symbols are dynamically highlighted with a distinct background (Mint green) when the match concludes.
- **Start Preferences**: Allows the user to select whether the Human or the AI goes first.
- **Interactive GUI**: Smooth button hover feedback, custom cursor indicators, and separate color themes for 'X' (Cyan) and 'O' (Lavender).
- **Realistic Delay**: A brief artificial thinking delay (400–500ms) is applied to the AI turns, making the game feel natural and conversational rather than instantaneous.

---

## Minimax Algorithm Explanation

The minimax algorithm acts as a backtracking search. It recursively builds a game-tree of possible boards:
1. **Evaluation**: Returns a utility value of `+10` for an AI win, `-10` for a Human win, and `0` for a draw.
2. **Depth Discounting**: Subtracts depth from positive scores (`10 - depth`) and adds depth to negative scores (`depth - 10`) so the AI optimizes for the shortest paths to victory and stalls when facing inevitable draws/losses.
3. **Alpha-Beta Pruning**: Prunes search branches that cannot possibly influence the final minimax choice, significantly reducing the search space from $9!$ permutations.

---

## Technologies Used

- **Python 3.12+**
- **Tkinter** (Python Desktop GUI package)
- **Logging** (Standard engine trace logger)

---

## Folder Structure

```text
Task2_TicTacToeAI/
│
├── assets/             # Graphical assets
├── screenshots/        # Application screenshots
├── main.py             # Main GUI application client
├── minimax.py          # Minimax AI decision core
├── README.md           # Documentation (this file)
└── requirements.txt    # Package specifications
```

---

## Requirements

1. **Python 3.12+**
2. **Tkinter Library**:
   - On Windows/macOS, Tkinter is bundled with Python.
   - On Linux (Debian/Kali), you must install it using the system package manager:
     ```bash
     sudo apt-get update
     sudo apt-get install python3-tk
     ```

---

## Installation & Running

1. Clone or navigate to the project directory:
   ```bash
   cd Task2_TicTacToeAI
   ```
2. (Optional) Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Run the application:
   ```bash
   python3 main.py
   ```

---

## Usage Guide

- **Play**: Click any grid button to place an 'X'. The AI will immediately respond and place an 'O'.
- **Choose Who Starts**: Before playing, select the radio options **Human first** or **AI first**. The game will automatically reset and adjust.
- **Restarting**:
  - Click **Restart Match** to clear the grid board while retaining the current scoreboard tallies.
  - Click **Reset Scores** to wipe both the grid board and reset all win/draw counts back to zero.

---

## Screenshots

Below is a placeholder indicating where visual previews of the application interface are placed.

| Game Layout (Mid-game) | Game Over (AI wins highlighted) |
|:---:|:---:|
| ![Main Game Layout](screenshots/tictactoe_main_placeholder.png) | ![AI Win Highlight](screenshots/tictactoe_win_placeholder.png) |

---

## Future Improvements

- Extend grid size support to 4x4 or 5x5 boards (incorporating heuristic search limitations or depth-limit minimax).
- Add sound effects for button clicks and game end.

---

## License

This project is licensed under the [MIT License](../LICENSE).

---

## Author

- **Ritheesh MG**
- GitHub: [ritheesh2808](https://github.com/ritheesh2808)
