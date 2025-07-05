import random

m,n = 100,80

print(m,n)
print(*sorted([random.randint(0,1000000000) for i in range(m)]))
print(*[random.randint(0,1000000000) for i in range(n)])
