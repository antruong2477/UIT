import sys
def print_aligned_array(arr):
    max_lengths = [max(len(str(elem)) for elem in col) for col in zip(*arr)]
    format_str = ' '.join(f'{{:>{length}}}' for length in max_lengths)
    for row in arr:
        print(format_str.format(*row))

r, c = map(int, sys.stdin.readline().split())
arr_ = [list(map(int, sys.stdin.readline().strip().split())) for _ in range(r)]

print_aligned_array(arr_)
