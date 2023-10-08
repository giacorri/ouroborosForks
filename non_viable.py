from forks import *

# Initialize fork with the struct constructor
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


# Initialize fork by converting a list of tines
OTHER_NON_VIABLE_TINES_LIST= [['0', '2 a1'], ['0', '4 a1'], ['0', '5 a1'], ['0', '1', '3', '6']]
OTHER_NON_VIABLE_FORK = convert_tines_to_fork(OTHER_NON_VIABLE_TINES_LIST)

if __name__ == "__main__":
    print("NON_VIABLE_FORK:\n\t",end="")
    NON_VIABLE_FORK.print()
    NON_VIABLE_FORK.plot()
    print(f"\tIs tine 1 viable? {NON_VIABLE_FORK.is_viable(0)}")
    print(f"\tIs tine 2 viable? {NON_VIABLE_FORK.is_viable(1)}")
    print(f"\tIs closed? {NON_VIABLE_FORK.is_closed()}")

    print("OTHER_NON_VIABLE_FORK:\n\t",end="")
    OTHER_NON_VIABLE_FORK.print()
    OTHER_NON_VIABLE_FORK.plot()
    for nTine in range(len(OTHER_NON_VIABLE_FORK.get_tines())):
        print(f"Is the {nTine}-th tine {OTHER_NON_VIABLE_FORK.get_tines()[nTine]} viable? {OTHER_NON_VIABLE_FORK.is_viable(nTine)}")