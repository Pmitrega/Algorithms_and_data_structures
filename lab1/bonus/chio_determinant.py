# skonczone
from typing import Tuple, Union, List


class Matrix:
    __matrix: List[List[int]]
    __rows: int
    __cols: int

    def __init__(self, arr: Union[Tuple[int, int], List[List[Union[float, int]]]], val: int = 0):
        self.__matrix = []
        if isinstance(arr, Tuple) and arr.__len__() == 2:
            self.__rows = arr[0]
            self.__cols = arr[1]
            for row in range(self.__rows):
                r = []
                for col in range(self.__cols):
                    r.append(val)
                self.__matrix.append(r)
        elif isinstance(arr, List):
            self.__rows = arr.__len__()
            self.__cols = arr[0].__len__()
            for row in range(self.__rows):
                r = []
                for col in range(self.__cols):
                    r.append(arr[row][col])
                self.__matrix.append(r)
        else:
            raise ValueError("Argument must be tuple or list[list]")

    def __add__(self, other):
        if other.__len__()[1] != self.__cols or other.__len__()[0] != self.__rows:
            raise ValueError("Size of matrices doesn't match")
        mat = Matrix(self.__matrix[:])
        for i in range(self.__rows):
            for j in range(self.__cols):
                mat[i][j] += other[i][j]
        return mat

    def __getitem__(self, item):
        return self.__matrix[item]

    def __mul__(self, other):
        if self.__cols != other.__len__()[0]:
            raise ValueError("Wrong size of matrices")
        mat = Matrix((self.__rows, other.__len__()[1]))
        for row in range(mat.__len__()[0]):
            for col in range(mat.__len__()[1]):
                result = 0
                for i in range(self.__cols):
                    result += self.__matrix[row][i] * other[i][col]
                mat[row][col] = result
        return mat

    def __str__(self):
        r_str = "[\n"
        for i in range(self.__rows):
            r_str += '['
            for j in range(self.__cols):
                r_str += str(self.__matrix[i][j])
                if j != (self.__cols - 1):
                    r_str += ', '
            r_str += ']\n'
        r_str += "]"
        return r_str

    def __len__(self):
        return self.__rows, self.__cols


def transpose(matr: Matrix):
    size = matr.__len__()
    t_matr = Matrix((size[1], size[0]))
    for row in range(size[1]):
        for col in range(size[0]):
            t_matr[row][col] = matr[col][row]
    return t_matr


def determinant_chio(matr: Matrix):
    if matr.__len__()[0] != matr.__len__()[1]:
        raise ValueError("Argument must be square matrix")
    if matr.__len__()[0] == 2:
        return matr[0][0] * matr[1][1] - matr[0][1] * matr[1][0]
    change_flag = 0
    if matr[0][0] == 0:  # rozwązanie problemu, gdy pierwszy element jest równy 0
        for i in range(matr.__len__()[0]):
            if matr[i][0] != 0:
                tmp_lst = matr[:]  # kopujemy listę list z macierzy
                tmp_lst[0], tmp_lst[i] = tmp_lst[i], tmp_lst[0]
                matr = Matrix(tmp_lst)
                # gdy następuje zamiana wiersza wyznacznik zmienia znak na przeciwny, zostanie to użyte do zmiany znaku
                # ponadto, jeśli nie zaszła zamiana to wyznacznik jest równy 0
                change_flag = 1
                break
        if change_flag == 0:
            return 0  # wyznacznik jest rowny 0 gdzy pierwsza kolumna jest równa 0
    new_matr = Matrix((matr.__len__()[0] - 1, matr.__len__()[0] - 1))
    for row in range(new_matr.__len__()[0]):
        for col in range(new_matr.__len__()[0]):
            new_matr[row][col] = matr[0][0] * matr[row + 1][col + 1] - matr[0][col + 1] * matr[row + 1][0]
    return 1 / (matr[0][0] ** (matr.__len__()[0] - 2)) * (-1) ** change_flag * determinant_chio(new_matr)


m1 = Matrix([
    [5, 1, 1, 2, 3],
    [4, 2, 1, 7, 3],
    [2, 1, 2, 4, 7],
    [9, 1, 0, 7, 0],
    [1, 4, 7, 2, 2]

])
m2 = Matrix([
    [0, 1, 1, 2, 3],
    [4, 2, 1, 7, 3],
    [2, 1, 2, 4, 7],
    [9, 1, 0, 7, 0],
    [1, 4, 7, 2, 2]
])

print("m1:\n",m1)
print("m2:\n",m2)
print("wyznacznik m1:\n",determinant_chio(m1))
print("wyznacznik m2:\n",determinant_chio(m2))
print("m1 po operacjach(dla pewności, że nie zaszła jakaś zmiana):\n",m1)
print("m2 po operacjach(dla pewności, że nie zaszła jakaś zmiana):\n",m2)