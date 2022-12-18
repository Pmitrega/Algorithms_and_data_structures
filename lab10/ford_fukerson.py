## skonczone

class Vertex:
    def __init__(self, key, color=0):
        self.key = key
        self.color = color

    def setColor(self, color):
        self.color = color

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key

    def __str__(self):
        return str(self.key)


class Edge:
    def __init__(self, vertex1, vertex2, capacity=1, is_residual=False):
        self.start = vertex1
        self.end = vertex2
        self.weight = capacity
        if not is_residual:
            self.flow = 0
            self.is_residual = is_residual
            self.residual = capacity
        else:
            self.flow = 0
            self.is_residual = is_residual
            self.residual = 0

    # def __str__(self):
    #     return str(self.start) + "->" + str(self.end)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __repr__(self):
        return str(self.start) + "->" + str(self.end) + " c:" + str(self.weight) + " f:" + str(self.flow) + " r:" + str(
            self.residual) + " " + str(self.is_residual)


class Graph:
    def __init__(self):
        self.vertices = []
        self.dic_obj = {}
        self.dic_key = {}

    def insertVertex(self, vertex: Vertex):
        self.vertices.append(vertex)

        self.dic_obj[vertex] = len(self.vertices) - 1
        self.dic_key[len(self.vertices) - 1] = vertex

    def getVertexIdx(self, vert):
        return self.dic_obj[vert]

    def getVertex(self, vertex_idx):
        return self.vertices[vertex_idx]

    def order(self):
        return len(self.vertices)


class LstGraph(Graph):
    def __init__(self):
        super().__init__()
        self.edges_lst = []

    def insertEdge(self, vert1, vert2, weight=1):
        if vert1 not in self.vertices:
            self.insertVertex(vert1)
        if vert2 not in self.vertices:
            self.insertVertex(vert2)
        if Edge(vert1, vert2) not in self.edges_lst and Edge(vert2, vert1) not in self.edges_lst:
            self.edges_lst.append(Edge(vert1, vert2, weight, False))
            ## dla nieskierowaniego zakomentować linijke ponizej
            self.edges_lst.append(Edge(vert2, vert1, weight, True))
        else:
            pass
            # raise Warning("edge already exists")

    def neighbours(self, vertex_ind):
        neigh = []
        if vertex_ind >= len(self.vertices):
            return None
        for edg in self.edges_lst:
            if edg.start.key == self.vertices[vertex_ind].key:
                neigh.append(edg)
        return neigh

    def neighbours2(self, vertex_ind):
        neigh = []
        if vertex_ind >= len(self.vertices):
            return None
        for edg in self.edges_lst:
            if edg.start.key == self.vertices[vertex_ind].key:
                neigh.append((self.getVertexIdx(edg.end), edg.weight))
        return neigh

    def deleteVertex(self, vertex):
        if vertex not in self.vertices:
            raise Warning("Vertex " + str(vertex) + " isn't in graph")
        temp = self.edges_lst[:]
        for edg in self.edges_lst:
            if edg.start == vertex or edg.end == vertex:
                temp.remove(edg)
        self.vertices.remove(vertex)
        new_dic_obj = {}
        new_dic_key = {}
        for i in range(len(self.vertices)):
            new_dic_obj[self.vertices[i]] = i
        self.dic_obj = new_dic_obj
        self.dic_key = new_dic_key
        self.edges_lst = temp

    def deleteEdge(self, vertex1, vertex2):
        e1 = None
        e2 = None
        for edg in self.edges_lst:
            if edg.start == vertex1 and edg.end == vertex2:
                e1 = edg
            if edg.start == vertex2 and edg.end == vertex1:
                e2 = edg
        if e1 is not None:
            self.edges_lst.remove(e1)
        if e2 is not None:
            self.edges_lst.remove(e2)

    def edges(self):
        edges = []
        for edge in self.edges_lst:
            edges.append((edge.start.key, edge.end.key))
        return edges

    def size(self):
        return len(self.edges())


def printGraph(g):
    n = g.order()
    print("------GRAPH------", n)
    for i in range(n):
        v = g.getVertex(i)
        print(v, end=" -> ")
        nbrs = g.neighbours(i)
        for n in nbrs:
            print(n.end, n.weight, n.flow, n.residual, n.is_residual, end=";")
        print()
    print("-------------------")


