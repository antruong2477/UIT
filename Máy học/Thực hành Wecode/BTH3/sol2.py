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
        return l
    else:
        return -1

n = int(sys.stdin.readline())
a = ((list(map(int, sys.stdin.readline().strip().split()))))
m = int(sys.stdin.readline())
b = list(map(int, sys.stdin.readline().split()))

for target in b:
    idx = binary_search(a, target)
    if idx != -1:
        print(idx)
    else:
        print(-1)
        
