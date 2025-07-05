import random 

n,m = 100,100
print(n,m)
for _ in range(n):
    print(*[random.randint(-n*10,n*10) for i in range(n)])
