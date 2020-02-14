import math
import agent
import board


###########################
# Alpha-Beta Search Agent #
###########################

#########################################################
# CS4341 AI: Group 09 ###################################
# Members: Tianyi Cui, Chioma Onyenokwe, Meixintong Zha #
#########################################################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        self.score = 100000
        self.alpha = -99999
        self.beta = 99999

    # Check if a line of identical tokens exists starting at (x,y) in direction (dx,dy)
    #
    # PARAM [board] brd:  a board state
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # PARAM [int] dx: the step in the x direction
    # PARAM [int] dy: the step in the y direction
    # PARAM [int] n: the winning condition(connectN -> connect4)
    # RETURN [int]: return the calculated score
    def n_connection_value(self,brd, x, y, dx, dy, n):
        """Return True if a line of n identical tokens exists starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + (n-1) * dx >= brd.w) or
            (y + (n-1) * dy < 0) or (y + (n-1) * dy >= brd.h)):
            return 0

        # Get token at (x,y)
        t = brd.board[y][x]

        player1 = 0
        player2 = 0

        for i in range(1, n):
            if brd.board[y + i * dy][x + i * dx] == 1:
                player1 = player1 + 1
            elif brd.board[y + i * dy][x + i * dx] == 2:
                player2 = player2 + 1

        count = 1
        for i in range(1, n):
             if brd.board[y + i * dy][x + i * dx] == t:
                 count = count + 1

        if count == n:
            if brd.board[y][x] == 1:
                return self.score
            elif brd.board[y][x] == 2:
                return -self.score+1

        return 0


    # extract_brd: take the first item from a tuple
    #
    # PARAM [list] lst:  the list of tuple you want to process
    # RETURN [list]: a list of integer
    def extract_brd(self, lst):
        return [item[0] for item in lst]


    # extract_col: take the second item from a tuple
    #
    # PARAM [list] lst:  the list of tuple you want to process
    # RETURN [list]: a list of integer
    def extract_col(self, lst):
        return [item[1] for item in lst]


    # Check if a line of n identical tokens exist in any direction
    #
    # PARAM [board] brd:  a board state
    # PARAM [int] n: the winning condition(connectN -> connect4)
    # RETURN [int]: return the total points from horizontal vertical and diagonals
    def get_score(self, brd, n):
        """Return True if a line of identical tokens exists starting at (x,y) in any direction"""
        vertical = 0
        horizontal = 0
        diag1 = 0
        diag2 = 0

        # Calculate horizontal score
        for x in range(brd.w):
            for y in range(brd.h):
                score = self.n_connection_value(brd,x,y,1,0,n)
                if score == self.score:
                    return self.score
                if score == -self.score:
                    return -self.score
                horizontal = horizontal + score

        # Calculate vertical score
        for x in range(brd.w):
            for y in range(brd.h):
                score = self.n_connection_value(brd,x,y,0,1,n)
                if score == self.score:
                    return self.score
                if score == -self.score:
                    return -self.score
                vertical = vertical + score

        # Calculate diagonal score (left top to right bottom)
        for x in range(brd.w):
            for y in range(brd.h):
                score = self.n_connection_value(brd,x,y,1,1,n)
                if score == self.score:
                    return self.score
                if score == -self.score:
                    return -self.score
                diag1 = diag1 + score

        # Calculate diagonal score (left bottom to right top)
        for x in range(brd.w):
            for y in range(brd.h):
                score = self.n_connection_value(brd,x,y,1,-1,n)
                if score == self.score:
                    return self.score
                if score == -self.score:
                    return -self.score
                diag2 = diag2 + score

        points = horizontal + vertical + diag1 + diag2
        return points


    # count_m_value: use the corrent version of get_score
    #
    # PARAM [board] brd:  a board state
    # RETURN [int]: return the total points from horizontal vertical and diagonals
    def count_m_value(self, brd):
            return self.get_score(brd,brd.n)

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        value = []
        if brd.player == 1:
            value = self.max_algorithm(brd, self.max_depth)
        else:
            value = self.min_algorithm(brd, self.max_depth)
        return value[1]


    # max_algorithm: find the max value
    #
    # PARAM [board] brd:  a board state
    # PARAM [int] current_depth: how far down the level has the alphabeta agent been
    # RETURN [list]: return a list of [value, col] where value is the current max value and col is the arg max
    def max_algorithm(self, brd, current_depth):
        value = [-99999, None]
        score = self.count_m_value(brd)
        freecols = brd.free_cols()
        # Are there legal actions left? Are the game terminal conditions met?
        if(current_depth == 0 or score == self.score or score == -self.score or not freecols):
            return [score, None]
        my_successors = self.get_successors(brd)
        brd_list = self.extract_brd(my_successors)
        col_list = self.extract_col(my_successors)
        for j in range(0, len(my_successors)):
            next_value = self.min_algorithm(brd_list[j], current_depth-1)
            if value[1] == None or next_value[0] >= value[0]:
                value[0] = next_value[0]
                value[1] = col_list[j]
                self.alpha = next_value[0]
                print("max", "current_depth", current_depth, "maxv", value[0], "col", value[1], "alpha", self.alpha, "beta", self.beta)
            if self.alpha > self.beta:
                return value

        return value


    # min_algorithm: find the min value
    #
    # PARAM [board] brd:  a board state
    # PARAM [int] current_depth: how far down the level has the alphabeta agent been
    # RETURN [list]: return a list of [value, col] where value is the current min value and col is the arg min
    def min_algorithm(self, brd, current_depth):
        value = [99999, None]
        score = self.count_m_value(brd)
        freecols = brd.free_cols()
        # Are there legal actions left? Are the game terminal conditions met?
        if (current_depth == 0 or score == self.score or score == -self.score or not freecols):
            return [score, None]
        my_successors = self.get_successors(brd)
        brd_list = self.extract_brd(my_successors)
        col_list = self.extract_col(my_successors)
        for j in range(0, len(my_successors)):
            next_value = self.max_algorithm(brd_list[j], current_depth-1)
            if value[1] == None or next_value[0] <= value[0]:
                value[1] = col_list[j]
                value[0]= next_value[0]
                self.beta = next_value[0]
                print("min", "current_depth", current_depth, "minv", value[0], "col", value[1], "alpha", self.alpha, "beta", self.beta)
            if self.alpha > self.beta:
                return value

        return value


    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb, col))
        return succ

THE_AGENT = AlphaBetaAgent("Group09", 5)
