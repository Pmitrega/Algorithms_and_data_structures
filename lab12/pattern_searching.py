import time

with open("lotr.txt", encoding='utf-8') as f:
    text = f.readlines()

S = ' '.join(text).lower()


def find_naive(S: str, W: str):
    m = 0
    S_len = len(S)
    W_len = len(W)
    found = []
    no_comparison = 0
    while m < S_len - W_len + 1:
        i = 0
        while i < W_len:
            no_comparison += 1
            if not S[m + i] == W[i]:
                break
            i += 1
        if i == W_len:
            found.append(m)
        m += 1

    else:
        return found, no_comparison


def hash(word, d, q):
    hw = 0
    for i in range(len(word)):  # N - to długość wzorca
        hw = (hw * d + ord(word[
                               i])) % q  # dla d będącego potęgą 2 można mnożenie zastąpić shiftem uzyskując pewne przyspieszenie obliczeń
    return hw


def RabinKarp(S: str, W: str):
    M = len(S)
    N = len(W)
    d = 256
    q = 101  # liczba pierwsza
    hW = hash(W, d, q)
    hS = hash(S[0:N], d, q)
    found = []
    h = 1
    for i in range(N - 1):  # N - jak wyżej - długość wzorca
        h = (h * d) % q

    no_comparison = 0
    for m in range(1, M - N + 1):
        hS = (d * (hS - ord(S[m - 1]) * h) + ord(S[m + N - 1])) % q
        if hS < 0: hS += q
        # hS = hash(S[m:m+N],d,q)
        # no_comparison += 1
        if hS == hW:
            j = 0
            while j < N:
                no_comparison += 1
                if S[m + j] != W[j]:
                    break
                j += 1
            if j == N:
                found.append(m)

            # if S[m:m + N] == W:
            #     found.append(m)

    return found, no_comparison


def KMP_table(W: str):
    pos = 1
    cnd = 0
    T = [-1 for i in W]
    T.append(-1)
    while pos < len(W):
        if W[pos] == W[cnd]:
            T[pos] = T[cnd]
        else:
            T[pos] = cnd
            while cnd >= 0 and W[pos] != W[cnd]:
                cnd = T[cnd]
            pos += 1
            cnd += 1
    T[pos] = cnd
    return T


def KMP(S: str, W: str):
    m = 0
    i = 0
    T = KMP_table(W)
    nP = 0
    P = []
    no_comparison = 0
    while m < len(S):
        no_comparison += 1
        if W[i] == S[m]:
            m += 1
            i += 1
            if i == len(W):
                P.append(m - i)
                nP += 1
                if T[i] != -1:
                    i = T[i]
        else:
            i = T[i]
            if i < 0:
                m += 1
                i += 1
    return  P, no_comparison


t_start = time.perf_counter()
found, no_comparison = find_naive(S, "time.")
print(len(found), no_comparison)
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

t_start = time.perf_counter()
found, no_comparison = RabinKarp(S, "time.")
print(len(found), no_comparison)
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))
###W metodzie Rabina Karpa porównujemy znaki defacto tylko w momencie zgodniości kodów.


t_start = time.perf_counter()
found, no_comparison = KMP(S, "time.")
print(len(found), no_comparison)
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))