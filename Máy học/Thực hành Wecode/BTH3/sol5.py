
import sys

def print_(arr_min, arr_max):
    return f"{arr_min} {arr_max}\n"
    
def find_closest_numbers(arr, k, x):
    left = 0
    right = len(arr) - k
    while left < right:
        mid = (left + right) // 2
        if x - arr[mid] > arr[mid + k] - x:
            left = mid + 1
        else:
            right = mid
    return arr[left], arr[left + k - 1]

n = int(sys.stdin.readline())
arr = list(map(int, sys.stdin.readline().split()))
result = []

while True:
    line = sys.stdin.readline().strip()
    if not line:
        break
    k, x = map(int, line.split())
    result.append(find_closest_numbers(arr, k, x))
result_strings = [print_(arr_min, arr_max) for arr_min, arr_max in result]
sys.stdout.writelines(result_strings)
