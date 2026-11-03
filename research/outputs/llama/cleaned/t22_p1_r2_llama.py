def sieve_primes(n):
    """
    Returns a list of all prime numbers less than or equal to n.

    :param n: An integer representing the upper bound for the prime numbers.
    :return: A list of prime numbers less than or equal to n.
    """
    if not isinstance(n, int) or n < 2:
        raise ValueError('n must be a positive integer')
    prime = [True] * (n + 1)
    prime[0] = prime[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if prime[p]:
            for i in range(p * p, n + 1, p):
                prime[i] = False
    return [p for p in range(2, n + 1) if prime[p]]