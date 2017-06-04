def make_primes(n):
    primes = []
    step = 0
    i = 2
    while step < n:
        while not is_primal(i):
            i+=1
        primes.append(i)
        i+=1
        step+=1
    return primes

def is_primal(n):
    if n == 2:
        return True
    if n%2==0:
        return False
    i = 3
    primal = True
    while i*i <= n:
        if n % i == 0:
            primal = False
            break
        i+=2
    return primal
