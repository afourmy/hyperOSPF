from collections import defaultdict

class GraphGenerator:
    
    def is_neighbor(self, graph, *neighbors):
        print(graph, neighbors)
        for n1, n2 in neighbors:
            graph[n1].append(n2)
            graph[n2].append(n1)

    def tree(self, n):
        '''Generate a tree.'''
        graph = defaultdict(list)
        for i in range(2**n-1):
            n1, n2, n3 = i, 2*i+1, 2*i+2
            self.is_neighbor(graph, (n1, n2), (n1, n3))
        return graph

    def star(self, n, subtype):
        '''Generate a star.'''
        nb_node = self.cpt_node + 1
        for i in range(n):
            n1, n2 = str(nb_node), str(nb_node+1+i)
            source = self.nf(name = n1, subtype = subtype)
            destination = self.nf(name = n2, subtype = subtype)
            yield source
            yield destination
            yield self.lf(source=source, destination=destination)

    def full_mesh(self, n, subtype):
        '''Generate a full-mesh.'''
        nb_node = self.cpt_node + 1
        for i in range(n):
            for j in range(i):
                n1, n2 = str(nb_node+j), str(nb_node+i)
                source = self.nf(name = n1, subtype = subtype)
                destination = self.nf(name = n2, subtype = subtype)
                yield source
                yield destination
                yield self.lf(source=source, destination=destination)

    def ring(self, n, subtype):
        '''Generate a ring'''
        nb_node = self.cpt_node + 1
        for i in range(n):
            n1, n2 = str(nb_node+i), str(nb_node+(1+i)%n)
            source = self.nf(name = n1, subtype = subtype)
            destination = self.nf(name = n2, subtype = subtype)
            yield source
            yield destination
            yield self.lf(source=source, destination=destination)

    def square_tiling(self, n, subtype):
        '''Generate a square tiling'''
        for i in range(n**2):
            n1, n2, n3 = str(i), str(i-1), str(i+n)
            if i-1 > -1 and i%n:
                source = self.nf(name = n1, subtype = subtype)
                destination = self.nf(name = n2, subtype = subtype)
                yield source
                yield destination
                yield self.lf(source=source, destination=destination)
            if i+n < n**2:
                source = self.nf(name = n1, subtype = subtype)
                destination = self.nf(name = n3, subtype = subtype)
                yield source
                yield destination
                yield self.lf(source=source, destination=destination)

    def hypercube(self, n, subtype):
        '''Generate a hypercube'''
        # we create a n-dim hypercube by connecting two (n-1)-dim hypercubes
        i = 0
        graph_nodes = [self.nf(name=str(0), subtype=subtype)]
        graph_plinks = []
        while i < n+1:
            for k in range(len(graph_nodes)):
                # creation of the nodes of the second hypercube
                graph_nodes.append(
                                   self.nf(
                                           name = str(k+2**i), 
                                           subtype = subtype
                                           )
                                   )
            for plink in graph_plinks[:]:
                # connection of the two hypercubes
                source, destination = plink.source, plink.destination
                n1 = str(int(source.name) + 2**i)
                n2 = str(int(destination.name) + 2**i)
                graph_plinks.append(
                                   self.lf(
                                           source = self.nf(name = n1), 
                                           destination = self.nf(name = n2)
                                           )
                                   )
            for k in range(len(graph_nodes)//2):
                # creation of the physical links of the second hypercube
                graph_plinks.append(
                                   self.lf(
                                           source = graph_nodes[k], 
                                           destination = graph_nodes[k+2**i]
                                           )
                                   )
            i += 1
        yield from graph_nodes
        yield from graph_plinks

    def kneser(self, n, k, subtype):
        '''Generate a Kneser graph'''
        # we keep track of what set we've seen to avoid having
        # duplicated edges in the graph, with the 'already_done' set
        already_done = set()
        for setA in map(set, combinations(range(1, n), k)):
            already_done.add(frozenset(setA))
            for setB in map(set, combinations(range(1, n), k)):
                if setB not in already_done and not setA & setB:
                    source = self.nf(name = str(setA), subtype = subtype)
                    destination = self.nf(name = str(setB), subtype = subtype)
                    yield source
                    yield destination
                    yield self.lf(source=source, destination=destination)

    def petersen(self, n, k, subtype):
        '''Generate a Petersen graph'''
        # the petersen graph is made of the vertices (u_i) and (v_i) for 
        # i in [0, n-1] and the edges (u_i, u_i+1), (u_i, v_i) and (v_i, v_i+k).
        # to build it, we consider that v_i = u_(i+n).
        for i in range(n):
            # (u_i, u_i+1) edges
            source = self.nf(name = str(i), subtype = subtype)
            destination = self.nf(name = str((i + 1)%n), subtype = subtype)
            yield source
            yield destination
            yield self.lf(source=source, destination=destination)
            # (u_i, v_i) edges
            source = self.nf(name = str(i), subtype = subtype)
            destination = self.nf(name = str(i+n), subtype = subtype)
            yield source
            yield destination
            yield self.lf(source=source, destination=destination)
            # (v_i, v_i+k) edges
            source = self.nf(name = str(i+n), subtype = subtype)
            destination = self.nf(name = str((i+n+k)%n + n), subtype = subtype)
            yield source
            yield destination
            yield self.lf(source=source, destination=destination)