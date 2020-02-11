import math
import agent
import board
###########################
# Alpha-Beta Search Agent #
###########################

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

    # Check if a line of identical tokens exists starting at (x,y) in direction (dx,dy)
    #
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # PARAM [int] dx: the step in the x direction
    # PARAM [int] dy: the step in the y direction
    # RETURN [Bool]: True if n tokens of the same type have been found, False otherwise
    def n_connection_value(self,brd, x, y, dx, dy, n):
        """Return True if a line of n identical tokens exists starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + (n-1) * dx >= brd.w) or
            (y + (n-1) * dy < 0) or (y + (n-1) * dy >= brd.h)):
            return False
        # Get token at (x,y)
        t = brd.board[y][x]
        # Go through elements
        for i in range(1, n):
            if brd.board[y + i*dy][x + i*dx] != t:
                return False
        return True

    # Python3 program to extract first and last
    # element of each sublist in a list of lists
    def extract_brd(self, lst):
        return [item[0] for item in lst]


    # Python3 program to extract first and last
    # element of each sublist in a list of lists
    def extract_col(self, lst):
        return [item[1] for item in lst]

    def getKey(self,item):
        return item[1]


    def sortSuccessors(self, succ, brd):
        stack = []
        sorted_list = []
        for i in range(0, brd.w):
           stack.append(succ[i])

#TODO edit for n = 5
        for i in range(0, len(stack)):
            if self.getKey(stack[i]) == 3:
                sorted_list.append(stack.remove(stack[i]))

        for i in range(0, len(stack)):
            if self.getKey(stack[i]) == 2 or self.getKey(stack[i]) == 4:
                sorted_list.append(stack.remove(stack[i]))




    # Check if a line of n identical tokens exist in any direction
    #
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # RETURN [Bool]: True if n tokens of the same type have been found, False otherwise
    def is_any_n_at(self,brd, x, y, n):
        """Return True if a line of identical tokens exists starting at (x,y) in any direction"""
        return (self.n_connection_value(brd, x, y, 1, 0 , n) or  # Horizontal
                self.n_connection_value(brd, x, y, 0, 1, n) or  # Vertical
                self.n_connection_value(brd, x, y, 1, 1, n) or  # Diagonal up
                self.n_connection_value(brd, x, y, 1, -1, n))  # Diagonal down


    def count_m_value(self, brd):
        for x in range(brd.w):
            for y in range(brd.h):
                if (brd.board[y][x] != 0) and self.max_depth == 5 and self.is_any_n_at(brd,x,y,5):
                    if brd.board[y][x]==1:
                        return 5
                    else:
                        return -5
                if (brd.board[y][x] != 0) and self.is_any_n_at(brd,x,y,4):
                    if brd.board[y][x]==1:
                        return 4
                    else:
                        return -4
                if (brd.board[y][x] != 0) and self.is_any_n_at(brd,x,y,3):
                    if brd.board[y][x]==1:
                        return 3
                    else:
                        return -3
                if (brd.board[y][x] != 0) and self.is_any_n_at(brd, x, y, 2):
                    if brd.board[y][x] == 1:
                        return 2
                    else:
                        return -2
                if (brd.board[y][x] != 0) and self.is_any_n_at(brd,x,y,1):
                    if brd.board[y][x]==1:
                        return 1
                    else:
                        return -1


        return 0

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here



        (maxv, col) = self.max(brd, 0, 0)
        return col


    # find the max value (the max number of identical tokens in a r)
    def max(self, brd, current_depth, last_move):

        col = last_move
        current_depth = current_depth + 1
        maxv = -4
        if current_depth == self.max_depth * 2:
            maxv = self.count_m_value(brd)
            print("max", "current_depth", current_depth, "maxv", maxv, "col", col)
            return (maxv,last_move)

        my_successors = self.get_successors(brd)
        brd_list = self.extract_brd(my_successors)
        col_list = self.extract_col(my_successors)
        for j in range(0, len(my_successors)):
            (minv,min_col) = self.min(brd_list[j], current_depth, col_list[j])
            if minv > maxv:
                maxv = minv
                col = col_list[j]
                print("max", "current_depth", current_depth, "maxv", maxv, "col", col)
            elif minv<maxv:
                break


        return (maxv, col)


    def min(self, brd, current_depth, last_move):
        current_depth = current_depth + 1
        col = last_move
        minv = 4
        if current_depth == self.max_depth * 2:
            maxv = self.count_m_value(brd)
            print("min", "current_depth", current_depth, "minv", minv, "col", col)
            return (maxv, last_move)

        my_successors = self.get_successors(brd)
        brd_list = self.extract_brd(my_successors)
        col_list = self.extract_col(my_successors)
        for j in range(0, len(my_successors)):
            current_tuple = my_successors[j]
            (maxv, max_col) = self.max(brd_list[j], current_depth,col_list[j])
            if maxv < minv:
                minv = maxv
                col = col_list[j]
                print("min", "current_depth", current_depth, "minv", minv, "col", col)
            elif maxv > minv:
                break


        return (minv, col)


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
            succ.append((nb,col))
        return succ
