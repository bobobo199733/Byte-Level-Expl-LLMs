def sieve_primes(n):
    primes = [True] * (n + 1)
    p = 2
    while p ** 2 <= n:
        if primes[p]:
            for i in range(p ** 2, n + 1, p):
                primes[i] = False
        p += 1
    primes[0] = primes[1] = False
    result = [p for p in range(2, len(primes)) if primes[p]]
    return result