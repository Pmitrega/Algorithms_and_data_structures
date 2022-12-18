#skonczone
from typing import Tuple, Union, List


class Matrix:
    __matrix: List[List[int]]
    __rows: int
    __cols: int

    def __init__(self, arr: Union[Tuple[int, int], List[List[Union[float,int]]]], val: int = 0):
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
                    result += self.__matrix[row][i]*other[i][col]
                mat[row][col] = result
        return mat


    def __str__(self):
        r_str = "[\n"
        for i in range(self.__rows):
            r_str+='['
            for j in range(self.__cols):
                r_str += str(self.__matrix[i][j])
                if j != (self.__cols-1):
                    r_str += ', '
            r_str += ']\n'
        r_str += "]"
        return r_str
    def __len__(self):
        return self.__rows, self.__cols


def transpose(matr :Matrix):
    size = matr.__len__()
    t_matr = Matrix((size[1], size[0]))
    for row in range(size[1]):
        for col in range(size[0]):
            t_matr[row][col] = matr[col][row]
    return t_matr

m1 = Matrix([ [1, 0, 2],
             [-1, 3, 1] ])
print("m1:\n", m1)
m2 = Matrix((2,3),1)
print("m2:\n", m2)
m3 = Matrix([ [3, 1],
              [2, 1],
              [1, 0]])
print("m3:\n", m3)
print("TRANSPOZYCJA  m1\n",transpose(m1))
print("SUMA m1+m2:\n",m1+m2)
print("ILOCZYN m1*m3:\n",m1*m3)