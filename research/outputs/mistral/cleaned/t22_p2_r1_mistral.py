def sieve_primes(n):
    if n < 2:
        return []
    composite = [True] * (n + 1)
    composite[0], composite[1] = (False, False)
    for i in range(int(n ** 0.5) + 1):
        if composite[i]:
            for multiple in range(i * i, n + 1, i):
                composite[multiple] = False
    primes = [x for x in range(2, len(composite)) if composite[x]]
    return sorted(primes)