############################################################
#   MEMORY GRAPH
#-----------------------------------------------------------
############################################################

from tools.data_structures import DefaultDict, Stack, Queue
from tools.iter_tools import is_iterable

############################################################
#   MemoryGraph
############################################################


class MemoryGraph:

    DEFAULT__NODES = None
    DEFAULT__EDGES = None
    DEFAULT__INVERSE_EDGE_LABEL_PAIRS = None
    DEFAULT__USE_INVERSE_EDGE_LABEL_PAIRS = True

    def __init__(
        self,
        nodes=DEFAULT__NODES,
        edges=DEFAULT__EDGES,
        inverse_edge_label_pairs=DEFAULT__INVERSE_EDGE_LABEL_PAIRS,
        use_inverse_edge_label_pairs=DEFAULT__USE_INVERSE_EDGE_LABEL_PAIRS,
    ):

        self.map = DefaultDict(dict)
        self.inverse_edge_labels = DefaultDict(list)

        if is_iterable(edges):
            for (label_a, label_b) in inverse_edge_label_pairs:
                self.inverse_edge_labels[label_a].append(label_b)
                self.inverse_edge_labels[label_b].append(label_a)

        if is_iterable(nodes):
            for node in nodes:
                self.add_node(node)

        if is_iterable(edges):
            for (from_node, edge_label, to_node) in edges:
                if use_inverse_edge_label_pairs and edge_label in self.inverse_edge_labels:
                    self.add_both_edge(from_node, edge_label, to_node)
                else:
                    self.add_edge(from_node, edge_label, to_node)

        return

    def add_inverse_edge_label_pair(self, edge_label_a, edge_label_b):
        """
        Add the inverse edge label pair `(edge_label_a, edge_label_b)` to the graph's `inverse_edge_labels` dict.
        """

        self.inverse_edge_labels[edge_label_a].append(edge_label_b)
        self.inverse_edge_labels[edge_label_b].append(edge_label_a)

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
        Add a directed edge `(from_node, edge_label, to_node)` to the graph.
        """

        if from_node not in self.map:
            self.add_node(from_node)

        if to_node not in self.map:
            self.add_node(to_node)

        self.map[from_node][edge_label] = to_node

        return

    def add_both_edges(self, from_node, edge_label, to_node):
        """
        Add two directed edges to the graph:
        - `(from_node, edge_label, to_node)`
        - `(to_node, self.inverse_edge_labels[edge_label][0], from_node)`
        """

        edge_label_a = edge_label
        edge_label_b = self.inverse_edge_labels[edge_label_a][0]

        self.add_edge(from_node, edge_label_a, to_node)
        self.add_edge(to_node, edge_label_b, from_node)

        return

    def get_neighbors(self, node):
        """
        Get all neighbors of the node with label `node`.
        """

        return dict(self.map[node])    # We don't want users to directly edit this.

    def xft(
        self,
        from_node,
        nodes_to_visit=None,
    ):
        """
        Find each node in the graph from `from_node` in customizable order.
        """

        if nodes_to_visit is None:
            nodes_to_visit = list()

        visited_nodes = set()
        traversed_nodes = list()

        nodes_to_visit.push((None, from_node))

        while len(nodes_to_visit) > 0:

            (label, node) = nodes_to_visit.pop()

            if node not in visited_nodes:

                visited_nodes.add(node)
                traversed_nodes.append((label, node))

                for (next_label, next_node) in self.get_neighbors(node).items():
                    nodes_to_visit.push((next_label, next_node))

            else:
                pass

        return traversed_nodes

    def bft(self, from_node):
        """
        Find each node in the graph starting from `from_node`, in breadth-first order.
        """

        return self.xft(from_node, Queue())

    def dft(self, from_node):
        """
        Find each node in the graph starting from `from_node`, in depth-first order.
        """

        return self.xft(from_node, Stack())

    def xfs(
        self,
        found,
        from_node,
        paths_to_search=None,
    ):
        """
        Find a path in the graph from `from_node` until `found(...)` is True, in customizable order.
        The order is determined by how `paths_to_search` implements `*.push` and `*.pop`.
        The signature of `found` is `(curr_node, curr_path, from_node, paths_to_search, visited_nodes,) -> bool`.
        """

        if paths_to_search is None:
            paths_to_search = list()

        visited_nodes = set()
        searched_path = list()

        curr_node = from_node
        curr_path = [(None, from_node)]

        if found(
                curr_node,
                curr_path,
                from_node,
                paths_to_search,
                visited_nodes,
        ):

            searched_path = curr_path

        else:

            paths_to_search.push(curr_path)

        while len(paths_to_search) > 0 and not searched_path:

            curr_path = paths_to_search.pop()
            (curr_label, curr_node) = curr_path[-1]

            if curr_node not in visited_nodes:

                visited_nodes.add(curr_node)

                for (next_label, next_node) in self.get_neighbors(curr_node).items():

                    next_path = list(curr_path)    # copy of `curr_path`
                    next_path.append((next_label, next_node))

                    if found(
                            next_node,
                            next_path,
                            from_node,
                            paths_to_search,
                            visited_nodes,
                    ):

                        searched_path = next_path
                        break

                    paths_to_search.push(next_path)

            else:
                pass

        return searched_path

    def bfs(self, found, from_node):
        """
        Find a path in the graph from `from_node` until `found(...)` is True, in breadth-first order.
        """

        return self.xfs(found, from_node, Queue())

    def dfs(self, found, from_node):
        """
        Find a path in the graph from `from_node` until `found(...)` is True, in breadth-first order.
        """

        return self.xfs(found, from_node, Stack())

    def xfs__to_node(
        self,
        to_node,
        from_node,
        paths_to_search=None,
    ):
        """
        Find a path in the graph from `from_node` to `to_node`, in customizable order.
        The order is determined by how `paths_to_search` implements `*.push` and `*.pop`.
        """

        def found_to_node(curr_node, *rest):
            return (curr_node == to_node)

        return self.xfs(found_to_node, from_node, paths_to_search)

    def bfs__to_node(self, to_node, from_node):
        """
        Find the shortest path from `from_node` to `to_node`, in breadth-first order.
        """

        return self.xfs__to_node(to_node, from_node, Queue())

    def dfs__to_node(self, to_node, from_node):
        """
        Find a path from `from_node` to `to_node`, in depth-first order.
        """

        return self.xfs__to_node(to_node, from_node, Stack())

    def xfs__to_node_set(
        self,
        to_node_set,
        from_node,
        paths_to_search=None,
    ):
        """
        Find a path from `from_node` to a node in `to_node_set`, in customizable order.
        The order is determined by how `paths_to_search` implements `*.push` and `*.pop`.
        """

        def found_to_node_set(curr_node, *rest):
            return (curr_node in to_node_set)

        return self.xfs(found_to_node_set, from_node, paths_to_search)

    def bfs__to_node_set(self, to_node_set, from_node):
        """
        Find the shortest path from `from_node` to a node in `to_node_set`, in breadth-first order.
        """

        return self.xfs__to_node_set(to_node_set, from_node, Queue())

    def dfs__to_node_set(self, to_node_set, from_node):
        """
        Find a path from `from_node` to a node in `to_node_set`, in depth-first order.
        """

        return self.xfs__to_node_set(to_node_set, from_node, Stack())


############################################################
#   Main
############################################################

if __name__ == "__main__":

    memory_map = """
    1 ← → 2 ← → 3
    ↑           ↑
    ↓           ↓
    4     5 ← → 6
    ↑           ↑
    ↓           ↓
    7 ← → 8 ← → 9
    """

    memory_graph__inverse_edge_label_pairs = (
        ("n", "s"),
        ("e", "w"),
    )

    memory_graph__edges = set([
        (1, "e", 2),
        (2, "e", 3),
        (1, "s", 4),
        (3, "s", 6),
        (5, "e", 6),
        (4, "s", 7),
        (6, "s", 9),
        (7, "e", 8),
        (8, "e", 9),
    ])

    memory_graph__nodes = set()
    for (from_node, edge_label, to_node) in memory_graph__edges:
        memory_graph__nodes.add(from_node)
        memory_graph__nodes.add(to_node)

    memory_graph = MemoryGraph(
        inverse_edge_label_pairs=memory_graph__inverse_edge_label_pairs,
        nodes=memory_graph__nodes,
        edges=memory_graph__edges,
    )

    results__bft = memory_graph.bft(1)
    results__dft = memory_graph.dft(1)
    results__bfs__to_node = memory_graph.bfs__to_node(5, 1)
    results__dfs__to_node = memory_graph.dfs__to_node(5, 1)
    results__bfs__to_node_set = memory_graph.bfs__to_node_set({3, 6, 5, 9}, 1)
    results__dfs__to_node_set = memory_graph.dfs__to_node_set({3, 6, 5, 9}, 1)

    #-----------------------------------------------------------

    import pprint
    from tools.printers import print_heading, print_line
    line_width = 40

    def print_spaced(*args, **kwargs):
        print()
        print(*args, **kwargs)
        print()
        return

    print_heading("memory_graph : __main__", width=line_width)
    print_spaced(
        "--- pretty map ---",
        memory_map,
        "--- map ---",
        pprint.pformat(memory_graph.map),
        "--- bft ---",
        pprint.pformat(results__bft),
        "--- dft ---",
        pprint.pformat(results__dft),
        "--- bfs - to node ---",
        pprint.pformat(results__bfs__to_node),
        "--- dfs - to node ---",
        pprint.pformat(results__dfs__to_node),
        "--- bfs - to node set ---",
        pprint.pformat(results__bfs__to_node_set),
        "--- dfs - to node set ---",
        pprint.pformat(results__dfs__to_node_set),
        sep="\n\n",
    )
    print_line(liner="=", width=line_width)
    print("DONE")
