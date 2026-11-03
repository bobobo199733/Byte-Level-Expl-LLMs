def sieve_primes(n):
    primes = []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            primes.append(i)
            for multiple in range(i * i, n + 1, i):
                sieve[multiple] = False
    for i in range(int(n ** 0.5) + 1, n + 1):
        if sieve[i]:
            primes.append(i)
    return primes