def BFS(graph: LstGraph, start):
    if start >= len(graph.vertices):
        raise IndexError("vertex out of range")
    visited = [-1 for el in graph.vertices]
    parent = [-1 for el in graph.vertices]
    queue = [start]
    visited[start] = 1
    while len(queue) > 0:
        el = queue.pop()
        neigh = graph.neighbours(el)
        for n in neigh:
            if visited[graph.getVertexIdx(n.end)] == -1 and n.residual > 0:
                queue.append(graph.getVertexIdx(n.end))
                parent[graph.getVertexIdx(n.end)] = el
                visited[graph.getVertexIdx(n.end)] = 1
    return parent


def lowest_capacity(graph, start_ind, end_ind, parent):
    curr_ind = end_ind
    lowest_cap = float("inf")
    if parent[curr_ind] == -1:
        return 0

    while curr_ind != start_ind:
        par = parent[curr_ind]
        par_ver = graph.getVertex(par)
        curr_ver = graph.getVertex(curr_ind)
        neigh = graph.neighbours(par)
        non_res = None
        for n in neigh:
            if graph.getVertexIdx(n.end) == curr_ind and not n.is_residual:
                non_res = n
                if non_res.residual < lowest_cap:
                    lowest_cap = non_res.residual
        if non_res is None:
            for n in neigh:
                if graph.getVertexIdx(n.end) == curr_ind and n.is_residual:
                    non_res = n
                    if non_res.residual < lowest_cap:
                        lowest_cap = non_res.residual
        curr_ind = par
    return lowest_cap


def augmentation(graph, start_ind, end_ind, parent, lowest_cap):
    curr_ind = end_ind
    if parent[curr_ind] == -1:
        return 0

    while curr_ind != start_ind:
        par = parent[curr_ind]
        neigh_children = graph.neighbours(curr_ind)
        par_ver = graph.getVertex(par)
        curr_ver = graph.getVertex(curr_ind)
        res = None
        for n in neigh_children:
            if graph.getVertexIdx(n.end) == par and n.is_residual:
                res = n
        neigh = graph.neighbours(par)
        non_res = None
        for n in neigh:
            if graph.getVertexIdx(n.end) == curr_ind and not n.is_residual:
                non_res = n
        ## jak nie ma rzeczywistej korzystamy z rezydualnej -------- inaczej algorytm nie działa dla gdy powracamy przepływ
        if non_res is None:
            res = None
            for n in neigh_children:
                if graph.getVertexIdx(n.end) == par and not n.is_residual:
                    res = n
            neigh = graph.neighbours(par)
            non_res = None
            for n in neigh:
                if graph.getVertexIdx(n.end) == curr_ind and n.is_residual:
                    non_res = n
        non_res.flow += lowest_cap
        non_res.residual -= lowest_cap
        res.residual += lowest_cap
        curr_ind = par


def ford_fulkerson(graph, start, end):
    flow = 0
    parent = BFS(graph, start)
    if parent[end] == -1:
        raise AssertionError("cant find path")
    min_flow = lowest_capacity(graph, start, end, parent)
    flow += min_flow
    while min_flow > 0:
        augmentation(graph, start, end, parent, min_flow)
        parent = BFS(graph, start)
        min_flow = lowest_capacity(graph, start, end, parent)
        flow += min_flow
    return flow


graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]
# 3
graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9), ('b', 't', 20),
          ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]
# 23
graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6),
          ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9), ('d', 'a', 1)]
# 5
graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7),
          ('d', 'c', 4)]
# 6
graph = LstGraph()
for el in graf_0:
    graph.insertEdge(Vertex(el[0]), Vertex(el[1]), el[2])
print("max_flow:",ford_fulkerson(graph,graph.getVertexIdx(Vertex('s')), graph.getVertexIdx(Vertex('t'))))
printGraph(graph)

graph = LstGraph()
for el in graf_1:
    graph.insertEdge(Vertex(el[0]), Vertex(el[1]), el[2])
print("max_flow:",ford_fulkerson(graph,graph.getVertexIdx(Vertex('s')), graph.getVertexIdx(Vertex('t'))))
printGraph(graph)

graph = LstGraph()
for el in graf_2:
    graph.insertEdge(Vertex(el[0]), Vertex(el[1]), el[2])
print("max_flow:",ford_fulkerson(graph, graph.getVertexIdx(Vertex('s')), graph.getVertexIdx(Vertex('t'))))
printGraph(graph)

graph = LstGraph()
for el in graf_3:
    graph.insertEdge(Vertex(el[0]), Vertex(el[1]), el[2])
print("max_flow:",ford_fulkerson(graph,graph.getVertexIdx(Vertex('s')), graph.getVertexIdx(Vertex('t'))))
printGraph(graph)
