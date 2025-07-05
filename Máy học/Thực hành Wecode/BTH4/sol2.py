import sys
import heapq

arr = []
heap = []
        
while True:
    line = sys.stdin.readline().strip()
    if line == '0':
        break
    a,b = map(int, line.split())
    arr.append([a,b])


for a,b in arr:
    if a == 1 and b not in heap:
        heapq.heappush(heap, b)
    else:
        if b in heap:
            print(heap.index(b)+1)
        else:
            print(0)
            
