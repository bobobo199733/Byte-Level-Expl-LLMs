def sieve_primes(n):
    prime = [True] * (n + 1)
    p = 2
    while p ** 2 <= n:
        if prime[p]:
            for i in range(p ** 2, n + 1, p):
                prime[i] = False
        p += 1
    primes = [str(x) for x in prime[:n + 1] if x]
    return primes