#!/usr/bin/env python3
"""
Tic-Tac-Toe AI - Main GUI Client
CodSoft AI Internship - Task 2
Developer: Ritheesh MG

This application implements a desktop Tic-Tac-Toe game using Tkinter.
It features a premium dark theme, a scoreboard, turn status updates, and
an option to choose who starts the game. It links to the minimax solver module.
"""

import logging
import tkinter as tk
from tkinter import messagebox
from typing import List, Optional

# Import the minimax engine logic
from minimax import check_winner, find_best_move, EMPTY, HUMAN, AI, WINNING_COMBINATIONS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class TicTacToeGUI:
    """Manages the user interface and game flow for Tic-Tac-Toe."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Tic-Tac-Toe AI")
        self.root.geometry("450x640")
        self.root.resizable(False, False)

        # Game State Variables
        self.board: List[str] = [EMPTY] * 9
        self.human_score = 0
        self.ai_score = 0
        self.draws = 0
        self.game_active = True
        self.first_player_var = tk.StringVar(value="Human") # "Human" or "AI"
        self.current_turn = HUMAN # HUMAN starts by default

        # Premium Dark Color Palette
        self.colors = {
            "bg": "#181825",          # Deep background
            "card_bg": "#1e1e2e",     # Surface background
            "button_bg": "#313244",   # Base button color
            "button_hover": "#45475a",# Hover highlight
            "text": "#cdd6f4",        # Warm white text
            "subtext": "#a6adc8",     # Muted text
            "x_color": "#89dceb",     # Cyan for Human (X)
            "o_color": "#f5c2e7",     # Pink/Lavender for AI (O)
            "win_bg": "#a6e3a1",      # Light Green for winning combination
            "win_fg": "#11111b",      # Contrast dark text for winning combo
            "accent": "#89b4fa",      # Pastel Blue for restarts
            "accent_fg": "#11111b",
            "accent_hover": "#b4befe"
        }

        # Apply root styling
        self.root.configure(bg=self.colors["bg"])

        self._create_widgets()
        self._reset_game()

    def _create_widgets(self) -> None:
        """Constructs the GUI layout."""
        # --- Header Section (Scores & Options) ---
        header_frame = tk.Frame(self.root, bg=self.colors["card_bg"], pady=15)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(
            header_frame,
            text="Unbeatable Tic-Tac-Toe AI",
            font=("Helvetica", 14, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text"]
        )
        title_lbl.pack()

        # Scoreboard Frame
        score_frame = tk.Frame(header_frame, bg=self.colors["card_bg"], pady=10)
        score_frame.pack(fill=tk.X)

        self.lbl_human = tk.Label(
            score_frame,
            text="Human (X): 0",
            font=("Helvetica", 11, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["x_color"]
        )
        self.lbl_human.pack(side=tk.LEFT, expand=True)

        self.lbl_draws = tk.Label(
            score_frame,
            text="Draws: 0",
            font=("Helvetica", 11, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["subtext"]
        )
        self.lbl_draws.pack(side=tk.LEFT, expand=True)

        self.lbl_ai = tk.Label(
            score_frame,
            text="AI (O): 0",
            font=("Helvetica", 11, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["o_color"]
        )
        self.lbl_ai.pack(side=tk.LEFT, expand=True)

        # First turn preference selectors
        pref_frame = tk.Frame(header_frame, bg=self.colors["card_bg"])
        pref_frame.pack(pady=(5, 0))

        pref_lbl = tk.Label(
            pref_frame,
            text="Starts: ",
            font=("Helvetica", 9),
            bg=self.colors["card_bg"],
            fg=self.colors["subtext"]
        )
        pref_lbl.pack(side=tk.LEFT)

        human_opt = tk.Radiobutton(
            pref_frame,
            text="Human first",
            variable=self.first_player_var,
            value="Human",
            font=("Helvetica", 9),
            bg=self.colors["card_bg"],
            fg=self.colors["text"],
            activebackground=self.colors["card_bg"],
            activeforeground=self.colors["text"],
            selectcolor=self.colors["bg"],
            command=self._pref_changed
        )
        human_opt.pack(side=tk.LEFT, padx=10)

        ai_opt = tk.Radiobutton(
            pref_frame,
            text="AI first",
            variable=self.first_player_var,
            value="AI",
            font=("Helvetica", 9),
            bg=self.colors["card_bg"],
            fg=self.colors["text"],
            activebackground=self.colors["card_bg"],
            activeforeground=self.colors["text"],
            selectcolor=self.colors["bg"],
            command=self._pref_changed
        )
        ai_opt.pack(side=tk.LEFT)

        # --- Game Status Label ---
        self.lbl_status = tk.Label(
            self.root,
            text="Your Turn (X)",
            font=("Helvetica", 12, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            pady=15
        )
        self.lbl_status.pack()

        # --- Grid Area (Buttons) ---
        grid_outer = tk.Frame(self.root, bg=self.colors["bg"])
        grid_outer.pack(pady=5)

        self.buttons: List[tk.Button] = []
        for i in range(9):
            btn = tk.Button(
                grid_outer,
                text="",
                font=("Helvetica", 24, "bold"),
                width=5,
                height=2,
                bg=self.colors["button_bg"],
                fg=self.colors["text"],
                activebackground=self.colors["button_hover"],
                bd=0,
                cursor="hand2",
                command=lambda idx=i: self._cell_clicked(idx)
            )
            # Standard grid arrangement
            row, col = divmod(i, 3)
            btn.grid(row=row, column=col, padx=6, pady=6)

            # Bind hover events
            btn.bind("<Enter>", lambda e, b=btn: self._btn_hover(b))
            btn.bind("<Leave>", lambda e, b=btn: self._btn_leave(b))

            self.buttons.append(btn)

        # --- Footer Controls ---
        footer_frame = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        footer_frame.pack(fill=tk.X)

        self.restart_btn = tk.Button(
            footer_frame,
            text="Restart Match",
            font=("Helvetica", 11, "bold"),
            bg=self.colors["accent"],
            fg=self.colors["accent_fg"],
            activebackground=self.colors["accent_hover"],
            activeforeground=self.colors["accent_fg"],
            bd=0,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self._reset_game
        )
        self.restart_btn.pack(side=tk.LEFT, expand=True)
        self.restart_btn.bind("<Enter>", lambda e: self.restart_btn.configure(bg=self.colors["accent_hover"]))
        self.restart_btn.bind("<Leave>", lambda e: self.restart_btn.configure(bg=self.colors["accent"]))

        self.reset_scores_btn = tk.Button(
            footer_frame,
            text="Reset Scores",
            font=("Helvetica", 11, "bold"),
            bg=self.colors["button_bg"],
            fg=self.colors["text"],
            activebackground=self.colors["button_hover"],
            activeforeground=self.colors["text"],
            bd=0,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self._reset_scores
        )
        self.reset_scores_btn.pack(side=tk.RIGHT, expand=True)
        self.reset_scores_btn.bind("<Enter>", lambda e: self.reset_scores_btn.configure(bg=self.colors["button_hover"]))
        self.reset_scores_btn.bind("<Leave>", lambda e: self.reset_scores_btn.configure(bg=self.colors["button_bg"]))

    def _btn_hover(self, btn: tk.Button) -> None:
        """Handles grid button hover state."""
        # Only hover if active and empty
        if self.game_active and btn["text"] == "":
            btn.configure(bg=self.colors["button_hover"])

    def _btn_leave(self, btn: tk.Button) -> None:
        """Restores grid button leave state."""
        if self.game_active and btn["text"] == "":
            btn.configure(bg=self.colors["button_bg"])

    def _pref_changed(self) -> None:
        """Callback when 'Starts' radio button is clicked."""
        self._reset_game()

    def _reset_scores(self) -> None:
        """Resets the scores and restart game."""
        self.human_score = 0
        self.ai_score = 0
        self.draws = 0
        self._update_scoreboard()
        self._reset_game()
        logging.info("Scoreboard reset.")

    def _update_scoreboard(self) -> None:
        """Syncs the GUI scoreboard with state variables."""
        self.lbl_human.configure(text=f"Human (X): {self.human_score}")
        self.lbl_draws.configure(text=f"Draws: {self.draws}")
        self.lbl_ai.configure(text=f"AI (O): {self.ai_score}")

    def _reset_game(self) -> None:
        """Resets board and sets up the starting player."""
        self.board = [EMPTY] * 9
        self.game_active = True

        # Clear buttons
        for btn in self.buttons:
            btn.configure(
                text="",
                bg=self.colors["button_bg"],
                state=tk.NORMAL,
                disabledforeground=self.colors["text"]
            )

        # Decide who starts based on the selected setting
        starts = self.first_player_var.get()
        if starts == "Human":
            self.current_turn = HUMAN
            self.lbl_status.configure(text="Your Turn (X)", fg=self.colors["x_color"])
        else:
            self.current_turn = AI
            self.lbl_status.configure(text="AI is thinking...", fg=self.colors["o_color"])
            # Give a small delay before AI makes its move to look realistic
            self.root.after(400, self._ai_move)

        logging.info("Game reset. Starting turn: %s", self.current_turn)

    def _cell_clicked(self, index: int) -> None:
        """Handles human cell selection click."""
        if not self.game_active or self.board[index] != EMPTY or self.current_turn != HUMAN:
            return

        # Player move
        self.board[index] = HUMAN
        self.buttons[index].configure(
            text=HUMAN,
            disabledforeground=self.colors["x_color"],
            state=tk.DISABLED
        )
        logging.info("Human clicked index: %d", index)

        # Check state
        if self._evaluate_game_state():
            return

        # Handover to AI
        self.current_turn = AI
        self.lbl_status.configure(text="AI is thinking...", fg=self.colors["o_color"])
        self.root.after(500, self._ai_move)

    def _ai_move(self) -> None:
        """Performs AI calculations and updates board state."""
        if not self.game_active:
            return

        # Find best move using minimax
        best_move_idx = find_best_move(self.board)

        if best_move_idx != -1:
            self.board[best_move_idx] = AI
            self.buttons[best_move_idx].configure(
                text=AI,
                disabledforeground=self.colors["o_color"],
                state=tk.DISABLED
            )
            logging.info("AI clicked index: %d", best_move_idx)

        # Check state
        if self._evaluate_game_state():
            return

        # Handover to Human
        self.current_turn = HUMAN
        self.lbl_status.configure(text="Your Turn (X)", fg=self.colors["x_color"])

    def _evaluate_game_state(self) -> bool:
        """
        Assesses winner state. Updates score, highlights, and returns status.
        
        Returns:
            True if game ended (Winner or Tie), False otherwise.
        """
        state = check_winner(self.board)

        if state is None:
            return False

        self.game_active = False

        if state == HUMAN:
            self.human_score += 1
            self.lbl_status.configure(text="You Win!", fg=self.colors["x_color"])
            self._highlight_win(HUMAN)
            self._update_scoreboard()
            messagebox.showinfo("Game Over", "Congratulations! You won the game!")

        elif state == AI:
            self.ai_score += 1
            self.lbl_status.configure(text="AI Wins!", fg=self.colors["o_color"])
            self._highlight_win(AI)
            self._update_scoreboard()
            messagebox.showinfo("Game Over", "AI wins! Better luck next time.")

        elif state == "Tie":
            self.draws += 1
            self.lbl_status.configure(text="It's a Draw!", fg=self.colors["subtext"])
            self._update_scoreboard()
            messagebox.showinfo("Game Over", "It's a draw!")

        # Disable all remaining buttons
        for btn in self.buttons:
            if btn["state"] != tk.DISABLED:
                btn.configure(state=tk.DISABLED)

        return True

    def _highlight_win(self, winner: str) -> None:
        """Highlights the three winning buttons."""
        win_color = self.colors["x_color"] if winner == HUMAN else self.colors["o_color"]
        
        # Check which combination was the winner
        for a, b, c in WINNING_COMBINATIONS:
            if self.board[a] == self.board[b] == self.board[c] == winner:
                for idx in (a, b, c):
                    self.buttons[idx].configure(
                        bg=self.colors["win_bg"],
                        disabledforeground=self.colors["win_fg"]
                    )
                break


def main() -> None:
    """Application entry point."""
    try:
        root = tk.Tk()
        app = TicTacToeGUI(root)
        root.mainloop()
    except Exception as e:
        logging.critical("Failed to launch Tic-Tac-Toe game: %s", str(e))
        messagebox.showerror("Fatal Error", f"Failed to start Tic-Tac-Toe:\n{str(e)}")


if __name__ == "__main__":
    main()
