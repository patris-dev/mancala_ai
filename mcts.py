import numpy as np
from board import Board
import random


class State():

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
        self.wins = wins
        self.games = games

    # generates children for current state
    def generate_children(self):
        plays = self.board.legal_plays()
        children = [State(self.board.next_state(play), self, [], play)
                    for play in plays]
        self.children = children


class MCTS():

    def __init__(self):
        self.root = None
        # Takes an instance of Board and optionally som keyword arguments.
        # Initializes the list of game states and the statistics tables.

    def get_play(self, board, iterations):
        # Causes AI to calculate the best move from the current game state and returns it.

        # Root node
        self.root = State(board, None, [], None)
        self.root.generate_children()

        # Running MCTS
        for _ in range(iterations):
            self.select(self.root, iterations)

        # TODO debugging, root should have 100 games
        # for c in self.root.children:
        #     print(str(c.wins) + " " + str(c.games))

        # Returning the best play
        bestChild = max(self.root.children, key=lambda c: c.wins/c.games)
        return bestChild.play

    def select(self, state, iterations):

        # boolean flag
        expanded = False

        # if any children are unexpanded
        # expand random child
        children = state.children
        for s in children:
            if s.games <= 0:
                self.expand(s)
                expanded = True
                break
        if not expanded:
            maxVal = 0
            for s in children:
                uc = self.ucb(state.games, state.wins, self.root.games)
                if uc > maxVal:
                    maxVal = uc
                    maxState = s

            self.expand(maxState)

    def ucb(self, games, wins, totalGames):

        ub = wins/games + np.sqrt(2*np.log(totalGames)/games)
        return ub

    def expand(self, state):
        # Expands a child node after selection (generate children and then run a simulation)
        state.generate_children()
        winner = self.run_simulation(state.board)
        self.update(state, winner)

    def run_simulation(self, board):
        # Plays out a random game from the current position, returns the winning player.
        sim = Board(board.aSide.copy(), board.bSide.copy(), board.player)
        while sim.winner() == 0:
            plays = sim.legal_plays()
            selected_play = random.choice(plays)
            sim = sim.next_state(selected_play)
        return sim.winner()

    def update(self, state, winner):

        # winner = 1 = AI loss (+0)
        # winner = 2 = AI win (+1)
        # winner = -1 = draw (+0.5)
        if winner == -1:
            wins = 0.5
        elif winner == 2:
            wins = 1
        elif winner == 1:
            wins = 0

        # update all nodes in path until root is reached
        while state.parent != None:
            state.games += 1
            if not state.board.player:
                state.wins += wins
            state = state.parent

        # update root
        state.games += 1
        state.wins += wins
