from forks import *

NON_VIABLE_W = [0, 1, 0, 1, 0, 0]
NON_VIABLE_FORK = Fork(NON_VIABLE_W)

NON_VIABLE_FORK.tree.add_node("2 a1", weight=2, type="adversarial", n=1)
NON_VIABLE_FORK.tree.add_edge("0", "2 a1")
NON_VIABLE_FORK.tree.add_node("4 a1", weight=4, type="adversarial", n=1)
NON_VIABLE_FORK.tree.add_edge("2 a1", "4 a1")
NON_VIABLE_FORK.tree.add_node("6 a1", weight=6, type="adversarial", n=1)
NON_VIABLE_FORK.tree.add_edge("4 a1", "6 a1")

NON_VIABLE_FORK.tree.add_node("1", weight=1, type="honest", n=0)
NON_VIABLE_FORK.tree.add_edge("0", "1")
NON_VIABLE_FORK.tree.add_node("2 a2", weight=2, type="adversarial", n=2)
NON_VIABLE_FORK.tree.add_edge("1", "2 a2")
NON_VIABLE_FORK.tree.add_node("3", weight=3, type="honest", n=0)
NON_VIABLE_FORK.tree.add_edge("2 a2", "3")
NON_VIABLE_FORK.tree.add_node("4 a2", weight=4, type="adversarial", n=2)
NON_VIABLE_FORK.tree.add_edge("3", "4 a2")
NON_VIABLE_FORK.tree.add_node("5", weight=5, type="honest", n=0)
NON_VIABLE_FORK.tree.add_edge("4 a2", "5")

if __name__ == "__main__":
    NON_VIABLE_FORK.print()
    NON_VIABLE_FORK.plot()
    print(f"Is tine 0 viable? {NON_VIABLE_FORK.is_viable(0)}")
    print(f"Is tine 1 viable? {NON_VIABLE_FORK.is_viable(1)}")