# FORKING LIBRARY v2
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import *

# To save all log messages in a file:
# import sys
# sys.stdout = open('myForks.log', 'w')

# TINE, a list of nodes
# t = [0, 1, 3, 5, 6 , 9]

# FORK, a list of tines (directed rooted tree)
# F = [
#       [0, 1, 3, 5, 6 , 9],
#       [0, 1, 2, 4, 6, 8]
# ]

# CHARACTERISTICS STRING, a list of 0s and 1s
# w = [0, 1, 0, 1, 0, 0, 1]

def tine_length(tine):
    return len(tine) - 1

def truncate_to_node(tine, node):
    return tine[:tine.index(node)+1]

def truncate_k(tine, k):
    if k > tine_length(tine):
        return [0]
    else:
        return tine[:len(tine)-k]

def label(tine):
    return tine[len(tine)-1]

def is_honest(tine, w):
    return w[label(tine)-1] == 0

def is_prefix(tine1, tine2):
    if len(tine1) > len(tine2):
        return False
    else:
        return tine1 == tine2[:len(tine1)]

# length of the path from the genesis block to the (honest) node
def depth(node, fork):
    # search for node in fork
    for tine in fork:
        if node in tine:
            return tine.index(node)

def get_honest_slots(w):
    honestSlots = []
    for sl in range(len(w)):
        if w[sl] == 0:
            honestSlots.append(sl+1)
    return honestSlots

def is_viable(nTine, fork, w):
    tine = fork[nTine]
    labelTine = label(tine)
    # if tine is the genesis block
    if labelTine == 0:
        return True
    # get honest slots
    else:
        honestSlots = get_honest_slots(w)
        # remove slots after the label of the tine
        honestSlots = [slot for slot in honestSlots if slot <= labelTine]
        # remove honest slots which are not nodes of the fork
        for h in reversed(honestSlots):
            present = False
            for tine in fork:
                if h in tine:
                    present = True
                    break
            if not present:
                honestSlots.remove(h)
        for h in honestSlots:
            # if depth of honest node is greater than depth of label of tine
            if depth(h, fork) > depth(labelTine, fork):         
                # tine is not viable
                return False
        return True

def print_forks(forks):
    print("[")
    for fork in forks:
        print(f"\t{fork}")
    print("]")

def make_tree(fork, w):
    G = nx.DiGraph()
    G.add_node(0, weight=0, type='honest')
    for tine in fork:
        previousNode = 0
        for node in tine:
            # if node is not the genesis block
            if node != 0:
                # if honest 
                if w[node-1] == 0:
                    # if node is not already in the graph
                    if node not in G.nodes():
                        # add node to graph
                        G.add_node(str(node), weight=node, type='honest')
                        # add edge from previous node to the current node
                        G.add_edge(previousNode, str(node))
                        previousNode = str(node)
                # if adversarial
                else:
                    # count how many adversarial nodes with the same weight are already in the graph
                    conta = 0
                    # for each node in the graph
                    for nodoSalvato in G.nodes():
                        # get weight of node
                        weightNodoSalvato = G.nodes[nodoSalvato]['weight']
                        # increment if weight of node is equal to the weight of the current node
                        if weightNodoSalvato == node:
                            conta += 1
                    G.add_node(str(node)+" a"+str(conta+1), weight=node, type='adversarial')
                    G.add_edge(previousNode, str(node)+" a"+str(conta+1))
                    previousNode = str(node)+" a"+str(conta+1)
    # check if two nodes of same weight are connected to the same next honest node
    for weight in range(1, len(w)+1):                                           
        nodesOfSameWeight = []
        for node in G.nodes():
            if G.nodes[node]['weight'] == weight:
                nodesOfSameWeight.append(node)
        for node in nodesOfSameWeight:
            # get next honest node
            nextHonestNode = None
            # for each successor of the node
            for successor in G.successors(node):
                # if successor is honest
                if G.nodes[successor]['type'] == 'honest':
                    # set next honest node to successor
                    nextHonestNode = successor
                    break
# check if another node of same weight is connected to the same next honest node
            # for each node of same weight
            for node2 in nodesOfSameWeight:
                # if node is not the same node
                if node != node2:
                    # for each successor of the node
                    for successor in G.successors(node2):
                        # if successor is the same next honest node
                        if successor == nextHonestNode:
                            # remove node from graph
                            G.remove_node(node)
                break
    return G

