import dsc40graph

def slc(graph, d, k):
    '''
    Performs single linkage clustering using Kruskal's algorithm.
    '''
    if hasattr(graph, 'nodes'):
        nodes_attr = graph.nodes
        nodes = list(nodes_attr() if callable(nodes_attr) else nodes_attr)
    elif hasattr(graph, 'get_nodes'):
        nodes = list(graph.get_nodes())
    else:
        nodes = list(graph._adj.keys())  

    if hasattr(graph, 'edges'):
        edges_attr = graph.edges
        edges = list(edges_attr() if callable(edges_attr) else edges_attr)
    elif hasattr(graph, 'get_edges'):
        edges = list(graph.get_edges())
    else:
        edges = list(graph._edges)  

    
    weighted_edges = [(d(e), e) for e in edges]
    weighted_edges.sort(key=lambda x: x[0])  

    dsf = DisjointSetForest(nodes)
    num_sets = len(nodes)

    for _, edge in weighted_edges:
        if num_sets <= k:
            break

        u, v = list(edge)
        if not dsf.in_same_set(u, v):
            dsf.union(u, v)
            num_sets -= 1

    rep_to_cluster = {}
    for node in nodes:
        rep = dsf.find_set(node)
        if rep not in rep_to_cluster:
            rep_to_cluster[rep] = set()
        rep_to_cluster[rep].add(node)

    return frozenset(frozenset(cluster) for cluster in rep_to_cluster.values())


class DisjointSetForest:

    def __init__(self, elements):
        self._core = _DisjointSetForestCore()

        self.element_to_id = {}
        self.id_to_element = {}

        for element in elements:
            eid = self._core.make_set()
            self.element_to_id[element] = eid
            self.id_to_element[eid] = element

    def find_set(self, element):
        
        return self.id_to_element[
                self._core.find_set(
                    self.element_to_id[element]
                )
            ]

    def union(self, x, y):
        
        x_id = self.element_to_id[x]
        y_id = self.element_to_id[y]
        self._core.union(x_id, y_id)


    def in_same_set(self, x, y):
        """Determines if elements x and y are in the same set.
        Example
        -------
        >>> dsf = DisjointSetForest(['a', 'b', 'c'])
        >>> dsf.in_same_set('a', 'b')
        False
        >>> dsf.union('a', 'b')
        >>> dsf.in_same_set('a', 'b')
        True
        """
        return self.find_set(x) == self.find_set(y)


class _DisjointSetForestCore:

    def __init__(self):
        self._parent = []
        self._rank = []
        self._size_of_set = []

    def make_set(self):
        # get the new element's "id"
        x = len(self._parent)
        self._parent.append(None)
        self._rank.append(0)
        self._size_of_set.append(1)
        return x

    def find_set(self, x):
        try:
            parent = self._parent[x]
        except IndexError:
            raise ValueError(f'{x} is not in the collection.')

        if self._parent[x] is None:
            return x
        else:
            root = self.find_set(self._parent[x])
            self._parent[x] = root
            return root

    def union(self, x, y):
        x_rep = self.find_set(x)
        y_rep = self.find_set(y)

        if x_rep == y_rep:
            return

        if self._rank[x_rep] > self._rank[y_rep]:
            self._parent[y_rep] = x_rep
            self._size_of_set[x_rep] += self._size_of_set[y_rep]
        else:
            self._parent[x_rep] = y_rep
            self._size_of_set[y_rep] += self._size_of_set[x_rep]
            if self._rank[x_rep] == self._rank[y_rep]:
                self._rank[y_rep] += 1
