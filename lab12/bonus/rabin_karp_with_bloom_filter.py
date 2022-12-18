#skonczone
import math
import time

with open("lotr.txt", encoding='utf-8') as f:
    text = f.readlines()

S = ' '.join(text).lower()
d = 256
q = 101  # liczba pierwsza


def hash(word, q):
    hw = 0
    for i in range(len(word)):  # N - to długość wzorca
        hw = (hw * d + ord(word[i])) % q  #
    return hw


def rolling_hash(last_hash, l_rem, l_add, d, h, q):
    return (d * (last_hash - ord(l_rem) * h) + ord(l_add)) % q


def is_prime(num):
    prime_flag = 0
    if num > 1:
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                prime_flag = 1
                break
        if prime_flag == 0:
            return True
        else:
            return False
    else:
        return False


def get_q_lst(k, maxim):
    q_lst = []
    if not maxim % 2:
        maxim -= 1
    while len(q_lst) != k and maxim > 1:
        if is_prime(maxim):
            q_lst.append(maxim)
        maxim -= 2
    return q_lst

def RabinKarpSet(S: str, subs, P = 0.001):
    #q_list = [233, 239, 241, 251, 257, 263, 269, 271, 277]
    n = len(subs)
    d = 256
    b = math.floor(-n * math.log(P) / (math.log(2)) ** 2)
    k = math.floor(b / n * math.log(2))
    found = []
    q_list = get_q_lst(k, b)#[233, 239, 241, 251, 257, 263, 269, 271, 277]
    M = len(S)
    N = len(subs[0])
    bloom_arr = [False for i in range(b)]
    subs_ind = []
    h_lst = [1 for i in range(len(q_list))]
    h = 1
    mismatched = []
    for j in range(len(q_list)):
        for i in range(N - 1):  # N - jak wyżej - długość wzorca
            h_lst[j] = (h_lst[j] * d) % q_list[j]

    for i in range(len(subs)):
        for q in q_list:
            subs_ind.append(hash(subs[i], q))
    for ind in subs_ind:
        bloom_arr[ind] = True

    hs_lst = []
    for q in q_list:
        hs_lst.append(hash(S[0:N], q))

    for m in range(1, M - N + 1):
        ii = 0
        while ii < len(hs_lst):
            if bloom_arr[hs_lst[ii]] is False:
                break
            ii += 1

        if ii == len(hs_lst):
            if S[m - 1:m + N - 1] in subs:
                found.append(m - 1)
            else:
                mismatched.append(m - 1)

        for i in range(len(q_list)):
            hs_lst[i] = rolling_hash(hs_lst[i], S[m - 1], S[m + N - 1], d, h_lst[i], q_list[i])
            #hs_lst[i] = hash(S[m :m +N], q_list[i])
    return found, mismatched


def print_str(S: str):
    s1 = ""
    s2 = ""
    for i in range(len(S)):
        s2 += S[i] + math.floor(math.log10(i + 1)) * " " + " "
        s1 += str(i) + " "
    print(s1 + '\n' + s2)


# my_string = "arka dupa marka szynka pawel hermes opata deszcz myszka rurka murek cycki taras "
# print_str(my_string)
# my_subs = ["marka", "pawel", "opata", "rurka", "murek", "cycki", "taras"]
# print(RabinKarpSet(my_string, my_subs))
subs = ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred', 'hobbits', 'however', 'popular',
        'nothing', 'enjoyed', 'stuffed', 'relaxed', 'himself3', 'present', 'deliver', 'welcome', 'baggins', 'further']
t_start = time.perf_counter()
found, mismatched = RabinKarpSet(S, subs, P= 0.01)
print(len(found), len(mismatched))
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

t_start = time.perf_counter()
found, mismatched = RabinKarpSet(S, subs, P= 0.001)
print(len(found), len(mismatched))
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))


t_start = time.perf_counter()
found, mismatched = RabinKarpSet(S, subs, P = 0.00001)
print(len(found), len(mismatched))
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))
print("\n\n10 elementów --------------------")
subs = ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred', 'hobbits', 'however', 'popular']
        #'nothing', 'enjoyed', 'stuffed', 'relaxed', 'himself3', 'present', 'deliver', 'welcome', 'baggins', 'further']

found, mismatched = RabinKarpSet(S, subs, P= 0.01)
print(len(found), len(mismatched))
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

t_start = time.perf_counter()
found, mismatched = RabinKarpSet(S, subs, P= 0.001)
print(len(found), len(mismatched))
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))


t_start = time.perf_counter()
found, mismatched = RabinKarpSet(S, subs, P = 0.00001)
print(len(found), len(mismatched))
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

print("\n\npojedynczy element --------------------")
subs = ['gandalf']
        #'nothing', 'enjoyed', 'stuffed', 'relaxed', 'himself3', 'present', 'deliver', 'welcome', 'baggins', 'further']

found, mismatched = RabinKarpSet(S, subs, P= 0.01)
print(len(found), len(mismatched))
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

t_start = time.perf_counter()
found, mismatched = RabinKarpSet(S, subs, P= 0.001)
print(len(found), len(mismatched))
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

t_start = time.perf_counter()
found, mismatched = RabinKarpSet(S, subs, P= 0.00001)
print(len(found), len(mismatched))
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))


### mimo dużych zmian szukanych wzorców czas nie zmienia się znacznie, a długośc algorytmu zależy silnie od P,
### gdy jest ono za małe lub za duże powoduje to zwiększenie czasu wykonywania