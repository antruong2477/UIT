import random

n,m = 100,80

print(n)
print(*sorted([random.randint(-n,n) for i in range(n)]))
print(m)
print(*[random.randint(-n,n) for i in range(m)])
