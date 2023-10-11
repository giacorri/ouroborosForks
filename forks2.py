# FORKING LIBRARY v5.0
import networkx as nx
from networkx.drawing.nx_pydot import *
import matplotlib.pyplot as plt
import multiprocessing
import concurrent.futures

NUM_PROCESSES = multiprocessing.cpu_count()

# tree graph with only root node
ROOT = nx.DiGraph()
ROOT.add_node("0", weight=0, type="h")

# Directed rooted tree layout
def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
    
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos
            
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

# plot a directed rooted tree as a fork with labels and colors
def plot_tree(tree, w, quick=False):
    fig, ax = plt.subplots()
    pos = hierarchy_pos(tree, root='0')
    # get y positions from weights
    y_positions = {node: -tree.nodes[node]['weight'] for node in tree.nodes()}
    # grow towards east
    pos = {k: (-y_positions[k], pos[k][0],) for k in pos}
    # label nodes with their weight
    node_labels = {node: str(tree.nodes[node]['weight']) for node in tree.nodes()}

    # color nodes according to type
    node_colors = {'h': 'green', 'a': 'red'}
    node_colors = [node_colors[tree.nodes[node]['type']] for node in tree.nodes()]

    # draw graph
    nx.draw(tree, pos, labels=node_labels, with_labels=True, node_color=node_colors, node_size=400, ax=ax)

    # display vertical lines dividing slots
    for y in range(0, len(w) + 1):
        plt.axvline(x=y+0.5, color='gray', linestyle='--', lw=1)
    # display x axis 
    ax.tick_params(bottom=True, labelbottom=True)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    # name x axis
    ax.set_xlabel("slot")

    ax2 = ax.twiny()
    # put w on the upper x axis
    ax2.tick_params(bottom=False, labelbottom=False)
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks([x for x in range(0, len(w)+1)])
    # insert 0 at the beginning of w
    w = w.copy()
    w.insert(0, 0)
    # set w as labels
    ax2.set_xticklabels(w)
    ax2.set_xlabel("w")

    ax.set_axis_on()
    # plot
    if quick:
        plt.show(block=False)
        plt.pause(0.4)
        plt.close()
    else:
        plt.show()

# TINE, a list of nodes in a path of the graph
def truncate_tine(tine, k):
    if len(tine) < k:
        return []
    return tine[:len(tine)-k]

# check if tine1 is a prefix of tine2
def is_prefix(tine1, tine2):
    if len(tine1) > len(tine2):
        return False
    for i in range(len(tine1)):
        if tine1[i] != tine2[i]:
            return False
    return True

# get number of the slot in which the node was published
def get_label(node):
    return int(node.split("a")[0])

def is_honest(node):
    if len(node.split("a")) == 1:
        return True
    return False

# compute tine length (number of edges)
def length_tine(tine):
    return len(tine)-1

# share edge relation
def tilde_rel(tine1, tine2):
    if tine1 == '0' or tine2 == '0':
        return False
    # if they share an edge, they should share also the first edge
    if tine1[:1] == tine2[:1]:
        return True
    return False

# common prefix of two tines
def common_prefix(tine1, tine2):
        commonPrefix = []
        for i in range(min(len(tine1), len(tine2))):
            if tine1[i] == tine2[i]:
                commonPrefix.append(tine1[i])
            else:
                break
        return commonPrefix

