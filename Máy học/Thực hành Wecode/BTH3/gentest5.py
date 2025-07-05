import random

n = 100

print(n)
print(*sorted([random.randint(0,1000000000) for i in range(n)]))

for i in range(50):
        k = random.randint(0,n)
        x = random.randint(0,1000000000)
        print(k,x)
