# CHARACTERISTICS STRING, a list of 0s and 1s
# w = [0, 1, 0, 1, 0, 0, 1]

# TREE, a directed rooted tree graph (netoworkx DiGraph)
# graph test
# w = [0, 0, 1]
# G = nx.DiGraph()
# G.add_node("0", weight=0, type="honest", n=0)
# G.add_node("1", weight=1, type="honest", n=0)
# G.add_node("2 a1", weight=2, type="adversarial", n=1)
# G.add_node("2 a2", weight=2, type="adversarial", n=2)
# # add edges
# G.add_edge("0", "1")
# G.add_edge("1", "2 a1")
# G.add_edge("0", "2 a2")