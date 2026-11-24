import time
from dataclasses import dataclass, field
from typing import Optional

from board import Board
from heuristic import evaluate_board
from tree_printer import print_tree

INF = float("inf")


def _fmt(x):
    if x == INF:
        return "∞"
    if x == -INF:
        return "-∞"
    return x


@dataclass
class TreeNode:
    move: Optional[int]
    depth: int
    node_type: str
    value: Optional[int] = None
    alpha: float = -INF
    beta: float = INF
    is_leaf: bool = False
    is_pruned: bool = False
    heuristic_value: Optional[int] = None
    children: list = field(default_factory=list)

    def to_dict(self):
        return {
            "move": self.move,
            "depth": self.depth,
            "node_type": self.node_type,
            "value": self.value,
            "alpha": _fmt(self.alpha),
            "beta": _fmt(self.beta),
            "is_leaf": self.is_leaf,
            "is_pruned": self.is_pruned,
            "heuristic_value": self.heuristic_value,
            "children": [child.to_dict() for child in self.children],
        }


def find_best_move(board, k):
    stats = {"nodes_expanded": 0, "pruned_branches": 0}
    start = time.perf_counter()

    root = TreeNode(move=None, depth=0, node_type="MAX")
    _minimax(board, root, k, -INF, INF, True, stats)

    best_col = None
    for child in root.children:
        if not child.is_pruned and child.value == root.value:
            best_col = child.move
            break

    stats["execution_time_ms"] = round((time.perf_counter() - start) * 1000, 2)
    stats["k"] = k
    print_tree(root)
    return best_col, root, stats


def _minimax(board, node, remaining_depth, alpha, beta, is_maximizing, stats):
    if remaining_depth == 0 or board.is_full():
        score, _ = evaluate_board(board)
        node.is_leaf = True
        node.value = score
        node.heuristic_value = score
        node.alpha, node.beta = alpha, beta
        stats["nodes_expanded"] += 1
        return score

    stats["nodes_expanded"] += 1
    player = Board.AI if is_maximizing else Board.HUMAN
    child_type = "MIN" if is_maximizing else "MAX"
    best = -INF if is_maximizing else INF
    moves = board.get_valid_moves()

    for index, col in enumerate(moves):
        child = TreeNode(move=col, depth=node.depth + 1, node_type=child_type)
        node.children.append(child)

        board.drop_piece(col, player)
        value = _minimax(board, child, remaining_depth - 1, alpha, beta,
                         not is_maximizing, stats)
        board.undo_piece(col)

        if is_maximizing:
            best = max(best, value)
            alpha = max(alpha, best)
        else:
            best = min(best, value)
            beta = min(beta, best)

        if beta <= alpha:
            for skipped_col in moves[index + 1:]:
                node.children.append(TreeNode(
                    move=skipped_col, depth=node.depth + 1, node_type=child_type,
                    alpha=alpha, beta=beta, is_pruned=True))
                stats["pruned_branches"] += 1
            break

    node.value = best
    node.alpha, node.beta = alpha, beta
    return best
