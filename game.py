from board import Board
from mcts import MCTS
import random

board = Board([4, 4, 4, 4, 4, 4, 0], [4, 4, 4, 4, 4, 4, 0], True)

mode = int(
    input("Input 1 for singleplayer, input 2 for multiplayer, input 3 for random: "))

# Singleplayer: playing against AI
if mode == 1:
    ai = MCTS()
    while (board.winner() == 0):
        board.print()
        # Player's turn
        if board.player:
            action = int(input("Input action: "))
            if action in board.legal_plays():
                board = board.next_state(action)
            else:
                print("\nIllegal action")
        # AI's turn
        else:
            action = ai.get_play(board, 10000)
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
    ai = MCTS()
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
