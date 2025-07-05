import sys 
import heapq

def solve(arr,operations):
    heap = []
    for num in arr:
        heapq.heappush(heap, -num)

    for op in operations:
        #Xóa số lớn nhất
        if op[0] == -1:
            heapq.heappop(heap)
        #Xóa tất cả số lớn nhất
        elif op[0] == -2:
            max_val = heap[0]
            while heap and heap[0] == max_val:
                heapq.heappop(heap)
        #Giảm đi giá trị số lớn nhất trong mảng một lượng 
        elif op[0] == -3:
            max_val = heap[0]
            idx = heap.index(max_val)
            heap[idx] += op[1]
            heapq.heapify(heap)
        #Giảm đi giá trị của tất cả số lớn nhất trong mảng một lượng
        elif op[0] == -4:
            max_val = heap[0]
            for i in range(len(heap)):
                if heap[i] == max_val:
                    heap[i] += op[1]
                else:
                    break
            heapq.heapify(heap)
    return [-x for x in heap]

n, m = map(int, sys.stdin.readline().split())
arr = [int(sys.stdin.readline()) for _ in range(n)]
operations = [list(map(int, sys.stdin.readline().split())) for _ in range(m)]

result = sorted(solve(arr, operations), reverse = True)

for num in result:
    print(num)
