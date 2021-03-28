import numpy as np
from termcolor import colored


class Board():
    """
    Board (no. of stones on board, player, etc.)
    """

    # Initialise board
    def __init__(self, aSide, bSide, player):
        self.set(aSide, bSide, player)

    # Setting board variables
    def set(self, aSide, bSide, player):
        self.aSide = aSide
        self.bSide = bSide
        self.player = player

    # Representing the board as a string (unused)
    def __repr__(self):
        if (self.player):
            return "\n{0:<3} {1:<3} {2:<3} {3:<3} {4:<3} {5:<3} {6:<3}\n    {7:<3} {8:<3} {9:<3} {10:<3} {11:<3} {12:<3} {13:<3}\nPlayer 1's turn".format(
                *self.bSide[::-1], *self.aSide)
        else:
            return "\n{0:<3} {1:<3} {2:<3} {3:<3} {4:<3} {5:<3} {6:<3}\n    {7:<3} {8:<3} {9:<3} {10:<3} {11:<3} {12:<3} {13:<3}\nPlayer 2's turn".format(
                *self.aSide[::-1], *self.bSide)

    # Prints the board in colors
    def print(self):
        if (self.player):
            print(colored("\n{0:<3}".format(self.bSide[6]), 'red', attrs=['bold']),
                  colored("{1:<3} {2:<3} {3:<3} {4:<3} {5:<3} {6:<3}".format(
                      *self.bSide[::-1]), 'red'),
                  colored("\n    {0:<3} {1:<3} {2:<3} {3:<3} {4:<3} {5:<3}".format(
                      *self.aSide), 'blue'),
                  colored("{0:<3}".format(
                      self.aSide[6]), 'blue', attrs=['bold']),
                  colored("\n    {0:<3} {1:<3} {2:<3} {3:<3} {4:<3} {5:<3}".format(
                      *range(6)), 'white', attrs=['dark']),
                  "\nPlayer 1's turn")
        else:
            print(colored("\n{0:<3}".format(self.aSide[6]), 'blue', attrs=['bold']),
                  colored("{1:<3} {2:<3} {3:<3} {4:<3} {5:<3} {6:<3}".format(
                      *self.aSide[::-1]), 'blue'),
                  colored("\n    {0:<3} {1:<3} {2:<3} {3:<3} {4:<3} {5:<3}".format(
                      *self.bSide), 'red'),
                  colored("{0:<3}".format(
                      self.bSide[6]), 'red', attrs=['bold']),
                  colored("\n    {0:<3} {1:<3} {2:<3} {3:<3} {4:<3} {5:<3}".format(
                      *range(6)), 'white', attrs=['dark']),
                  "\nPlayer 2's turn")

    # Returns current player number (1 or 2)
    def current_player(self):
        return 1 if self.player else 2

    # Returns board state after a specific play
    def next_state(self, play):
        player = self.player
        a = self.aSide.copy()
        b = self.bSide.copy()
        nInitial = 0
        replay = False

        if player:
            nPebbles = self.aSide[play]
            a[play] = 0
        else:
            nPebbles = self.bSide[play]
            b[play] = 0

        while nPebbles > 0:

            for i in range(play + 1 - nInitial, 7):
                if nPebbles > 0:
                    if player:
                        if nPebbles == 1:
                            if i == 6:
                                replay = True
                                a[i] += 1
                            elif a[i] == 0:
                                a[6] += 1 + b[6 - i - 1]
                                b[6 - i - 1] = 0
                            else:
                                a[i] += 1
                        else:
                            a[i] += 1
                    else:
                        if nPebbles == 1:
                            if i == 6:
                                replay = True
                                b[i] += 1
                            elif b[i] == 0:
                                b[6] += 1 + a[6 - i - 1]
                                a[6 - i - 1] = 0
                            else:
                                b[i] += 1
                        else:
                            b[i] += 1

                    nPebbles -= 1

            for i in range(0, 6):
                if nPebbles > 0:
                    if player:
                        b[i] += 1
                    else:
                        a[i] += 1

                    nPebbles -= 1

            nInitial = play + 1

        if replay:
            player = not player

        return Board(a, b, not player)

    # Returns array of numbers corresponding to legal plays
    def legal_plays(self):
        # figure out which side to consider
        if self.player:
            side = self.aSide
        else:
            side = self.bSide

        # determine legal plays from num. of non-empty pits
        legal_plays = []
        for i in range(0, 6):
            if side[i] > 0:
                legal_plays.append(i)
        return legal_plays

    # Returns winner:
    # -1 - tie
    #  0 - not a terminal state
    #  1 - player 1
    #  2 - player 2
    def winner(self):
        if sum(self.aSide[:6]) == 0 or sum(self.bSide[:6]) == 0:
            self.aSide[6] += sum(self.aSide[:6])
            self.bSide[6] += sum(self.bSide[:6])
            self.aSide[:6] = [0, 0, 0, 0, 0, 0]
            self.bSide[:6] = [0, 0, 0, 0, 0, 0]

            if self.aSide[6] > self.bSide[6]:
                return 1
            elif self.aSide[6] == self.bSide[6]:
                return -1
            else:
                return 2
        else:
            return 0
