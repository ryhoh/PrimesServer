import math


# [2, end) の区間内の素数をリストに詰める
# 10^7 より大きいendに対してはValueError
def eratosthenes(end: int) -> list:
    if end > 10000000:
        raise ValueError

    primes = []

    if end < 2:
        return primes

    if end < 9:
        for prime in [2, 3, 5, 7]:
            if prime < end:
                primes.append(prime)
        return primes

    closed = [False for _ in range(end)]
    limit = int(math.sqrt(end))

    for i in range(2, limit + 1):
        if not closed[i]:
            primes.append(i)
            for j in range(i, end, i):
                closed[j] = True

    for i in range(limit + 1, end):
        if not closed[i]:
            primes.append(i)

    return primes


def generate_primes_str(end: int) -> str:
    primes_str = list(map(str, eratosthenes(end)))

    if len(primes_str) == 0:
        return "None"
    else:
        return " ".join(primes_str)
