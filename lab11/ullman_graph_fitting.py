import numpy as np
import copy


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


class MatrixGraph(Graph):
    def __init__(self):
        super().__init__()
        self.adj_matrix = []

    def insertVertex(self, vertex: Vertex):
        if vertex in self.vertices:
            return
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
            raise Warning("vertices:" + str(vertex1) + " or " + str(vertex2) + "aren't in graph")
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

    def get_adj_matrix(self):
        return copy.deepcopy(self.adj_matrix)

    def print_adj_mart(self):
        v = "   "
        st = ""
        for i in self.vertices:
            v += str(i.key)
            v += "  "
        for i in range(len(self.adj_matrix)):
            st += str(self.vertices[i].key) + " "
            st += str(self.adj_matrix[i])
            st += "\n"
        st = v + "\n" + st
        print(st)


def deg(matr, vert_ind):
    return np.sum(matr[vert_ind])


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


def is_isomorphism(P: np.ndarray, G: np.ndarray, M: np.ndarray):
    if (P == M @ np.transpose(M @ G)).all():
        return True
    else:
        return False


def neigh(G: np.ndarray, index):
    neig = []
    for i in range(G.shape[0]):
        if G[index, i] == 1:
            neig.append(i)
    return neig


def prune(M: np.ndarray, G: np.ndarray, P: np.ndarray, current_row):
    M_copy = M.copy()
    M = copy.deepcopy(M)
    while True:
        for i in range(M_copy.shape[0]):
            for j in range(M_copy.shape[1]):
                if M[i,j] == 1:
                    p_neigh = neigh(P, i)
                    g_neigh = neigh(G, j)

                    for n_P in p_neigh:
                        for n_G in g_neigh:
                            if M[n_P, n_G] == 1:
                                break
                        else:
                            M[i, j] = 0
        if (M == M_copy).all():
            break
        M_copy = M.copy()
    return M


def ullman_v1(used_col, current_row, G: np.ndarray, P: np.ndarray, M: np.ndarray, no_recursion=0, no_iso=0):
    no_recursion += 1
    if current_row == M.shape[0]:
        if is_isomorphism(P, G, M):
            return no_recursion, no_iso + 1
        else:
            return no_recursion, no_iso

    M_prim = copy.deepcopy(M)

    for i in range(len(used_col)):
        if used_col[i] == 0:
            used_col_cp = copy.deepcopy(used_col)
            M_prim[current_row, i] = 1
            M_prim[current_row, i + 1:] = 0
            M_prim[current_row, :i] = 0
            used_col_cp[i] = 1
            (no_recursion, no_iso) = ullman_v1(used_col_cp, current_row + 1, G, P, M_prim, no_recursion, no_iso)
            used_col_cp[i] = 0

    return no_recursion, no_iso


def get_MO(G: np.ndarray, P: np.ndarray):
    M0 = np.zeros((P.shape[0], G.shape[0]))
    for i in range(G.shape[0]):
        for j in range(P.shape[0]):
            if deg(G, i) >= deg(P, j):
                M0[j, i] = 1
    return M0


def ullman_v2(used_col, current_row, G: np.ndarray, P: np.ndarray, no_recursion=0, no_iso=0):
    M0 = get_MO(G, P)

    def ullman_h1(used_col, current_row, G: np.ndarray, P: np.ndarray, M: np.ndarray, no_recursion=0, no_iso=0,
                  M0=get_MO(G, P)):

        no_recursion += 1
        if current_row == M.shape[0]:
            if is_isomorphism(P, G, M):
                return no_recursion, no_iso + 1
            else:
                return no_recursion, no_iso

        M_prim = copy.deepcopy(M)

        for i in range(len(used_col)):
            if used_col[i] == 0 and M0[current_row, i] == 1:
                M_prim[current_row, i] = 1
                M_prim[current_row, i + 1:] = 0
                M_prim[current_row, :i] = 0
                used_col[i] = 1
                (no_recursion, no_iso) = ullman_h1(used_col, current_row + 1, G, P, M_prim, no_recursion, no_iso, M0)
                used_col[i] = 0

        return no_recursion, no_iso

    return ullman_h1(used_col, current_row, G, P, np.ones((P.shape[0], G.shape[1])), 0, 0, M0)


def ullman_v3(used_col, current_row, G: np.ndarray, P: np.ndarray, M: np.ndarray, no_recursion=0, no_iso=0):
    M0 = get_MO(G, P)

    def ullman_h2(used_col, current_row, G: np.ndarray, P: np.ndarray, M: np.ndarray, no_recursion=0, no_iso=0,
                  M0=None):

        no_recursion += 1
        if current_row == M.shape[0]:
            if is_isomorphism(P, G, M):
                return no_recursion, no_iso + 1
            else:
                return no_recursion, no_iso

        M_prim = prune(M, G, P, current_row)
        M = copy.deepcopy(M)
        for i in range(len(used_col)):
            if used_col[i] == 0 and M0[current_row, i] == 1:
                used_col_cp = copy.deepcopy(used_col)
                M[current_row, i] = 1
                M[current_row, i + 1:] = 0
                M[current_row, :i] = 0
                used_col_cp[i] = 1
                (no_recursion, no_iso) = ullman_h2(used_col_cp, current_row + 1, G, P, M, no_recursion, no_iso, M_prim)
                used_col_cp[i] = 0

        return no_recursion, no_iso

    return ullman_h2(used_col, current_row, G, P, M0, 0, 0, M0)



if __name__ == '__main__':
    vert_G = ['A', 'B', 'C', 'D', 'E', "F"]
    vert_P = ['A', 'B', 'C']
    graph_G_lst = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    graph_P_lst = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]

    graph_G = MatrixGraph()
    graph_P = MatrixGraph()
    for e in graph_G_lst:
        graph_G.insertEdge(Vertex(e[0]), Vertex(e[1]))

    for e in graph_P_lst:
        graph_P.insertEdge(Vertex(e[0]), Vertex(e[1]))

    # graph_G.print_adj_mart()
    # graph_P.print_adj_mart()
    graph_G_np = np.array(graph_G.get_adj_matrix())
    graph_P_np = np.array(graph_P.get_adj_matrix())
    M_v = np.zeros((graph_P_np.shape[0], graph_G_np.shape[0]))
    used = [0, 0, 0, 0, 0, 0]
    print(ullman_v1(used, 0, graph_G_np, graph_P_np, M_v))
    print(ullman_v2(used, 0, graph_G_np, graph_P_np))
    print(ullman_v3(used, 0, graph_G_np, graph_P_np, M_v))