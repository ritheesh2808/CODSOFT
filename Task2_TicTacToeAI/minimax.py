#!/usr/bin/env python3
"""
Tic-Tac-Toe AI - Minimax Engine
CodSoft AI Internship - Task 2
Developer: Ritheesh MG

This module handles the core game board evaluation and the unbeatable Minimax
algorithm with Alpha-Beta pruning to optimize move search speed.
"""

from typing import List, Optional, Tuple

# Constants for the game pieces
EMPTY = ""
HUMAN = "X"
AI = "O"

# Indices combinations representing winning rows, columns, and diagonals
WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
    (0, 4, 8), (2, 4, 6)              # Diagonals
]


def check_winner(board: List[str]) -> Optional[str]:
    """
    Checks the current board for a winner.
    
    Args:
        board: A list of 9 strings representing the Tic-Tac-Toe grid.
        
    Returns:
        'X' if Human wins, 'O' if AI wins, 'Tie' if it's a draw, or None if the game is active.
    """
    # Check winning configurations
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]

    # Check for tie
    if EMPTY not in board:
        return "Tie"

    # Game still active
    return None


def minimax(
    board: List[str],
    depth: int,
    is_maximizing: bool,
    alpha: float,
    beta: float
) -> int:
    """
    Minimax algorithm with Alpha-Beta pruning.
    
    Args:
        board: A list of 9 strings representing the Tic-Tac-Toe grid.
        depth: The depth of the search tree.
        is_maximizing: True if assessing the AI move, False if assessing the Human move.
        alpha: The best score the maximizer can guarantee so far.
        beta: The best score the minimizer can guarantee so far.
        
    Returns:
        The best score for the current board state.
    """
    winner = check_winner(board)
    
    # Base cases - terminal nodes
    if winner == AI:
        return 10 - depth  # AI wins (prefer faster wins)
    elif winner == HUMAN:
        return depth - 10  # Human wins (AI prefers stalling human wins)
    elif winner == "Tie":
        return 0

    if is_maximizing:
        max_eval = -float("inf")
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                evaluation = minimax(board, depth + 1, False, alpha, beta)
                board[i] = EMPTY
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break  # Prune branch
        return int(max_eval)
    else:
        min_eval = float("inf")
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                evaluation = minimax(board, depth + 1, True, alpha, beta)
                board[i] = EMPTY
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break  # Prune branch
        return int(min_eval)


def find_best_move(board: List[str]) -> int:
    """
    Scans the board and computes the optimal move index for the AI.
    
    Args:
        board: A list of 9 strings representing the Tic-Tac-Toe grid.
        
    Returns:
        Index (0-8) representing the best move.
    """
    best_score = -float("inf")
    best_move = -1

    for i in range(9):
        if board[i] == EMPTY:
            # Simulate the move
            board[i] = AI
            # Compute score using Minimax
            score = minimax(board, 0, False, -float("inf"), float("inf"))
            # Undo simulated move
            board[i] = EMPTY

            if score > best_score:
                best_score = score
                best_move = i

    return best_move
