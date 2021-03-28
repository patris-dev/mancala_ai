from board import Board
from mcts import MCTS
import random

board = Board([4, 4, 4, 4, 4, 4, 0], [4, 4, 4, 4, 4, 4, 0], True)
strength = 1000

mode = int(
    input("Input 1 for player vs AI \ninput 2 for player vs player \ninput 3 for random vs AI \ninput 4 for AI vs AI: "))

# Player vs AI
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
            action = ai.get_play(board, strength)
            board = board.next_state(action)

    print("\nThe winner is player " + str(board.winner()) + " with a score of " +
          str(sum(board.aSide)) + " to " + str(sum(board.bSide)))

# Player vs Player
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

# AI vs Random
if mode == 3:
    ai = MCTS(2)
    p1w = 0
    p2w = 0
    for _ in range(10):
        board = Board([4, 4, 4, 4, 4, 4, 0], [4, 4, 4, 4, 4, 4, 0], True)
        while (board.winner() == 0):
            board.print()
            # Random's turn
            if board.player:
                plays = board.legal_plays()
                action = random.choice(plays)
                print("Random: " + str(action))
                board = board.next_state(action)
            # AI's turn
            else:
                action = ai.get_play(board, strength)
                board = board.next_state(action)

        print("\nThe winner is player " + str(board.winner()) + " with a score of " +
              str(sum(board.aSide)) + " to " + str(sum(board.bSide)))

        if board.winner() == 1:
            p1w += 1
        else:
            p2w += 1

    print("player 1 wins: " + str(p1w))
    print("player 2 wins: " + str(p2w))

# AI vs AI
if mode == 4:
    ai1 = MCTS(1)
    ai2 = MCTS(2)
    p1w = 0
    p2w = 0
    for _ in range(10):
        board = Board([4, 4, 4, 4, 4, 4, 0], [4, 4, 4, 4, 4, 4, 0], True)
        while (board.winner() == 0):
            board.print()
            # AI 1's turn
            if board.current_player() == 1:
                action = ai1.get_play(board, strength)
                board = board.next_state(action)
            # AI 2's turn
            else:
                action = ai2.get_play(board, strength)
                board = board.next_state(action)

        print("\nThe winner is player " + str(board.winner()) + " with a score of " +
              str(sum(board.aSide)) + " to " + str(sum(board.bSide)))

        if board.winner() == 1:
            p1w += 1
        else:
            p2w += 1

    print("player 1 wins: " + str(p1w))
    print("player 2 wins: " + str(p2w))
