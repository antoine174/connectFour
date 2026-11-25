from constants import ROWS, COLS, EMPTY, HUMAN, AI

def _build_windows():
    windows = []
    for dr, dc in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
        for r in range(ROWS):
            for c in range(COLS):
                end_r, end_c = r + 3 * dr, c + 3 * dc
                if 0 <= end_r < ROWS and 0 <= end_c < COLS:
                    windows.append([(r + i * dr, c + i * dc) for i in range(4)])
    return windows


ALL_WINDOWS = _build_windows()

POSITION_WEIGHTS = [
    [1, 2, 3, 4, 3, 2, 1],
    [2, 3, 4, 5, 4, 3, 2],
    [3, 4, 5, 6, 5, 4, 3],
    [3, 4, 5, 6, 5, 4, 3],
    [2, 3, 4, 5, 4, 3, 2],
    [1, 2, 3, 4, 3, 2, 1],
]

FOUR_SCORE = 100
PLAYABLE_THREAT_SCORE = 35
FLOATING_THREAT_SCORE = 15
OPEN_TWO_SCORE = 5
NEXT_TURN_THREAT_BONUS = 50


def evaluate_board(board, next_player):
    grid = board.grid

    if board.is_full():
        exact = FOUR_SCORE * (board.count_connected_fours(AI) - board.count_connected_fours(HUMAN))
        return exact, {"locked_fours": exact, "threats": 0, "open_twos": 0,
                       "position": 0, "total": exact}

    next_open_row = [board.get_next_open_row(c) for c in range(COLS)]

    locked_fours = 0
    threats = 0
    open_twos = 0
    playable_counts = {}

    for window in ALL_WINDOWS:
        cells = [grid[r][c] for r, c in window]
        ai_count = cells.count(AI)
        human_count = cells.count(HUMAN)

        if ai_count and human_count:
            continue
        owner = AI if ai_count else HUMAN
        sign = 1 if owner == AI else -1
        count = max(ai_count, human_count)

        if count == 4:
            locked_fours += sign * FOUR_SCORE
        elif count == 3:
            r, c = next(cell for cell in window if grid[cell[0]][cell[1]] == EMPTY)
            if r == next_open_row[c]:
                threats += sign * PLAYABLE_THREAT_SCORE
                if owner == next_player:
                    playable_counts[c] = playable_counts.get(c, 0) + 1
            else:
                threats += sign * FLOATING_THREAT_SCORE
        elif count == 2:
            open_twos += sign * OPEN_TWO_SCORE

    if playable_counts:
        best_gain = max(playable_counts.values())
        if next_player == AI:
            threats += NEXT_TURN_THREAT_BONUS * best_gain
        elif next_player == HUMAN:
            threats -= NEXT_TURN_THREAT_BONUS * best_gain

    position = 0
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == AI:
                position += POSITION_WEIGHTS[r][c]
            elif grid[r][c] == HUMAN:
                position -= POSITION_WEIGHTS[r][c]

    total = locked_fours + threats + open_twos + position
    return total, {"locked_fours": locked_fours, "threats": threats,
                   "open_twos": open_twos, "position": position, "total": total}
