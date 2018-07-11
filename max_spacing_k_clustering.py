'''
Here we have a greedy clustering algorithm for computing a max-spacing k-clustering. The
accompanying file describes a distance function (equivalently, a complete graph with edge costs).
It has the following format:

[number_of_nodes]
[edge 1 node 1] [edge 1 node 2] [edge 1 cost]
[edge 2 node 1] [edge 2 node 2] [edge 2 cost]
...

There is one edge (i,j) for each choice of 1 <= i < j <= n, where n is the number of nodes.

For example, the third line of the file is "1 3 5250", indicating that the distance between nodes
1 and 3 (equivalently, the cost of the edge (1,3)) is 5250. We can assume that distances are
positive but should NOT assume that they are distinct.

We'll run the clustering algorithm on this data set, where the target number k of clusters is set
to 4. What is the maximum spacing of a 4-clustering?
'''
import time


# Vertex class for undirected graphs
class Vertex():
    def __init__(self, key):
        self._key = key
        self._nbrs = {}

    def __str__(self):
        return '{' + "'key': {}, 'nbrs': {}".format(
            self._key,
            self._nbrs
        ) + '}'

    def add_nbr(self, nbr_key, weight=1):
        if (nbr_key):
            self._nbrs[nbr_key] = weight

    def has_nbr(self, nbr_key):
        return nbr_key in self._nbrs

    def get_nbr_keys(self):
        return list(self._nbrs.keys())

    def remove_nbr(self, nbr_key):
        if nbr_key in self._nbrs:
            del self._nbrs[nbr_key]

    def get_e(self, nbr_key):
        if nbr_key in self._nbrs:
            return self._nbrs[nbr_key]


# Undirected graph class
class Graph():
    def __init__(self):
        self._vertices = {}

    # 'x in graph' will use this containment logic
    def __contains__(self, key):
        return key in self._vertices

    # 'for x in graph' will use this iter() definition, where x is a vertex in an array
    def __iter__(self):
        return iter(self._vertices.values())

    def __str__(self):
        output = '\n{\n'
        vertices = self._vertices.values()
        for v in vertices:
            graph_key = "{}".format(v._key)
            v_str = "\n   'key': {}, \n   'nbrs': {}".format(
                v._key,
                v._nbrs
            )
            output += ' ' + graph_key + ': {' + v_str + '\n },\n'
        return output + '}'

    def add_v(self, v):
        if v:
            self._vertices[v._key] = v
        return self

    def get_v(self, key):
        try:
            return self._vertices[key]
        except KeyError:
            return None

    def get_v_keys(self):
        return list(self._vertices.keys())

    # removes vertex as neighbor from all its neighbors, then deletes vertex
    def remove_v(self, key):
        if key in self._vertices:
            nbr_keys = self._vertices[key].get_nbr_keys()
            for nbr_key in nbr_keys:
                self.remove_e(nbr_key, key)
            del self._vertices[key]

    def add_e(self, from_key, to_key, weight=1):
        if from_key not in self._vertices:
            self.add_v(Vertex(from_key))
        if to_key not in self._vertices:
            self.add_v(Vertex(to_key))

        self._vertices[from_key].add_nbr(to_key, weight)
        self._vertices[to_key].add_nbr(from_key, weight)

    def get_e(self, from_key, to_key):
        if from_key and to_key in self._vertices:
            return self.get_v(from_key).get_e(to_key)

    # adds the weight for an edge if it exists already, with a default of 1
    def increase_e(self, from_key, to_key, weight=1):
        if from_key not in self._vertices:
            self.add_v(Vertex(from_key))
        if to_key not in self._vertices:
            self.add_v(Vertex(to_key))

        weight_u_v = self.get_v(from_key).get_e(to_key)
        new_weight_u_v = weight_u_v + weight if weight_u_v else weight

        weight_v_u = self.get_v(to_key).get_e(from_key)
        new_weight_v_u = weight_v_u + weight if weight_v_u else weight

        self._vertices[from_key].add_nbr(to_key, new_weight_u_v)
        self._vertices[to_key].add_nbr(from_key, new_weight_v_u)

    def has_e(self, from_key, to_key):
        if from_key in self._vertices:
            return self._vertices[from_key].has_nbr(to_key)

    def remove_e(self, from_key, to_key):
        if from_key in self._vertices:
            self._vertices[from_key].remove_nbr(to_key)
        if to_key in self._vertices:
            self._vertices[to_key].remove_nbr(from_key)

    def for_each_v(self, cb):
        for v in self._vertices:
            cb(v)


