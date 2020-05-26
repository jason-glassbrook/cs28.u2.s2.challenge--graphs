############################################################
#   WORLD GRAPH
#-----------------------------------------------------------
############################################################

from tools.data_structures import DefaultDict, Stack, Queue
from tools.iter_tools import is_iterable

############################################################
#   WorldGraph
############################################################


class WorldGraph:

    def __init__(self, nodes=None, edges=None):

        self.map = DefaultDict(dict)

        if is_iterable(nodes):
            for node in nodes:
                self.add_node(node)

        if is_iterable(edges):
            for (from_node, edge_label, to_node) in edges:
                self.add_edge(from_node, edge_label, to_node)

        return

    def add_node(self, node):
        """
        Add a node with label `node` to the graph.
        """

        # Simply add the node in map with no neighbors.
        # If it already exists, there is no change.
        self.map[node]

        return

    def add_edge(self, from_node, edge_label, to_node):
        """
        Add a directed edge `(from_node, to_node)` to the graph.
        """

        self.map[from_node][edge_label] = to_node

        return

    def get_neighbors(self, node):
        """
        Get all neighbors of the node with label `node`.
        """

        return dict(self.map[node])    # We don't want users to directly edit this.

    def xft(self, nodes_to_visit, from_node):
        """
        Find each node in the graph from `from_node` in customizable order.
        """

        visited_nodes = set()
        traversed_nodes = list()

        nodes_to_visit.push((None, from_node))

        while len(nodes_to_visit) > 0:

            (label, node) = nodes_to_visit.pop()

            if node not in visited_nodes:

                visited_nodes.add(node)
                traversed_nodes.append((label, node))

                for (neighbor_label, neighbor_node) in self.get_neighbors(node).items():
                    nodes_to_visit.push((neighbor_label, neighbor_node))

            else:
                pass

        return traversed_nodes

    def bft(self, from_node):
        """
        Print each node in breadth-first order beginning from `from_node`.
        """

        return self.xft(Queue(), from_node)

    def dft(self, from_node):
        """
        Print each node in depth-first order beginning from `from_node`.
        """

        return self.xft(Stack(), from_node)

    def xfs(self, paths_to_visit, from_node, to_node):
        """
        Find a path in the graph from `from_node` to `to_node` in customizable order.
        """

        visited_nodes = set()
        searched_path = None

        if from_node == to_node:

            searched_path = [(None, to_node)]

        else:

            paths_to_visit.push([(None, from_node)])

        while len(paths_to_visit) > 0 and searched_path is None:

            path = paths_to_visit.pop()
            (label, node) = path[-1]

            if node not in visited_nodes:

                visited_nodes.add(node)

                for (neighbor_label, neighbor_node) in self.get_neighbors(node).items():

                    neighbor_path = list(path)
                    neighbor_path.append((neighbor_label, neighbor_node))

                    if neighbor_node == to_node:

                        searched_path = neighbor_path
                        break

                    paths_to_visit.push(neighbor_path)

            else:
                pass

        return searched_path

    def bfs(self, from_node, to_node):
        """
        Return a list containing the shortest path from `from_node` to `to_node` in breath-first order.
        """

        return self.xfs(Queue(), from_node, to_node)

    def dfs(self, from_node, to_node):
        """
        Return a list containing a path from `from_node` to `to_node` in depth-first order.
        """

        return self.xfs(Stack(), from_node, to_node)


############################################################
#   Main
############################################################

if __name__ == "__main__":

    world_map = """
    1 ← → 2 ← → 3
    ↑           ↑
    ↓           ↓
    4     5 ← → 6
    ↑           ↑
    ↓           ↓
    7 ← → 8 ← → 9
    """

    world_edges = set([
        (1, "e", 2),
        (2, "w", 1),
        (2, "e", 3),
        (3, "w", 2),
        (1, "s", 4),
        (4, "n", 1),
        (3, "s", 6),
        (6, "n", 3),
        (5, "e", 6),
        (6, "w", 5),
        (4, "s", 7),
        (7, "n", 4),
        (6, "s", 9),
        (9, "n", 6),
        (7, "e", 8),
        (8, "w", 7),
        (8, "e", 9),
        (9, "w", 8),
    ])

    world_nodes = set()
    for (from_node, edge_label, to_node) in world_edges:
        world_nodes.add(from_node)
        world_nodes.add(to_node)

    world_graph = WorldGraph(
        nodes=world_nodes,
        edges=world_edges,
    )

    bft_results = world_graph.bft(1)
    dft_results = world_graph.dft(1)
    bfs_results = world_graph.bfs(1, 5)
    dfs_results = world_graph.dfs(1, 5)

    #-----------------------------------------------------------

    import pprint
    from tools.printers import print_heading, print_line
    line_width = 40

    def print_spaced(*args, **kwargs):
        print()
        print(*args, **kwargs)
        print()
        return

    print_heading("world_graph : __main__", width=line_width)
    print_spaced(
        "--- pretty map ---",
        world_map,
        "--- map ---",
        pprint.pformat(world_graph.map),
        "--- bft ---",
        pprint.pformat(bft_results),
        "--- dft ---",
        pprint.pformat(dft_results),
        "--- bfs ---",
        pprint.pformat(bfs_results),
        "--- dfs ---",
        pprint.pformat(dfs_results),
        sep="\n\n",
    )
    print_line(liner="=", width=line_width)
    print("DONE")