def plot_fork(fork, w, quick=False):
    G = make_tree(fork, w)
    pos = pydot_layout(G, prog="dot", root=0)
    # label nodes with their weight
    node_labels = {node: str(G.nodes[node]['weight']) for node in G.nodes()}
    # get y positions from weights
    y_positions = {node: -G.nodes[node]['weight'] for node in G.nodes()}
    # grow towards east
    pos = {k: (-y_positions[k], pos[k][0],) for k in pos}
    # color nodes according to type
    node_colors = {'honest': 'green', 'adversarial': 'red'}
    node_colors = [node_colors[G.nodes[node]['type']] for node in G.nodes()]
    # draw graph
    nx.draw(G, pos, labels=node_labels, with_labels=True, node_color=node_colors, node_size=500)
    # display the x-axis
    plt.axhline(y=0, color='gray', linestyle='-', lw=1)
    # display "Slot"
    plt.text(0, 2, "Slot", horizontalalignment='center')
    # display 1, 2, 3, ...
    for x in range(0, len(w)):
        plt.text(x+1, 2, str(x+1), horizontalalignment='center')    
    # diplay "w"
    plt.text(0, -4, "w", horizontalalignment='center')
    # display w_0, w_1, w_2, ...
    for x in range(0, len(w)):
        plt.text(x+1, -4, str(w[x]), horizontalalignment='center')
    # display vertical lines dividing slots
    for y in range(0, len(w) + 1):
        plt.axvline(x=y+0.5, color='gray', linestyle='--', lw=1)
    # plot
    if quick:
        plt.show(block=False)
        plt.pause(0.2)
        plt.close()
    else:
        plt.show()
    
def maxvalid(fork):
    max = 0
    for tine in fork:
        if tine_length(tine) > max:
            max = tine_length(tine)
    # check how many tines have maximum length and which ones they are
    maximalTines = []
    for tineNumber in range(len(fork)):
        tine = fork[tineNumber]
        if tine_length(tine) == max:
            # append tine index
            maximalTines.append(tine)
    return max, maximalTines

def clean_forks(forks):
    # for each fork sort tines
    for fork in forks:
        fork.sort()
    k = 0
    # remove fork duplicates
    for i in range(len(forks)):
        # decrement i in case the list has been shortened
        i -= k                                      
        fork = forks[i]
        for j in range(i+1, len(forks)):
            # decrement j in case the list has been shortened
            j -= k
            if i != j:
                fork2 = forks[j]
                if fork == fork2:
                    forks.pop(j)
                    k += 1                          
    # sort forks
    forks.sort()
    return forks

def honest_slot_gen_forks(slot, fork, w):
    generatedFromFork = []
    # If the prior slot is honest or the genesis block
    # if w[slot-1] == 0 or slot == 0:
    if True:
        max, maximalTines = maxvalid(fork)
        print(f"\t\tMaximal tines: {maximalTines}")
        # for each maximal tine
        for maximalTine in maximalTines:
            # apped new block to maximal tine
            generatedFromFork.append(fork.copy())
            # find index of maximal tine in fork
            maxTineIndex = 0
            for k in range(len(fork)):
                if maximalTine == fork[k]:
                    maxTineIndex = k
                    break
            # append new block to maximal tine in the copied fork
            newTine = maximalTine.copy()
            newTine.append(slot+1)
            generatedFromFork[len(generatedFromFork)-1][maxTineIndex] = newTine

            print(f"\t\t\t{generatedFromFork[len(generatedFromFork)-1]}")
    """ # Otherwise, if the prior slot is adversarial
    else:
        # the honest player sees only one of the adversarial ramifications
        # count how many blocks the adversary has placed in the previous slot and where they are
        blocksInPreviousSlot = 0
        for tineNumber in range(len(fork)):
            tine = fork[tineNumber]
            if label(tine) == slot:
                blocksInPreviousSlot += 1
                tineWithBlock = tineNumber
        # for  """
    return generatedFromFork