# FORK struct, composed by a tree graph and a characteristic string
class Fork:
    def __init__(self, w=[], tree=ROOT):
        self.w = w.copy()
        self.tree = tree.copy()

    def get_w(self):
        return self.w

    def get_leaves(self):
        leaves = []
        for node in self.tree.nodes:
            if self.tree.out_degree(node) == 0:
                leaves.append(node)
        return leaves
    
    def get_tines(self):
        tines = []
        for leaf in self.get_leaves():
            if leaf == '0':
                tines.append(['0'])
            else:
                path = list(nx.all_simple_paths(self.tree, '0', leaf))[0]
                tines.append(path)
        return tines
    
    def get_maximal_tines(self):
        maximal_tines = []
        max = 0
        tines = self.get_tines()
        for tine in tines:
            if len(tine) > max:
                max = len(tine)
                maximal_tines = [tine]
            elif len(tine) == max:
                maximal_tines.append(tine)
        return maximal_tines
    
    def depth(self, node):
        return nx.shortest_path_length(self.tree, '0', node)

    def is_viable(self, nTine):
        tine = self.get_tines()[nTine]
        lastNode = tine[-1]
        label = lastNode.split("a")[0]
        if label == '0':
            return True
        else:
            honestPriorSlots = [i+1 for i in range(int(label)) if self.w[i] == 0]
            honestPiorNodes = [node for node in self.tree.nodes if self.tree.nodes[node]['weight'] in honestPriorSlots and self.tree.nodes[node]['type'] == 'h']
            for h in honestPiorNodes:
                if self.depth(h) > self.depth(lastNode):
                    return False
            return True

    def is_closed(self):
        leaves = self.get_leaves()
        for leaf in leaves:
            type = self.tree.nodes[leaf]['type']
            if type == 'a':
                return False
        return True

    def get_viableTinesIndexes(self):
        viableTinesIndexes = []
        tines = self.get_tines()
        for nTine in range(len(tines)):
            if self.is_viable(nTine):
                viableTinesIndexes.append(nTine)
        return viableTinesIndexes

    def print(self):
        print(self.get_tines())
    
    def plot(self, quick=False):
        plot_tree(self.tree, self.w, quick)

    def copy(self):
        return Fork(self.w.copy(), self.tree.copy())
    
    def get_height(self):
        return nx.dag_longest_path_length(self.tree)

    def is_flat(self):
        tines = self.get_tines()
        for i in range(len(tines)):
            for j in range(i+1, len(tines)):
                if not tilde_rel(tines[i], tines[j]):
                    if length_tine(tines[i]) == length_tine(tines[j]) and length_tine(tines[i]) == self.get_height():
                        return True, [i, j]
        return False, []
    
    def gap(self, tine):
        if not self.is_closed():
            return "Error: fork is not closed"
        maxTine = self.get_maximal_tines()[0]
        return length_tine(maxTine) - length_tine(tine)
    
    def reserve(self, tine):
        if not self.is_closed():
            return "Error: fork is not closed"
        label = get_label(tine[-1])
        total = 0
        for i in range(label, len(self.w)):
            if self.w[i] == 1:
                total += 1
        return total

    def reach(self, tine):
        if not self.is_closed():
            return "Error: fork is not closed"
        return self.reserve(tine) - self.gap(tine)
    
    def rho(self):
        max = 0
        for tine in self.get_tines():
            if self.reach(tine) > max:
                max = self.reach(tine)
        return max
    
    def get_edge_disjoint_tines(self):
        tines = self.get_tines()
        edge_disjoint_tines = []
        for i in range(len(tines)):
            for j in range(i+1, len(tines)):
                if not tilde_rel(tines[i], tines[j]):
                    edge_disjoint_tines.append([tines[i], tines[j]])
        return edge_disjoint_tines

    def mu(self):
        max = 0
        for edgeDisjointTines in self.get_edge_disjoint_tines():
            for tines in edgeDisjointTines:
                tine1 = tines[0]
                tine2 = tines[1]
                reach1 = self.reach(tine1)
                reach2 = self.reach(tine2)
                if reach1 < reach2:
                    if reach1 > max:
                        max = reach1
                else:
                    if reach2 > max:
                        max = reach2
        return max

    # tine1/tine2
    def tines_frac(self, nTine1, nTine2):
        if not self.is_viable(nTine1) or not self.is_viable(nTine2):
            return "Error: tines are not viable"
        tines = self.get_tines()
        tine1 = tines[nTine1]
        tine2 = tines[nTine2]
        commonPrefix = common_prefix(tine1, tine2)
        return length_tine(tine1) - length_tine(commonPrefix)

    def tines_div(self, nTine1, nTine2):
        tines = self.get_tines()
        tine1 = tines[nTine1]
        tine2 = tines[nTine2]
        label1 = get_label(tine1[-1])
        label2 = get_label(tine2[-1])
        if label1 < label2:
            return self.tines_frac(nTine1, nTine2)
        elif label1 > label2:
            return self.tines_frac(nTine2, nTine1)
        else:
            frac1 = self.tines_frac(nTine1, nTine2)
            frac2 = self.tines_frac(nTine2, nTine1)
            if frac1 >= frac2:
                return frac1
            else:
                return frac2
            
    def fork_div(self):
        max = 0
        viableTinesIndexes = self.get_viableTinesIndexes()
        for i in range(len(viableTinesIndexes)):
            for j in range(i+1, len(viableTinesIndexes)):
                div = self.tines_div(viableTinesIndexes[i], viableTinesIndexes[j])
                if div > max:
                    max = div
        return max
    
    
