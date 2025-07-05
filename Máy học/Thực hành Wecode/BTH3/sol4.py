import sys

def find_closest_elements(arr, k, x):
    left = 0
    right = len(arr) - k
    
    while left < right:
        mid = (left + right) // 2
        if x - arr[mid] > arr[mid + k] - x:
            left = mid + 1
        else:
            right = mid
    
    return arr[left:left + k]

n = int(sys.stdin.readline())
a = ((list(map(int, sys.stdin.readline().strip().split()))))
k, x = map(int, sys.stdin.readline().strip().split())


# if x >= a[-1]:
    # for i in range(k):
        # ans.append(a[n-i-1])
# elif x <= a[0]:
    # for i in range(k):
        # ans.append(a[i])
# else:
    # idx = binary_search(a,x)
# 
result = find_closest_elements(a, k, x)

# In kết quả
for num in result:
    print(num, end=" ")
