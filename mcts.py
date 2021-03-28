import numpy as np
from board import Board
import random


class State():

    # Initializing state (0 wins and games by default)
    def __init__(self, board, parent, children, play):
        self.set(board, parent, children, play, 0, 0)

    # board - game board
    # parent - parent State object
    # children - array of children State objects
    # play - integer representing the play to get to this node from parent
    # wins - no. of simulated wins
    # games - no. of simulated games (if 0, node hasn't been expanded yet)
    def set(self, board, parent, children, play, wins, games):
        self.board = board
        self.parent = parent
        self.children = children
        self.play = play
        self.wins = wins
        self.games = games

    # Generates children for current state
    def generate_children(self):
        plays = self.board.legal_plays()
        children = [State(self.board.next_state(play), self, [], play)
                    for play in plays]
        self.children = children


class MCTS():

    # Initializes AI with their dedicated player number (1 or 2)
    def __init__(self, player):
        self.player = player
        self.root = None

    # Causes AI to calculate the best move from the current game state and returns it.
    def get_play(self, board, iterations):

        # Root node
        self.root = State(board, None, [], None)
        self.root.generate_children()

        # Running MCTS
        for _ in range(iterations):
            self.select(self.root)

        # Choosing the best play based on denominator (games played)
        bestChild = max(self.root.children, key=lambda c: c.games)

        # Returning the best play
        winrate = 100 * bestChild.wins / bestChild.games if bestChild.board.current_player() == self.player else 100 * (1 -
                                                                                                                        (bestChild.wins/bestChild.games))

        print("AI: {0:d}, perceived winrate: {1:.2f}%".format(
            bestChild.play, winrate))
        return bestChild.play

    def select(self, state):

        # If any children are unexpanded, expand child
        childrenExpanded = True
        children = state.children
        for s in children:
            if s.games <= 0:
                self.expand(s)
                childrenExpanded = False
                break
        # If all children were already expanded, move on to UCB
        if childrenExpanded:
            maxVal = -50000
            for s in children:
                uc = self.ucb1(s, state)
                if uc > maxVal:
                    maxVal = uc
                    maxState = s
            if len(children) != 0:
                self.select(maxState)
            else:
                self.expand(state)

    def ucb1(self, child, parent):
        # If the child node belongs to same as parent, return the standard ucb value
        if child.board.player == parent.board.player:
            return child.wins/child.games + np.sqrt(2*np.log(parent.games)/child.games)
        # If the child and parent are different, inverse the utility (winrate)
        else:
            return (1 - child.wins/child.games) + np.sqrt(2*np.log(parent.games)/child.games)

    def expand(self, state):
        # Expands a child node after selection (generate children and then run a simulation)
        state.generate_children()
        winner = self.run_simulation(state.board)
        self.update(state, winner)

    def run_simulation(self, board):
        # Plays out a random game from the current position, returns the winning player
        sim = Board(board.aSide.copy(), board.bSide.copy(), board.player)
        while sim.winner() == 0:
            plays = sim.legal_plays()
            selected_play = random.choice(plays)
            sim = sim.next_state(selected_play)
        return sim.winner()

    def update(self, state, winner):

        # Update all nodes in path until root is reached
        while state.parent != None:
            state.games += 1
            # Opponent wins
            if winner != self.player and state.board.current_player() != self.player:
                state.wins += 1
            # AI wins
            elif winner == self.player and state.board.current_player() == self.player:
                state.wins += 1
            # Draw
            elif winner == -1:
                state.wins += 0.5
            state = state.parent

        # Update root
        state.games += 1
        if winner == self.player:
            state.wins += 1
