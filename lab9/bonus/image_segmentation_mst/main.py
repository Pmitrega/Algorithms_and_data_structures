##skonczone
import cv2
import numpy as np
import matplotlib.pyplot as plt

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


def MST(graph):
    new_graph = LstGraph()
    for v in graph.vertices:
        new_graph.insertVertex(v)
    intree = [0 for i in range(new_graph.order())]
    distance = [float('inf') for i in range(new_graph.order())]
    parent = [-1 for i in range(new_graph.order())]
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
        new_graph.insertEdge(Vertex(graph.getVertex(min_ind).key), Vertex(graph.getVertex(parent[min_ind]).key), minn)
        length += minn
    return new_graph, length


def BFS(graph: LstGraph, start: Vertex):
    visited = [graph.getVertexIdx(start)]
    queue = [graph.getVertexIdx(start)]
    while len(queue) > 0:
        v = queue.pop()
        n = graph.neighbours(v)
        for (i, w) in n:
            if i not in visited:
                queue.insert(0, i)
                visited.append(i)
    return visited


I = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE)

graph = LstGraph()
for i in range(I.shape[0]):
    for j in range(I.shape[1]):
        graph.insertVertex(Vertex(I.shape[1] * j + i, I[i, j]))

for i in range(1, I.shape[0] - 1):
    for j in range(1, I.shape[1] - 1):
        central_vert_key = I.shape[1] * j + i
        for k in range(3):
            for m in range(3):
                pixel_j = j - 1 + m
                pixel_i = i - 1 + k
                curr_vert_key = I.shape[1] * pixel_j + pixel_i
                if pixel_i != i or pixel_j != j:
                    graph.insertEdge(Vertex(curr_vert_key, color=I[pixel_i, pixel_j]),
                                     Vertex(central_vert_key, color=I[i, j]), abs(int(I[pixel_i, pixel_j]) - int(I[i, j])))


def decode_key(key, shape):
    i = key % shape[0]
    j = key // shape[1]
    return i, j


graph, v = MST(graph)
maxim = 0
maxim_ind = 0
v_1 = None
v_2 = None


for i in range(len(graph.edges_lst)):
    if graph.edges_lst[i].weight > maxim:
        maxim_ind = i
        maxim = graph.edges_lst[i].weight
        v_1 = graph.edges_lst[i].end
        v_2 = graph.edges_lst[i].start


graph.deleteEdge(v_1, v_2)
visited_1 = BFS(graph, v_1)
visited_2 = BFS(graph, v_2)



IS = np.zeros(I.shape, dtype='uint8')

for ind in visited_1:
    x, y = decode_key(graph.vertices[ind].key, I.shape)
    IS[x, y] = 100

for ind in visited_2:
    x, y = decode_key(graph.vertices[ind].key, I.shape)
    IS[x, y] = 120

plt.imshow(IS, "gray", vmin=0, vmax=255)
plt.show()
## dodawanie krawędzi może potrwać długo, ponieważ moja implementacja sprawdza, czy istnieje już
## zadana krawędź, co ma złożoność O(n), łącząc to z dodawaniem po całym obrazie daje to O(n^3)

##Po obcięciu krawędzi wyraźnie widać podział obrazu na dwie części, tą która była czarna i na białą.
## algorytm pomija krawędzie (mają tylko jednego sąsiada, zamiast 3 lub 2)



