from Esercizi_2set.Es3_1 import *

def even(n):
    return n%2 == 0


def decryptionexp(n, d, e):
    r,_m = numberDecomposition(e*d -1)
    it = 0
    while True:
        it = it + 1
        x = random.randint(1, n-1)
        if math.gcd(x, n) != 1:
            return x, it
        v = expMod(x, _m, n)
        if v == 1:
            continue
        while v != 1:
            v0, v = v, expMod(v, 2, n)
        if v0 != -1 and v0 != n-1:
            return math.gcd(v0 + 1, n), it


def TestAttack(size):
    mu = 0
    t = 0
    ot = 0
    xtime = []
    for i in range(size):
        # genero le kpub e kpriv , quindi n,d,e
        kpub, kpriv = RSA(1024, False)  # kpub = [e,n] , kpriv = [d,n]
        n, d, e = kpub[1], kpriv[0], kpub[0]

        start_time = timeit.default_timer()
        _, nIter = decryptionexp(n, d, e)
        time = (timeit.default_timer() - start_time)
        mu = mu + nIter
        t = t + time
        xtime.append(time)
    mu = mu / size # numero medio di iterazioni
    t = t / size # tempo medio di esecuzione
    for i in xtime:
        ot = ot + (i - t) ** 2
    ot = ot / size # varianza
    return (mu, t, ot)


if __name__ == '__main__':
    print(TestAttack(100))