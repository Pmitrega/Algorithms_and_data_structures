# skonczone
import graf_mst


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
    def __init__(self, vertex1, vertex2, weight=1):
        self.start = vertex1
        self.end = vertex2
        self.weight = weight

    def __str__(self):
        return str(self.start) + "->" + str(self.end)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end


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
            self.edges_lst.append(Edge(vert1, vert2, weight))
            ## dla nieskierowaniego zakomentować linijke ponizej
            self.edges_lst.append(Edge(vert2, vert1, weight))
        else:
            pass
            # raise Warning("edge already exists")

    def neighbours(self, vertex_ind):
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
            edges.append((edge.start.key, edge.end.key, edge.weight))
        return edges

    def size(self):
        return len(self.edges())


class UnionFind:
    def __init__(self, graph):
        self.n = graph.order()
        self.parent = [graph.getVertexIdx(v) for v in graph.vertices]
        self.size = [1 for i in range(graph.order())]

    def find(self, v_ind):
        if v_ind == self.parent[v_ind]:
            return v_ind
        else:
            return self.find(self.parent[v_ind])

    def union_sets(self, s1, s2):
        root_s1 = self.find(s1)
        root_s2 = self.find(s2)
        if root_s1 == root_s2:
            return
        else:
            if self.size[root_s1] > self.size[root_s2]:
                # for v_ind in range(self.n):
                #     if self.find(v_ind) == root_s2:
                #         self.size[v_ind] += 1
                self.parent[root_s2] = root_s1
                #self.size[root_s2] += 1
            elif self.size[root_s1] < self.size[root_s2]:
                # for v_ind in range(self.n):
                #     if self.find(v_ind) == root_s1:
                #         self.size[v_ind] += 1
                # if self.size[root_s1] == self.size[root_s2]:
                self.parent[root_s1] = root_s2
                #self.size[root_s1] += 1
            else:
                self.parent[root_s1] = root_s2
                self.size[root_s2] += 1

    def same_components(self, s1, s2):
        return self.find(s1) == self.find(s2)


def printGraph(g):
    n = g.order()
    print("------GRAPH------", n)
    for i in range(n):
        v = g.getVertex(i)
        print(v, end=" -> ")
        nbrs = g.neighbours(i)
        for (j, w) in nbrs:
            print(g.getVertex(j), w, end=";")
        print()
    print("-------------------")


def weight(edg):
    return edg.weight


def MST_kruskal(graph: LstGraph):
    union_find = UnionFind(graph)
    result_graph = LstGraph()
    edges = graph.edges_lst[:]
    edges.sort(key=weight)
    for e in edges:
        start_ind = graph.getVertexIdx(e.start)
        end_ind = graph.getVertexIdx(e.end)
        if not union_find.same_components(start_ind, end_ind):
            union_find.union_sets(start_ind, end_ind)
            result_graph.insertEdge(Vertex(graph.getVertex(start_ind)), Vertex(graph.getVertex(end_ind)), e.weight)
    return result_graph

graph = LstGraph()

for i in range(len(graf_mst.graf)):
    graph.insertEdge(Vertex(graf_mst.graf[i][0]), Vertex(graf_mst.graf[i][1]), graf_mst.graf[i][2])


printGraph(graph)
mst_krusk = MST_kruskal(graph)
printGraph(mst_krusk)
### algorytm poprawnie wyznacza MST, a struktura union find jest zrównoważona