import random

n,m = 7,6

print(n)
print(*sorted([random.randint(-n,n) for i in range(n)]))
print(m)
print(*[random.randint(-n,n) for i in range(m)])