def adversarial_slot_gen_forks(slot, fork, w):
    # initialize with the fork where the adversary does not place any block
    generatedFromFork = [fork.copy()]
    # for each tine in the fork
    for nTine in range(len(fork)):
        tine = fork[nTine]
        print(f"\t\t{nTine+1}-th tine: {tine}")
        # for each node in the tine
        for node in tine:       
            print(f"\t\t\tNode {node}: ", end="")
            # duplicate fork
            generatedFromFork.append(fork.copy())
            # if node is the genesis block
            if node == 0:
                newTine = [0, slot+1]
                generatedFromFork[len(generatedFromFork)-1].append(newTine)
            # node is the leaf
            elif node == tine[len(tine)-1]:
                # append new block to end of the tine
                newTine = tine.copy()
                newTine.append(slot+1)
                generatedFromFork[len(generatedFromFork)-1][nTine] = newTine
            # node is internal
            else:
                # truncate tine to the node
                newTine = truncate_to_node(tine.copy(), node)
                # append block to truncated tine     
                newTine.append(slot+1)
                # append new tine
                generatedFromFork[len(generatedFromFork)-1].append(newTine)
            print(f"{generatedFromFork[len(generatedFromFork)-1]}")
    return generatedFromFork

def gen_forks(w):
    forks = []
    # Initialize with fork with only genesis block
    forks.append( [ [0] ] )
    for slot in range(len(w)):
        print(f"Slot {slot+1}:")
        print(f"\t{len(forks)} forks:")
        generated = []
        for fork in forks:
            print(f"\t- {fork}:")
            if w[slot] == 0:
                print("\033[0;32m", end="")
                generated.extend(honest_slot_gen_forks(slot, fork, w))
            else:
                print("\033[0;31m", end="")
                generated.extend(adversarial_slot_gen_forks(slot, fork, w))
            print("\033[0m", end="")
        forks = clean_forks(generated.copy())
    return forks

def kCP(k, w):
    forks = gen_forks(w)
    print_forks(forks)
    for fork in forks:
        print("fork =", fork)
        viableTines = []
        for tineNumber in range(len(fork)):
            tine = fork[tineNumber]
            if is_viable(tineNumber, fork, w):
                viableTines.append(tine)
        print("\tviable tines =", viableTines)
        # for every pair of viable tines, check if they are k-CP
        for i in range(len(viableTines)):
            for j in range(i+1, len(viableTines)):
                tine1 = viableTines[i]
                tine2 = viableTines[j]
                print("\t\tPair of viable tines:", tine1, "and", tine2)
                if label(tine1) > label(tine2):
                    # invert tines
                    tine1, tine2 = tine2, tine1
                print(f"\t\t\tLabel({tine1}) = {label(tine1)} <= {label(tine2)} = label({tine2})")
                print(f"\t\t\ttine1 = {tine1}, tine2 = {tine2}")
                print(f"\t\t\ttruncate({tine1}, {k}) = {truncate_k(tine1, k)}", end=" ")
                # if tine1 is not a prefix of tine2
                if is_prefix(truncate_k(tine1, k), tine2) == False:
                    print(f"is not a prefix of {tine2}")
                    print(f"\tFork {fork} of {w} breaks {k}-CP")
                    print(f"\tBecause truncate({tine1}, {k}) = {truncate_k(tine1, k)} is not a prefix of {tine2})")
                    plot_fork(fork, w)
                    return False
                else:
                    print(f"is a prefix of {tine2}\t\tOK")
                if label(tine1) == label(tine2):
                    print(f"\t\t\tLabel({tine1}) = {label(tine1)} = {label(tine2)} = label({tine2})")
                    # invert tines
                    tine1, tine2 = tine2, tine1
                    # check if tine1 is a prefix of tine2
                    if is_prefix(truncate_k(tine1, k), tine2) == False:
                        print("Fork", fork,"of", w, "breaks", k, "-CP")
                        print("Because " + str(truncate_k(tine1, k)) + " is not a prefix of " + str(tine2) + ")")
                        plot_fork(fork, w)
                        return False
    return True

def isClosed(fork, w):
    # check if each leaf is honest
    for tine in fork:
        if w[label(tine)-1] == 1:
            return False
    return True

def gap(tine, fork, w):
    if not isClosed(fork, w):
        return "Error: fork is not closed"
    # find maximum 
    max = 0
    for tine2 in fork:
        if tine_length(tine2) > max:
            max = tine_length(tine2)
    return max - tine_length(tine)  

