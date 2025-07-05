import sys

def binary_search(a, x):
    l = 0
    r = len(a) - 1
    while l < r:
        mid = (l + r) // 2
        if a[mid] < x:
            l = mid + 1
        else:
            r = mid
    if a[l] == x:
        return True
    else:
        return False

m,n = map(int,sys.stdin.readline().split())
a = ((list(map(int, sys.stdin.readline().strip().split()))))
b = list(map(int, sys.stdin.readline().split()))
cnt = 0
for target in b:
    if binary_search(a, target):
        cnt += 1

print(cnt)
        
