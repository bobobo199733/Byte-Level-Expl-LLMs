def sieve_primes(n):
    primes = [True] * (n + 1)
    primes[0], primes[1] = (False, False)
    for i in range(2, int(n ** 0.5) + 1):
        if primes[i]:
            for multiple in range(i * i, n + 1, i):
                primes[multiple] = False
    return [num for num in range(2, len(primes)) if primes[num]]