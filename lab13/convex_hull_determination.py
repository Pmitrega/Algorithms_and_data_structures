#skończone
import copy


def is_left(P1, P2, el):
    return (P2[1] - P1[1]) * (el[0] - P2[0]) - (el[1] - P2[1]) * (P2[0] - P1[0]) < 0


def is_right(P1, P2, el):
    return (P2[1] - P1[1]) * (el[0] - P2[0]) - (el[1] - P2[1]) * (P2[0] - P1[0]) > 0


def is_inline(P1, P2, el):
    return (P2[1] - P1[1]) * (el[0] - P2[0]) - (el[1] - P2[1]) * (P2[0] - P1[0]) == 0


def is_left_for_all(P1, P2, points):
    for el in points:
        if el != P1 and el != P2 and P1 != P2:
            val = (P2[1] - P1[1]) * (el[0] - P2[0]) - (el[1] - P2[1]) * (P2[0] - P1[0])
            if val > 0:
                return False
    return True


def min_lef(points):
    minn_x = 100000000
    p_min = (0, 0)
    for el in points:
        l_min_x = minn_x
        minn_x = min(el[0], minn_x)
        if minn_x != l_min_x:
            p_min = el
        elif minn_x == l_min_x and el[1] < p_min[1]:
            p_min = el

    return p_min


def jarvis(points):
    points = copy.copy(points)
    p = min_lef(points)
    start = p
    path = [p]
    while True:
        n_p = None
        c_q = None
        for q in points:
            if q != p:
                c_q = q
                break

        for i in range(len(points)):
            r = points[i]
            if is_right(p, c_q, r):
                c_q = r
            elif is_inline(p,c_q,r):
                if p[0] < c_q[0] < r[0] or p[0] > c_q[0] > r[0] or p[1] < c_q[1] < r[1] or p[1] > c_q[1] > r[1]:
                    c_q = r
        path.append(c_q)
        p = c_q
        if p == start:
            break
    return path


P1 = [(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)]
P2 = [(0, 3), (0, 1), (0, 0), (3, 0), (3, 3)]
P3 = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]
print(jarvis(P1))
print(jarvis(P2))
print(jarvis(P3))

