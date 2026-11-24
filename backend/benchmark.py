import contextlib
import io

from board import Board
from minimax import find_best_move
from tree_printer import print_tree

MOVES = [3, 3, 2, 4, 4, 2, 3, 3, 1, 4, 2, 5, 5, 3, 2]


def build_board():
    board = Board()
    player = Board.HUMAN
    for col in MOVES:
        board.drop_piece(col, player)
        player = Board.AI if player == Board.HUMAN else Board.HUMAN
    return board


def main():
    board = build_board()
    print(f"Benchmark board ({board.disc_count} discs; 1=Human, 2=AI):")
    for row in board.grid:
        print("  " + " ".join(".XO"[cell] for cell in row))
    print()

    print(f"{'K':>2} | {'Best Col':>8} | {'Root Value':>10} | {'Nodes Expanded':>14} | "
          f"{'Pruned Branches':>15} | {'Time (ms)':>9}")
    print("-" * 75)
    trees = {}
    for k in range(1, 7):
        with contextlib.redirect_stdout(io.StringIO()):
            col, root, stats = find_best_move(board, k)
        trees[k] = root
        print(f"{k:>2} | {col:>8} | {root.value:>10} | {stats['nodes_expanded']:>14} | "
              f"{stats['pruned_branches']:>15} | {stats['execution_time_ms']:>9}")

    print("\nSample tree for K = 2:")
    print_tree(trees[2])


if __name__ == "__main__":
    main()