# converts a list of tines into a Fork
def convert_tines_to_fork(tines):
    tree = ROOT.copy()
    wDict = {}
    maxSlot = 0
    for tine in tines:
        for i in range(1, len(tine)):
            node = tine[i]
            if node not in tree.nodes:
                print(f"node {node} not in tree")
                splittedNodeName = node.split("a")
                weight = int(splittedNodeName[0])
                print(f"weight {weight}")
                if weight > maxSlot:
                    maxSlot = weight
                if len(splittedNodeName) == 1:
                    type = "h"
                    print(f"type {type}")
                    wDict[weight] = 0
                    n = 0
                else:
                    type = "a"
                    print(f"type {type}")
                    wDict[weight] = 1
                    # n = int(splittedNodeName[1][1:])
                    n = int(splittedNodeName[1])
                    print(f"n {n}")    
                tree.add_node(node, weight=weight, type=type)
            # if the edge is not already in the tree
            if not tree.has_edge(tine[i-1], tine[i]):
                tree.add_edge(tine[i-1], tine[i])
    w = [1] * (maxSlot)
    for i in wDict:
        w[i-1] = wDict[i]
    print(f"w {w}")
    return Fork(w, tree)

# PLOTTING MULTIPLE FORKS
def plot_forks(forks, quick=False):
    nForks = len(forks)
    for n in range(nForks):
        print(f"fork {n+1}")
        forks[n].print()
        forks[n].plot(quick)

def plot_couple_of_forks(forksCouples, quick=False):
    for couple in forksCouples:
        fork1 = couple[0]
        fork2 = couple[1]
        # make two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2)

        pos1 = hierarchy_pos(fork1.tree, root='0')
        y_positions1 = {node: -fork1.tree.nodes[node]['weight'] for node in fork1.tree.nodes()}
        pos1 = {k: (-y_positions1[k], pos1[k][0],) for k in pos1}
        node_labels1 = {node: str(fork1.tree.nodes[node]['weight']) for node in fork1.tree.nodes()}
        node_colors1 = {'honest': 'green', 'a': 'red'}
        node_colors1 = [node_colors1[fork1.tree.nodes[node]['type']] for node in fork1.tree.nodes()]
        nx.draw(fork1.tree, pos1, labels=node_labels1, with_labels=True, node_color=node_colors1, node_size=400, ax=ax1)

        pos2 = hierarchy_pos(fork2.tree, root='0')
        y_positions2 = {node: -fork2.tree.nodes[node]['weight'] for node in fork2.tree.nodes()}
        pos2 = {k: (-y_positions2[k], pos2[k][0],) for k in pos2}
        node_labels2 = {node: str(fork2.tree.nodes[node]['weight']) for node in fork2.tree.nodes()}
        node_colors2 = {'honest': 'green', 'a': 'red'}
        node_colors2 = [node_colors2[fork2.tree.nodes[node]['type']] for node in fork2.tree.nodes()]
        nx.draw(fork2.tree, pos2, labels=node_labels2, with_labels=True, node_color=node_colors2, node_size=400, ax=ax2)

        for y in range(0, len(fork1.w) + 1):
            ax1.axvline(x=y+0.5, color='gray', linestyle='--', lw=1)
            ax2.axvline(x=y+0.5, color='gray', linestyle='--', lw=1)

        ax1.tick_params(bottom=True, labelbottom=True)
        ax1.xaxis.set_major_locator(plt.MultipleLocator(1))
        ax1.set_xlabel("slot")
        ax1.set_title("fork 1")
        ax2.tick_params(bottom=True, labelbottom=True)
        ax2.xaxis.set_major_locator(plt.MultipleLocator(1))
        ax2.set_xlabel("slot")
        ax2.set_title("fork 2")

        if quick:
            plt.show(block=False)
            plt.pause(0.2)
            plt.close()
        else:
            plt.show()

