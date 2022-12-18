#skonczone
import graf_mst

class Vertex:
    def __init__(self, key, color = 0):
        self.key = key
        self.color = color
    def setColor(self, color):
        self.color= color

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key

    def __str__(self):
        return str(self.key)


class Edge:
    def __init__(self, vertex1, vertex2, weight = 1):
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

    def insertEdge(self, vert1, vert2, weight = 1):
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
            edges.append((edge.start.key, edge.end.key))
        return edges

    def size(self):
        return len(self.edges())

def printGraph(g):
    n = g.order()
    print("------GRAPH------",n)
    for i in range(n):
        v = g.getVertex(i)
        print(v, end = " -> ")
        nbrs = g.neighbours(i)
        for (j, w) in nbrs:
            print(g.getVertex(j), w, end=";")
        print()
    print("-------------------")

graph = LstGraph()

for i in range(len(graf_mst.graf)):
    graph.insertEdge(Vertex(graf_mst.graf[i][0]), Vertex(graf_mst.graf[i][1]), graf_mst.graf[i][2])
# printGraph(graph)

def MST(graph):
    new_graph = LstGraph()
    for v in graph.vertices:
        new_graph.insertVertex(v)
    intree = [0 for i in range (new_graph.order())]
    distance = [float('inf') for i in range (new_graph.order())]
    parent = [-1 for i in range (new_graph.order())]
    curr_vert = new_graph.vertices[0]
    length = 0
    while intree[graph.getVertexIdx(curr_vert)] == 0:
        intree[graph.getVertexIdx(curr_vert)] = 1
        neig = graph.neighbours(graph.getVertexIdx(curr_vert))
        for (v_i, w) in neig:
            if w < distance[v_i] and intree[v_i] == 0:
                distance[v_i] = w
                parent[v_i] = graph.getVertexIdx(curr_vert)
        minn = float("inf")
        min_ind = -1
        for v_i in range(len(intree)):
            if not intree[v_i]:
                if distance[v_i] < minn:
                    min_ind = v_i
                    minn = distance[v_i]
        if min_ind == -1:
            break
        curr_vert = graph.getVertex(min_ind)
        new_graph.insertEdge(Vertex(graph.getVertex(min_ind).key),Vertex(graph.getVertex(parent[min_ind]).key), minn)
        length +=minn
    return new_graph, length



new, length = MST(graph)
printGraph(new)




