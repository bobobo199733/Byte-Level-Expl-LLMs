def sieve_primes(n):
    """
    Finds all prime numbers up to and including n using the Sieve of Eratosthenes algorithm.

    Args:
        n (int): The upper bound for finding primes.

    Returns:
        list: A sorted list of prime numbers.
    """
    if n < 2:
        return []
    prime = [True] * (n + 1)
    prime[0] = prime[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if prime[p]:
            for i in range(p * p, n + 1, p):
                prime[i] = False
    return [p for p in range(2, n + 1) if prime[p]]