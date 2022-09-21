import random
import copy

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        # toggle middle
        self.board[row][col] = not self.board[row][col]
        # toggle top
        if row != 0:
            self.board[row - 1][col] = not self.board[row - 1][col]
        # toggle bottom
        if row != len(self.board) - 1:
            self.board[row + 1][col] = not self.board[row + 1][col]
        # toggle left
        if col != 0:
            self.board[row][col - 1] = not self.board[row][col - 1]
        # toggle right
        if col != len(self.board[0]) - 1:
            self.board[row][col + 1] = not self.board[row][col + 1]
        return

    def scramble(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rand = random.random()
                if rand < 0.5:
                    self.perform_move(row, col)
        return

    def is_solved(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == True:
                    return False
        return True

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        for row in range(self.rows):
            for col in range(self.cols):
                copied = LightsOutPuzzle.copy(self)
                copied.perform_move(row, col)
                s = ((row, col), copied)
                yield s

    def find_moves(self, tuple_board, visited):
        cur = (None, tuple_board)
        order = []

        while cur[1] != tuple([tuple(row) for row in self.board]):
            prev = visited[cur[1]]
            order.insert(0, prev[0])
            cur = prev

        return order

    def find_solution(self):
        queue = Queue()
        visited = {}
        queue.put(self)
        while not queue.empty():
            current = queue.get()
            cur_tuple_board = tuple([tuple(row) for row in current.get_board()])

            for move, new_p in current.successors():
                board = new_p.get_board()
                tuple_board = tuple([tuple(row) for row in board])
                if tuple_board not in visited:
                    visited[tuple_board] = (move, cur_tuple_board)

                    if new_p.is_solved():
                        return self.find_moves(tuple_board, visited)

                    queue.put(new_p)       
        return None

def create_puzzle(rows, cols):
    a = [[False for i in range(cols)] for j in range(rows)]
    return LightsOutPuzzle(a)