def sieve_primes(n):
    is_prime = [True] * (n + 1)
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for multiple in range(i * i, n + 1, i):
                is_prime[multiple] = False
    primes = [p for p in range(2, n + 1) if is_prime[p]]
    return primes