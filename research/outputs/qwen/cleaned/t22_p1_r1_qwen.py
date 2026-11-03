def sieve_primes(n):
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0], sieve[1] = (False, False)
    for current in range(2, int(n ** 0.5) + 1):
        if sieve[current]:
            for multiple in range(current * current, n + 1, current):
                sieve[multiple] = False
    return [num for num, is_prime in enumerate(sieve) if is_prime]