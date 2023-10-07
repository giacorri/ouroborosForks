# FORKING LIBRARY v4
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import *
import multiprocessing
import concurrent.futures

NUM_PROCESSES = multiprocessing.cpu_count()

ROOT = nx.DiGraph()
ROOT.add_node("0", weight=0, type="honest", n=0)

# PLOTTING
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
    node_colors = {'honest': 'green', 'adversarial': 'red'}
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
def convert_tine(tine):
    return [int(node.split(" ")[0]) for node in tine]

# FORK struct, composed by a tree graph and a characteristics string
class Fork:
    def __init__(self, w, tree=ROOT):
        self.tree = tree
        self.w = w

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
    
    def print(self):
        print(self.get_tines())

    
    def plot(self, quick=False):
        plot_tree(self.tree, self.w, quick)

    def copy(self):
        return Fork(self.w.copy(), self.tree.copy())

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
        node_colors1 = {'honest': 'green', 'adversarial': 'red'}
        node_colors1 = [node_colors1[fork1.tree.nodes[node]['type']] for node in fork1.tree.nodes()]
        nx.draw(fork1.tree, pos1, labels=node_labels1, with_labels=True, node_color=node_colors1, node_size=400, ax=ax1)

        pos2 = hierarchy_pos(fork2.tree, root='0')
        y_positions2 = {node: -fork2.tree.nodes[node]['weight'] for node in fork2.tree.nodes()}
        pos2 = {k: (-y_positions2[k], pos2[k][0],) for k in pos2}
        node_labels2 = {node: str(fork2.tree.nodes[node]['weight']) for node in fork2.tree.nodes()}
        node_colors2 = {'honest': 'green', 'adversarial': 'red'}
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
                    newFork.tree.add_node(str(slot+1), weight=slot+1, type="honest", n=0)
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
                    newFork.tree.add_node(str(slot+1) + " a1", weight=slot+1, type="adversarial", n=1)
                    # add edge from node to new adversarial block
                    newFork.tree.add_edge(node, str(slot+1) + " a1")
                    # add new fork to list
                    generatedInSlot.append(newFork)
                    print(f"\t\t- {newFork.get_tines()}")
            print(f"\t\tFINISHED FORK {generatedForks.index(fork)+1}/{len(generatedForks)}")
        print(f"\tFINISHED SLOT {slot+1}: generated {len(generatedInSlot)} forks")
        generatedForks = generatedInSlot
    print(f"\033[0m", end="")
    return generatedForks

# PARALLEL COMPUTING

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

def gen_forks_worker(generatedForks, start, end, slot, w, maxAdversarialBlocks=1):
    generatedInSlot = []
    # for each fork in the chunk
    for fork in generatedForks[start:end]:
        if w[slot] == 0:
            for maximalTine in fork.get_maximal_tines():
                newFork = fork.copy()
                newFork.tree.add_node(str(slot + 1), weight=slot + 1, type="honest", n=0)
                newFork.tree.add_edge(maximalTine[-1], str(slot + 1))
                generatedInSlot.append(newFork)
        else:
            generatedInSlot.append(fork.copy())
            for node in fork.tree.nodes:
                k = 1
                newFork = fork.copy()
                newFork.tree.add_node(str(slot + 1) + " a" + str(k), weight=slot + 1, type="adversarial", n=k)
                newFork.tree.add_edge(node, str(slot + 1) + " a" + str(k))
                generatedInSlot.append(newFork)
                if k < maxAdversarialBlocks:
                    k += 1
                    for otherNode in fork.tree.nodes:
                        if otherNode != node:
                            newNewFork = newFork.copy()
                            newNewFork.tree.add_node(str(slot + 1) + " a" + str(k), weight=slot + 1, type="adversarial", n=k)
                            newNewFork.tree.add_edge(otherNode, str(slot + 1) + " a" + str(k))
                            generatedInSlot.append(newNewFork)
    
    print(f"\t\tFINISHED CHUNK {start+1}-{end}: generated {len(generatedInSlot)} forks")
    return generatedInSlot

def parallel_gen_forks(w, maxAdversarialBlocks=1, num_processes=NUM_PROCESSES):
    generatedForks = []
    # initialize with tree with only root node
    generatedForks.append(Fork(w))
    # for each slot
    for slot in range(len(w)):
        # print green if honest slot, red if adversarial slot
        if w[slot] == 0:
            print(f"\033[92m", end="")
        else:
            print(f"\033[91m", end="")

        print(f"slot {slot+1}: starting with {len(generatedForks)} forks")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_processes) as executor:
            futures = []
            chunkSize = len(generatedForks) // NUM_PROCESSES
            # for each process
            for i in range(NUM_PROCESSES):
                start = i * chunkSize
                end = start + chunkSize
                # if last process
                if i == NUM_PROCESSES - 1:
                    end = len(generatedForks)
                if end > 0:
                    print(f"\t\tSTARTING CHUNK {start+1}-{end}")
                    futures.append(executor.submit(gen_forks_worker, generatedForks, start, end, slot, w, maxAdversarialBlocks))
            generatedInSlot = []
            for future in concurrent.futures.as_completed(futures):
                generatedInSlot += future.result()
        nGenerated = len(generatedInSlot)
        if w[slot] == 0 or maxAdversarialBlocks == 1:
            print(f"\tFINISHED GENERATION: {nGenerated} forks")
        else:
            print(f"\tFINISHED GENERATION: {nGenerated} forks to clean")
            parallel_clean_forks(generatedInSlot)
            print(f"\tFINISHED SLOT {slot+1}: removed {nGenerated - len(generatedInSlot)} duplicates")
        generatedForks = generatedInSlot

    print(f"\033[0m", end="")
    return generatedForks