def reserve(tine, w):
    count = 0
    for sl in range(label(tine), len(w)-1):
        if w[sl] == 1:
            count += 1
    return count

def reach(tine, fork, w):
    if not isClosed(fork, w):
        print("Error: fork is not closed")
        return None
    return reserve(tine, w) - gap(tine, fork, w)

def maxReach(fork, w):
    max = 0
    for tine in fork:
        if reach(tine, fork, w) > max:
            max = reach(tine, fork, w)
    return max

def get_tines(G):
    root = 0
    startingTines = []
    endingTines = []
    finishedTines = []
    startingTines.append([root])
    finished = False
    while not finished:
        print(f"Processing startingTines = {startingTines}")
        for tine in startingTines:
            print(f"\ttine = {tine}")
            # check successors of the leaf
            leaf = tine[len(tine)-1]
            print(f"\tleaf = {leaf}")
            leaf_successors = list(G.successors(leaf))
            if len(leaf_successors) == 0:
                print("\t\tleaf is a leaf")
                # leaf is a leaf
                finishedTines.append(tine)
            else:
                print("\t\tleaf is not a leaf")
                # leaf is not a leaf
                for succ in leaf_successors:
                    print(f"\t\t\tsucc = {succ}")
                    new_tine = tine.copy()
                    new_tine.append(succ)
                    endingTines.append(new_tine)
        # update startingTines
        startingTines = endingTines.copy()
        endingTines = []
        if len(startingTines) == 0:
            finished = True
    return finishedTines

def find_tine(tine, fork, w):
    G = make_tree(fork, w)
    graph_tines = get_tines(G)
    might_be_the_same = []
    print(f"Finding tine {tine} in the graph of the fork {fork}")
    for graph_tine in graph_tines:
        print(f"\tgraph_tine = {graph_tine}")
        # compare nodes of tine with the weight of the nodes of graph_tine
        if len(tine) != len(graph_tine):
            # tine and graph_tine have different lengths
            print("\t\tdifferent lengths")
            # try another graph_tine
            continue
        print("\t\tsame length")
        for i in range(1, len(tine)):
            print(f"graph_tine[{i}] = {graph_tine[i]}")
            node_weight = G.nodes[graph_tine[i]]['weight']
            print(f"\tnode_weight = {node_weight}")
            if tine[i] != node_weight:
                # tine and graph_tine have different nodes
                print(f"\t\tdifferent nodes: tine[{i}] = {tine[i]}, graph_tine[{i}] = {node_weight}")
                break
        print("\t\tmight be the same")
        might_be_the_same.append(graph_tine)
    if len(might_be_the_same) == 1:
        return might_be_the_same[0]
    else:
        print(f"Check {len(might_be_the_same)} tines which could match")
        for tine in might_be_the_same:
            print(f"\t{tine}")
        return might_be_the_same
            
def common_edge(tine1, tine2, fork, w):
    tine1_in_graph = find_tine(tine1, fork, w)
    tine2_in_graph = find_tine(tine2, fork, w)
    # check if the two tines have a common edge in the tree
    node1 = tine1_in_graph[1]
    node2 = tine2_in_graph[1]
    if node1 == node2:
        print("common node different from root -> common edge")
        return True
    return False

def margin(fork, w):
    if not isClosed(fork, w):
        return "Error: fork is not closed"
    max = 0
    for tine1 in fork:
        for tine2 in fork:
            if tine1 != tine2:
                if not common_edge(tine1, tine2, fork, w):
                    # min = reach(tine1) if tine_length(tine1) < tine_length(tine2) else tine_length(tine2)
                    min = reach(tine1, fork, w) if reach(tine1, fork, w) < reach(tine2, fork, w) else reach(tine2, fork, w)
                    if min > max:
                        max = min
    return max  