# FORKS GENERATION
def gen_forks(w):
    generatedForks = []
    # initialize with tree with only root node
    generatedForks.append(Fork(w))
    # for each slot
    for slot in range(len(w)):
        if w[slot] == 0:
            print(f"\033[92m", end="")
        else:
            print(f"\033[91m", end="")

        print(f"slot {slot+1}: starting with {len(generatedForks)} forks")
        generatedInSlot = []
        # for each fork in the list
        for fork in generatedForks:
            print(f"\t- {generatedForks.index(fork)+1}/{len(generatedForks)}: {fork.get_tines()}")
            # if honest slot
            if w[slot] == 0:
                for maximalTine in fork.get_maximal_tines():
                    newFork = fork.copy()
                    # add new honest node
                    newFork.tree.add_node(str(slot+1), weight=slot+1, type="h")
                    # add edge from last node of maximal tine to new node
                    newFork.tree.add_edge(maximalTine[-1], str(slot+1))
                    # add new fork to list
                    generatedInSlot.append(newFork)
                    print(f"\t\t- {newFork.get_tines()}")
            # if adversarial slot
            else:
                # save fork where the adversary does not publish a block
                generatedInSlot.append(fork.copy())
                for node in fork.tree.nodes:
                    # save fork where the adversary publishes a block after node
                    newFork = fork.copy()
                    # add new adversarial block to node
                    newFork.tree.add_node(str(slot+1) + "_1", weight=slot+1, type="a")
                    # add edge from node to new adversarial block
                    newFork.tree.add_edge(node, str(slot+1) + "_1")
                    # add new fork to list
                    generatedInSlot.append(newFork)
                    print(f"\t\t- {newFork.get_tines()}")
            print(f"\t\tFINISHED FORK {generatedForks.index(fork)+1}/{len(generatedForks)}")
        print(f"\tFINISHED SLOT {slot+1}: generated {len(generatedInSlot)} forks")
        generatedForks = generatedInSlot
    print(f"\033[0m", end="")
    return generatedForks

# PARALLEL FORKS CLEANING
def clean_forks_worker(data, lock, pairs_to_check, result_queue):
    toRemove = []
    for pair in pairs_to_check:
        i, j = pair
        if nx.is_isomorphic(data[i].tree, data[j].tree, node_match=lambda x, y: x['type'] == y['type'] and x['weight'] == y['weight']):
            toRemove.append(j)
    print(f"\t\tFINISHED CHUNK of {len(pairs_to_check)} pairs: found {len(toRemove)} isomorphic forks")
    with lock:
        result_queue.extend(toRemove)

