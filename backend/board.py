from constants import ROWS, COLS, EMPTY, HUMAN, AI, COLUMN_ORDER
from heuristic import ALL_WINDOWS


class Board:
    ROWS = ROWS
    COLS = COLS
    EMPTY = EMPTY
    HUMAN = HUMAN
    AI = AI

    def __init__(self):
        self.grid = [[EMPTY] * COLS for _ in range(ROWS)]
        self.disc_count = 0

    def get_next_open_row(self, col):
        for row in range(ROWS - 1, -1, -1):
            if self.grid[row][col] == EMPTY:
                return row
        return -1

    def get_valid_moves(self):
        return [col for col in COLUMN_ORDER if self.grid[0][col] == EMPTY]

    def drop_piece(self, col, player):
        row = self.get_next_open_row(col)
        self.grid[row][col] = player
        self.disc_count += 1
        return row

    def undo_piece(self, col):
        for row in range(ROWS):
            if self.grid[row][col] != EMPTY:
                self.grid[row][col] = EMPTY
                self.disc_count -= 1
                return

    def is_full(self):
        return self.disc_count == ROWS * COLS

    def count_connected_fours(self, player):
        total = 0
        for window in ALL_WINDOWS:
            if all(self.grid[r][c] == player for r, c in window):
                total += 1
        return total

    def to_matrix(self):
        return [row[:] for row in self.grid]