if  __name__ == "__main__":

    # TRUNCATE EXAMPLE
    print("Truncate example")
    t = [0, 1, 3, 5, 6 , 9, 13, 14, 19]
    print(f"\tt = {t}")
    print(f"\ttruncate_to_node(t, 5) = {truncate_to_node(t, 5)}")
    print(f"\ttruncate_k(t, 3) = {truncate_k(t, 3)}")

    # PREFIX EXAMPLE
    print("Prefix example")
    t1 = [0, 1, 3, 5, 6 , 9]
    t2 = [0, 1, 2, 4, 6, 8]
    t3 = [0, 1, 3, 5, 6 , 9, 10, 13]

    print(f"\tt1 = {t1}")
    print(f"\tt2 = {t2}")
    print(f"\tt3 = {t3}")
    print(f"\tis_prefix(t1, t2) = {is_prefix(t1, t2)}")
    print(f"\tis_prefix(t1, t3) = {is_prefix(t1, t3)}")
    print(f"\tis_prefix(t2, t3) = {is_prefix(t2, t3)}")
    print(f"\tis_prefix(t3, t1) = {is_prefix(t3, t1)}")

    # PAPER'S FORK EXAMPLE
    print("Paper fork example")
    wPaper = [0, 1, 0, 1, 0, 0, 1, 1, 0]                    
    print("\tw =", wPaper)
    forkPaper = [
            [0, 2, 3],
            [0, 1, 4, 5],
            [0, 1, 2, 4, 6, 8, 9]
    ]
    print("\tF =", forkPaper)
    print("\tdepth(5, F) =", depth(5, forkPaper))
    print("\tlength of tine 3", forkPaper[2], "is", tine_length(forkPaper[2]))
    print("\tand its label is", label(forkPaper[2]) )
    print("\tis tine 3 honest?", is_honest(forkPaper[2], wPaper))
    print("\tis tine 3 viable?", is_viable(2, forkPaper, wPaper))
    plot_fork(forkPaper, wPaper)

    # VIABLE EXAMPLE
    print("Viability example")
    wViableEx = [0, 1, 0, 1, 0, 1]
    print("\tw =", wViableEx)
    FViableEx = [[0, 2, 4, 6], [0, 1, 2, 3, 4, 5]]
    print("\tF =", FViableEx)
    print("\tIs the first tine " + str(FViableEx[0]) + " viable?", is_viable(0, FViableEx, wViableEx))
    print("\tIs the second tine " + str(FViableEx[1]) + " viable?", is_viable(1, FViableEx, wViableEx))
    plot_fork(FViableEx, wViableEx)

    # FORK GENERATION EXAMPLE
    print("Fork generation example")
    wGenFork = [0, 1, 0, 1]
    forks = gen_forks(wGenFork)
    for fork in forks:
        plot_fork(fork, wGenFork, True)

    # K-CP EXAMPLE
    print("k-CP example")
    wKcp = [0, 1, 0, 1]
    print("\tw =", wKcp)
    k = 1
    print("\tIs", wKcp, "k-CP for k =", 2, "?", kCP(2, wKcp))

    # FORKS CLEANING
    forksToClean = [
        [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]],
        [[0,1,9], [0,1,3,6,9], [0,1,5,6,9], [0,1,2,3,6,9], [0,1,2,3,5,6,9], [0,1,2,3,4,5,6,9], [0,1,2,3,4,5,6,7,9], [0,1,2,3,4,5,6,7,8,9], [0,1,2,3,4,5,6,7,8,9,10]],
        [[0,1,2,3], [0,1,5,6,9]],
        [[0,1,2,3], [0,1,3,6,9]],
        [[0,1,9], [0,1,3,6,9], [0,1,5,6,9], [0,1,2,3,5,6,9], [0,1,2,3,4,5,6,9], [0,1,2,3,4,5,6,7,9], [0,1,2,3,6,9], [0,1,2,3,4,5,6,7,8,9], [0,1,2,3,4,5,6,7,8,9,10]],
        [[0,1,2,3], [0,1,5,6,9]],
        [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    ]
    print_forks(forksToClean)
    print( f"length of forks before cleaning = {len(forksToClean)}")
    cleanForks = clean_forks(forksToClean)
    print_forks(cleanForks)
    print( f"length of forks after cleaning = {len(cleanForks)}")

    # GAP, RESERVE, REACH EXAMPLE

    for tine in forkPaper:
        print(f"tine = {tine}")
        print(f"\tgap = {gap(tine, forkPaper, wPaper)}")
        print(f"\treserve = {reserve(tine, wPaper)}")
        print(f"\treach = {reach(tine, forkPaper, wPaper)}")
    print(f"isClosed = {isClosed(forkPaper, wPaper)}")
    print(f"maxReach(F) = {maxReach(forkPaper, wPaper)}")
    print(f"margin(F) = {margin(forkPaper, wPaper)}")