def parallel_clean_forks(forks, num_processes=NUM_PROCESSES):
    num_forks = len(forks)

    # Generate pairs of indexes to check
    pairs_to_check = [(i, j) for i in range(num_forks) for j in range(i + 1, num_forks)]

    # Calculate the number of pairs each process will handle
    pairs_per_process = len(pairs_to_check) // num_processes

    manager = multiprocessing.Manager()
    result_queue = manager.list()
    lock = multiprocessing.Lock()

    processes = []

    # Divide the work among processes based on pairs to check
    for i in range(num_processes):
        start = i * pairs_per_process
        end = (i + 1) * pairs_per_process if i < num_processes - 1 else len(pairs_to_check)

        process = multiprocessing.Process(target=clean_forks_worker, args=(forks, lock, pairs_to_check[start:end], result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    toRemove = []

    while len(result_queue) > 0:
        toRemove.append(result_queue.pop())

    # Sort and reverse toRemove
    toRemove.sort()
    toRemove.reverse()

    # Remove isomorphic forks
    for j in toRemove:
        forks.pop(j)



# PARALLEL FORKS GENERATION
def worker_gen_forks(maxAdversarialBlocks, wSl, slot, generatedForks, start, end, generatedInSlot):
    for forkIndex in range(start, end):
        fork = generatedForks[forkIndex]
        if wSl == 0:
            for maximalTine in fork.get_maximal_tines():
                newFork = fork.copy()
                newFork.tree.add_node(str(slot + 1), weight=slot + 1, type="h")
                newFork.tree.add_edge(maximalTine[-1], str(slot + 1))
                generatedInSlot.append(newFork)
        else:
            generatedInSlot.append(fork.copy())
            for node in fork.tree.nodes:
                newFork = fork.copy()
                newFork.tree.add_node(str(slot + 1) + "_1", weight=slot + 1, type="a")
                newFork.tree.add_edge(node, str(slot + 1) + "_1")
                generatedInSlot.append(newFork)
                if maxAdversarialBlocks == 2:
                    newFork = newFork.copy()
                    newFork.tree.add_node(str(slot + 1) + "_2", weight=slot + 1, type="a")
                    newFork.tree.add_edge(node, str(slot + 1) + "_2")
                    generatedInSlot.append(newFork)

def parallel_gen_forks(w, maxAdversarialBlocks=1, num_processes=NUM_PROCESSES):

    generatedForks = multiprocessing.Manager().list()
    generatedForks.append(Fork())

    for sl in range(len(w)):
        generatedInSlot = multiprocessing.Manager().list()
        processes = []
        for i in range(num_processes):
            start = i * len(generatedForks) // num_processes
            end = (i + 1) * len(generatedForks) // num_processes if i < num_processes - 1 else len(generatedForks)
            
            process = multiprocessing.Process(target=worker_gen_forks, args=(maxAdversarialBlocks, w[sl], sl, generatedForks, start, end, generatedInSlot))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        generatedForks = generatedInSlot

    return generatedForks


# CHARACTERISTIC STRING PROPERTIES
def k_cp(k, w, forks=None, parallel=True):
    if forks == None:
        if parallel:
            forks = parallel_gen_forks(w)
        else:
            forks = gen_forks(w)
    for fork in forks:
        # print(f"fork: {fork.get_tines()}")
        viableTinesIndexes = fork.get_viableTinesIndexes()
        # print(f"\tviable tines indexes: {viableTinesIndexes}")
        if len(viableTinesIndexes) > 1:
            # print(f"\t\tpossible pairs of viable tines: { ((len(viableTinesIndexes) * (len(viableTinesIndexes) - 1)) / 2):.0f}") 
            tines = fork.get_tines()
            for i in range(len(viableTinesIndexes)):
                if i == len(viableTinesIndexes) - 1:
                    break
                index1 = viableTinesIndexes[i]
                tine1 = tines[index1]
                
                for j in range(i+1, len(viableTinesIndexes)):
                    index2 = viableTinesIndexes[j]
                    tine2 = tines[index2]
                    l1 = int(tine1[-1].split("a")[0])
                    l2 = int(tine2[-1].split("a")[0])
                    t1 = tine1.copy()
                    t2 = tine2.copy()
                    if l1 > l2:
                        t1, t2 = t2, t1

                    if not is_prefix(truncate_tine(t1, k), t2):
                        counterExample = [fork, t1, t2]
                        return False, counterExample
    return True, None

def tau_s_hcg(tau, s, w, forks=None, parallel=True):
    if forks == None:
        if parallel:
            forks = parallel_gen_forks(w)
        else:
            forks = gen_forks(w)
    for fork in forks:
        viableTinesIndexes = fork.get_viableTinesIndexes()
        tines = fork.get_tines()
        for i in range(len(viableTinesIndexes)):
            tine = tines[viableTinesIndexes[i]]
            label = int(get_label(tine[-1]))
            # honest vertices on tine at least s slots before the tine label
            H = [h for h in tine if int(get_label(h)) + s <= label and fork.tree.nodes[h]['type'] == 'honest']
            
            # the path in tine from label(v)+1 to label(t) contains at least tau*s  nodes
            for h in H:
                path = tine[tine.index(h)+1:]
                if len(path) < tau*s:
                    return False, [fork, tine, h, path]
    return True, None

def s_ecq(s, w, forks=None, parallel=True):
    if forks == None:
        if parallel:
            forks = parallel_gen_forks(w)
        else:
            forks = gen_forks(w)

    for fork in forks:
        viableTinesIndexes = fork.get_viableTinesIndexes()
        tines = fork.get_tines()
        for i in range(len(viableTinesIndexes)):
            tine = tines[viableTinesIndexes[i]]
            label = int(get_label(tine[-1]))
            # every portion of tine spanning s slots contains at least one honest node
            for j in range(label-s):
                slots = list(range(j, j+s))

                path = []
                for node in tine:
                    if int(get_label(node)) in slots:
                        path.append(node)

                containsHonest = False
                for node in path:
                    if fork.tree.nodes[node]['type'] == 'honest':
                        containsHonest = True
                        break
                if not containsHonest:
                    return False, [fork, tine, slots, path]
    return True, None

def forkable(w, forks=None, parallel=True):
    if forks == None:
        if parallel:
            forks = parallel_gen_forks(w)
        else:
            forks = gen_forks(w)
    for fork in forks:
        isFlat, indexes = fork.is_flat()
        if isFlat:
            return True, [fork, indexes]
    return False, None

def rho(w, forks=None, parallel=True):
    if forks == None:
        if parallel:
            forks = parallel_gen_forks(w)
        else:
            forks = gen_forks(w)
    max = 0
    for fork in forks:
        if fork.rho() > max:
            max = fork.rho()
    return max

def mu(w, forks=None, parallel=True):
    if forks == None:
        if parallel:
            forks = parallel_gen_forks(w)
        else:
            forks = gen_forks(w)
    max = 0
    for fork in forks:
        if fork.mu() > max:
            max = fork.mu()
    return max

def m(w, forks=None, parallel=True):
    return (rho(w, forks, parallel), mu(w, forks, parallel))

def div(w, forks=None, parallel=True):
    if forks == None:
        if parallel:
            forks = parallel_gen_forks(w)
        else:
            forks = gen_forks(w)
    closedForks = [fork for fork in forks if fork.is_closed()]
    max = 0
    for fork in closedForks:
        div = fork.fork_div()
        if div > max:
            max = div
    return max