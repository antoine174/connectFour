def _fmt(x):
    if x == float("inf"):
        return "∞"
    if x == float("-inf"):
        return "-∞"
    return str(x)


def _describe(node):
    name = "ROOT" if node.move is None else f"Col {node.move}"
    if node.is_pruned:
        return f"{name} [{node.node_type}] d={node.depth} α={_fmt(node.alpha)} β={_fmt(node.beta)} [PRUNED]"
    text = f"{name} [{node.node_type}] d={node.depth} Val={_fmt(node.value)}"
    if node.is_leaf:
        text += f" Heuristic={node.heuristic_value}"
    return text + f" α={_fmt(node.alpha)} β={_fmt(node.beta)}"


def _print_children(node, prefix):
    for i, child in enumerate(node.children):
        is_last = i == len(node.children) - 1
        print(prefix + ("└── " if is_last else "├── ") + _describe(child))
        _print_children(child, prefix + ("    " if is_last else "│   "))


def print_tree(root_node):
    print("\n=== Minimax Search Tree ===")
    print(_describe(root_node))
    _print_children(root_node, "")
    print("===========================\n", flush=True)
