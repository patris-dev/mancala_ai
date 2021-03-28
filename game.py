from board import Board
from mcts import MCTS
import random

board = Board([4, 4, 4, 4, 4, 4, 0], [4, 4, 4, 4, 4, 4, 0], True)

mode = int(
    input("Input 1 for player vs AI \ninput 2 for player vs player \ninput 3 for random vs AI \ninput 4 for AI vs AI: "))

# Singleplayer: playing against AI
if mode == 1:
    ai = MCTS(2)
    while (board.winner() == 0):
        board.print()
        # Player's turn
        if board.current_player() == 1:
            action = int(input("Input action: "))
            if action in board.legal_plays():
                board = board.next_state(action)
            else:
                print("\nIllegal action")
        # AI's turn
        else:
            action = ai.get_play(board, 1000)
            board = board.next_state(action)

    print("\nThe winner is player " + str(board.winner()) + " with a score of " +
          str(sum(board.aSide)) + " to " + str(sum(board.bSide)))

# Multiplayer: playing against yourself or a friend locally
elif mode == 2:
    while (board.winner() == 0):
        board.print()
        action = int(input("Input action: "))
        if action in board.legal_plays():
            board = board.next_state(action)
        else:
            print("\nIllegal action")

    print("\nThe winner is player " + str(board.winner()) + " with a score of " +
          str(sum(board.aSide)) + " to " + str(sum(board.bSide)))

# Random: random against AI
if mode == 3:
    ai = MCTS(2)
    while (board.winner() == 0):
        board.print()
        # Player's turn
        if board.player:
            plays = board.legal_plays()
            action = random.choice(plays)
            print("Random: " + str(action))
            board = board.next_state(action)
        # AI's turn
        else:
            action = ai.get_play(board, 1000)
            board = board.next_state(action)

    print("\nThe winner is player " + str(board.winner()) + " with a score of " +
          str(sum(board.aSide)) + " to " + str(sum(board.bSide)))

# AI vs AI
if mode == 4:
    ai1 = MCTS(1)
    ai2 = MCTS(2)
    while (board.winner() == 0):
        board.print()
        # Player's turn
        if board.current_player() == 1:
            action = ai1.get_play(board, 1000)
            board = board.next_state(action)
        # AI's turn
        else:
            action = ai2.get_play(board, 1000)
            board = board.next_state(action)

    print("\nThe winner is player " + str(board.winner()) + " with a score of " +
          str(sum(board.aSide)) + " to " + str(sum(board.bSide)))
