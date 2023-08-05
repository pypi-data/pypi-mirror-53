def binom(n, k):
    """
    Computes the binomial coefficient using a multiplicative formula.
    Stolen from https://stackoverflow.com/a/46778364/5990435
    """
    assert k >= 0 and k <= n
    if k == 0 or k == n:
        return 1
    b = 1
    for i in range(min(k, n-k)):
        b = b * (n - i) // (i + 1)
    return b
