#skonczone
import polska
from typing import Union

class Vertex:
    def __init__(self, key):
        self.key = key

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key

    def __str__(self):
        return str(self.key)


class Edge:
    def __init__(self, vertex1, vertex2):
        self.start = vertex1
        self.end = vertex2

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
        self.dic_obj[vertex] = vertex.key
        self.dic_key[vertex.key] = vertex

    def getVertexIdx(self, vert):
        return self.dic_obj[vert]

    def getVertex(self, vertex_idx):
        return self.dic_key[vertex_idx]

    def order(self):
        return len(self.vertices)


class LstGraph(Graph):
    def __init__(self):
        super().__init__()
        self.edges_lst = []

    def insertEdge(self, vert1, vert2, edge=None):
        if vert1 not in self.vertices:
            self.insertVertex(vert1)
        if vert2 not in self.vertices:
            self.insertVertex(vert2)
        if Edge(vert1, vert2) not in self.edges_lst and Edge(vert2, vert1) not in self.edges_lst:
            self.edges_lst.append(Edge(vert1, vert2))
            self.edges_lst.append(Edge(vert2, vert1))
        else:
            pass
            # raise Warning("edge already exists")

    def neighbours(self, vertex_ind):
        neigh = []
        if not Vertex(vertex_ind) in self.vertices:
            return []
        for edg in self.edges_lst:
            if self.getVertexIdx(edg.start) == vertex_ind:
                neigh.append(self.getVertexIdx(edg.end))
        return neigh

    def deleteVertex(self, vertex):
        if vertex not in self.vertices:
            raise Warning("Vertex " + str(vertex) + " isn't in graph")
        temp = self.edges_lst[:]
        for edg in self.edges_lst:
            if edg.start == vertex or edg.end == vertex:
                temp.remove(edg)
        self.vertices.remove(vertex)
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
            edges.append((self.getVertexIdx(edge.start), self.getVertexIdx(edge.end)))
        return edges

    def size(self):
        ## każdą krawędz licze jako 2 bo jest nieskierowany
        return len(self.edges())


class MatrixGraph(Graph):
    def __init__(self):
        super().__init__()
        self.adj_matrix = []

    def insertVertex(self, vertex: Vertex):
        if vertex in self.vertices:
            raise Warning("Vertex " + str(vertex) + " already exists")
        super().insertVertex(vertex)
        if len(self.adj_matrix) != len(self.vertices):
            for row in self.adj_matrix:
                row.append(0)
            self.adj_matrix.append([0] * len(self.vertices))

    def insertEdge(self, vertex1, vertex2):
        if not vertex1 in self.vertices:
            self.insertVertex(vertex1)
        if not vertex2 in self.vertices:
            self.insertVertex(vertex2)
        i = self.vertices.index(vertex1)
        j = self.vertices.index(vertex2)
        self.adj_matrix[i][j] = 1
        self.adj_matrix[j][i] = 1

    def deleteVertex(self, vertex):
        if vertex not in self.vertices:
            raise Warning("Vertex " + str(vertex) + " isn't in graph")
        if len(self.adj_matrix) == 0:
            return

        k = self.vertices.index(vertex)
        for i in range(len(self.adj_matrix) - 1):
            self.adj_matrix[i].pop(k)
        self.adj_matrix.pop(k)
        self.vertices.pop(k)

    def deleteEdge(self, vertex1, vertex2):
        if vertex1 not in self.vertices or vertex2 not in self.vertices:
            raise Warning("vertices:" +str(vertex1) + " or " + str(vertex2) + "aren't in graph")
        i = self.vertices.index(vertex1)
        j = self.vertices.index(vertex2)
        self.adj_matrix[i][j] = 0
        self.adj_matrix[j][i] = 0

    def __str__(self):
        st = "  "
        for v in self.vertices:
            st += str(v) + " "
        st += '\n'
        for i in range(len(self.adj_matrix)):
            st += str(self.vertices[i]) + " "
            for j in range(len(self.adj_matrix)):
                st += str(self.adj_matrix[i][j]) + " "
            st += '\n'
        return st

    def edges(self):
        egs = []
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)):
                if self.adj_matrix[i][j] != 0:
                    start = self.getVertexIdx(self.vertices[i])
                    end = self.getVertexIdx(self.vertices[j])
                    egs.append((start, end))
        return egs

    def size(self):
        o = 0
        for v in self.adj_matrix:
            o += sum(v)
        return o

    def neighbours(self, vertex_ind):
        neigh = []
        try:
            k = self.vertices.index(Vertex(vertex_ind))
        except:
            return None
        for i in range(len(self.vertices)):
            if self.adj_matrix[k][i] != 0:
                neigh.append(self.getVertexIdx(self.vertices[i]))
        return neigh


def DFS(graph: Union[LstGraph, MatrixGraph], start: Vertex):
    visited = [graph.getVertexIdx(start)]
    stack = [graph.getVertexIdx(start)]

    while len(stack) > 0:
        v = stack.pop()
        neigh = graph.neighbours(v)
        ##żeby DFS był od lewej
        neigh.reverse()
        if v not in visited:
            visited.append(v)

        for n in neigh:
            if n not in visited:
                stack.append(n)
    return visited


def BFS(graph: Union[LstGraph, MatrixGraph], start: Vertex):
    visited = [graph.getVertexIdx(start)]
    queue = [graph.getVertexIdx(start)]
    while len(queue) > 0:
        v = queue.pop()
        n = graph.neighbours(v)
        for i in n:
            if i not in visited:
                queue.insert(0, i)
                visited.append(i)
    return visited


def color_graph(graph: Union[LstGraph, MatrixGraph], start: Vertex,method: str):
    if method == "BFS":
        order = BFS(graph, start)
    elif method == "DFS":
        order = DFS(graph, start)
    else:
        raise TypeError("method doesn't exist (" + method+")" )

    col_dic = {vert: None for vert in order}
    for i in order:
        neigh = graph.neighbours(i)
        neigh_col = []
        for n in neigh:
            neigh_col.append(col_dic[n])
        color = 1
        while color in neigh_col:
            color += 1
        col_dic[i] = color

    pair_lst = []
    for v in col_dic:
        pair_lst.append((v, col_dic[v]))

    return pair_lst



if __name__ == "__main__":
    graph = LstGraph()
    # graph = MatrixGraph()

    for p in polska.graf:
        graph.insertEdge(Vertex(p[0]), Vertex(p[1]))
    graph.deleteVertex(graph.getVertex('K'))
    graph.deleteEdge(graph.getVertex('W'), graph.getVertex('E'))
    polska.draw_map(graph.edges(), color_graph(graph, Vertex("W"), "DFS"))
    #polska.draw_map(graph.edges(), color_graph(graph, Vertex("W"), "BFS"))