# Heap class
# input: order is 0 for max heap, 1 for min heap
class Heap():
    def __init__(self, order=1):
        self._heap = []
        self._min_heap = order

    def __str__(self):
        output = '['
        size = len(self._heap)
        for i, v in enumerate(self._heap):
            txt = ', ' if i is not size - 1 else ''
            output += str(v) + txt
        return output + ']'

    # input: parent and child nodes
    def _is_balanced(self, p, c):
        is_min_heap = p <= c
        return is_min_heap if self._min_heap else not is_min_heap

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    # input: parent and child indices
    def _sift_up(self, p_i, c_i):
        if p_i == -1:
            return 0
        p = self._heap[p_i]
        c = self._heap[c_i]

        while (not self._is_balanced(p, c)):
            p_i = (c_i - 1) // 2
            self._swap(c_i, p_i)
            c_i = p_i
            if c_i is 0:
                break
            p = self._heap[(c_i - 1) // 2]

    # input: parent and child indices
    def _sift_down(self, p_i, c_i):
        while (c_i and not self._is_balanced(self._heap[p_i], self._heap[c_i])):
            self._swap(p_i, c_i)
            p_i = c_i
            c_i = self._get_swapped_child_index(p_i)

    def get_root(self):
        try:
            return self._heap[0]
        except KeyError:
            return None

    def get_node(self, key):
        try:
            return self._heap[key]
        except KeyError:
            return None

    def get_nodes(self):
        return self._heap

    def insert(self, node):
        self._heap.append(node)
        node_i = len(self._heap) - 1
        self._sift_up((node_i - 1) // 2, node_i)

    # input: parent index
    # output: index of smaller or greater child, one index if other DNE, or None
    def _get_swapped_child_index(self, p_i):
        size = len(self._heap)
        i = p_i * 2 + 1
        j = p_i * 2 + 2
        if size <= i:
            return None
        elif size <= j:
            return i

        if self._heap[i] > self._heap[j]:
            return j if self._min_heap else i
        else:
            return i if self._min_heap else j

    def _extract_root(self):
        if self._heap:
            self._swap(0, len(self._heap) - 1)
            root = self._heap.pop()
            self._sift_down(0, self._get_swapped_child_index(0))
            return root

    # extracts minimum value in O(logn) time
    def extract_min(self):
        if not self._min_heap:
            raise ValueError('Only min heaps support extract_min')
        return self._extract_root()

    # extracts maximum value in O(logn) time
    def extract_max(self):
        if self._min_heap:
            raise ValueError('Only max heaps support extract_max.')
        return self._extract_root()

    # deletes node from anywhere in heap in O(logn) time
    # input: key (i.e. index) of node to delete
    def delete(self, key):
        self._swap(key, len(self._heap) - 1)
        removed = self._heap.pop()

        p_i = (key - 1) // 2
        if not self._is_balanced(self._heap[p_i], self._heap[key]):
            self._sift_up(p_i, key)
        else:
            self._sift_down(p_i, key)

        return removed

    # initializes a heap in O(n) time
    def heapify(self):  # to do
        return self._heap


# input: filename
# output: Graph
def create_graph(filename):
    global G
    with open(filename) as f_handle:
        f_handle.readline()
        for line in f_handle:
            edge = line.split()
            u = int(edge[0])
            v = int(edge[1])
            cost = int(edge[2])
            G.add_e(u, v, cost)
    return G


def max_spacing_k_clustering(G):
    return None


def main():
    G = create_graph('max_spacing_k_clustering.txt')
    # print(G)

    start = time.time()
    result = max_spacing_k_clustering(G)
    print('result: ', result)
    print('elapsed time: ', time.time() - start)


main()
