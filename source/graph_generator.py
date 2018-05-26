from collections import defaultdict
from itertools import combinations

class GraphGenerator:

    def is_neighbor(self, graph, *neighbors):
        for n1, n2 in neighbors:
            graph[n1].append(n2)
            graph[n2].append(n1)

    def tree(self, n):
        '''Generate a tree.'''
        graph = defaultdict(list)
        for i in range(2**n-1):
            self.is_neighbor(graph, (i, 2*i + 1), (i, 2*i + 2))
        return graph

    def star(self, n):
        '''Generate a star.'''
        graph = defaultdict(list)
        for i in range(n):
            self.is_neighbor(graph, (n, n + 1 + i))
        return graph

    def full_mesh(self, n):
        '''Generate a full-mesh.'''
        graph = defaultdict(list)
        for i in range(n):
            for j in range(i):
                self.is_neighbor(graph, (n + j, n + i))
        return graph

    def ring(self, n):
        '''Generate a ring'''
        graph = defaultdict(list)
        for i in range(n):
            self.is_neighbor(graph, (n + i, n + (1 + i)%n))
        return graph

    def square_tiling(self, n):
        '''Generate a square tiling'''
        graph = defaultdict(list)
        for i in range(n**2):
            if i - 1 > -1 and i % n:
                self.is_neighbor(graph, (i, i - 1))
            if i + n < n**2:
                self.is_neighbor(graph, (i - 1, i + n))
        return graph

    def hypercube(self, n):
        '''Generate a hypercube'''
        graph = defaultdict(list)
        # we create a n-dim hypercube by connecting two (n-1)-dim hypercubes
        i = 0
        nodes = [0]
        links = []
        while i < n:
            for k in range(len(nodes)):
                # creation of the nodes of the second hypercube
                nodes.append(k + 2**i)
            for source, destination in links[:]:
                # connection of the two hypercubes
                links.append((source + 2**i, destination + 2**i))
            for k in range(len(nodes) // 2):
                # creation of the physical links of the second hypercube
                links.append((nodes[k], nodes[k + 2**i]))
            i += 1
        self.is_neighbor(graph, *links)
        return graph

    def petersen(self, n, k):
        '''Generate a Petersen graph'''
        graph = defaultdict(list)
        # the petersen graph is made of the vertices (u_i) and (v_i) for 
        # i in [0, n-1] and the edges (u_i, u_i+1), (u_i, v_i) and (v_i, v_i+k).
        # to build it, we consider that v_i = u_(i+n).
        for i in range(n):
            # (u_i, u_i+1) edges
            self.is_neighbor(graph, (i, (i + 1) % n))
            # (u_i, v_i) edges
            self.is_neighbor(graph, (i, i + n))
            # (v_i, v_i+k) edges
            self.is_neighbor(graph, (i + n, (i + n + k) % n + n))
        return graph
