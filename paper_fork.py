from forks import *

PAPER_W = [0, 1, 0, 1, 0, 0, 1, 1, 0]
PAPER_FORK = Fork(PAPER_W)

PAPER_FORK.tree.add_node("2a1", weight=2, type="a")
PAPER_FORK.tree.add_edge("0", "2a1")
PAPER_FORK.tree.add_node("3", weight=3, type="h")
PAPER_FORK.tree.add_edge("2a1", "3")

PAPER_FORK.tree.add_node("1", weight=1, type="h")
PAPER_FORK.tree.add_edge("0", "1")
PAPER_FORK.tree.add_node("2a2", weight=2, type="a")
PAPER_FORK.tree.add_edge("1", "2a2")
PAPER_FORK.tree.add_node("4a1", weight=4, type="a")
PAPER_FORK.tree.add_edge("2a2", "4a1")
PAPER_FORK.tree.add_node("6", weight=6, type="h")
PAPER_FORK.tree.add_edge("4a1", "6")
PAPER_FORK.tree.add_node("8a1", weight=8, type="a")
PAPER_FORK.tree.add_edge("6", "8a1")
PAPER_FORK.tree.add_node("9", weight=9, type="h")
PAPER_FORK.tree.add_edge("8a1", "9")

PAPER_FORK.tree.add_node("4a2", weight=4, type="a")
PAPER_FORK.tree.add_edge("1", "4a2")
PAPER_FORK.tree.add_node("5", weight=5, type="h")
PAPER_FORK.tree.add_edge("4a2", "5")

if __name__ == "__main__":
    PAPER_FORK.print()
    PAPER_FORK.plot()
    print(f"Is tine 0 viable? {PAPER_FORK.is_viable(0)}")
    print(f"Is tine 1 viable? {PAPER_FORK.is_viable(1)}")
    print(f"Is tine 2 viable? {PAPER_FORK.is_viable(2)}")
    print(f"height of fork: {PAPER_FORK.get_height()}")
    print(f"reserve of tine 0: {PAPER_FORK.get_tines()[0]} is {PAPER_FORK.reserve( PAPER_FORK.get_tines()[0] )}")