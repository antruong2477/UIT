def clockwise(a, n, e, w, s):
  if(n==s and w==e): return
  elif(n==s):
    temp = a[s][e]
    for i in range(e, w, -1):
      a[s][i] = a[s][i-1]
    a[s][w] = temp
  elif(w==e):
    temp = a[s][e]
    for i in range(s, n, -1):
      a[i][e]=a[i-1][e]
    a[n][e] = temp
  else:
    temp = a[n][e]
    for i in range(e-1, w-1, -1):
      a[n][i+1] = a[n][i]
    for i in range(n+1, s+1):
      a[i-1][w] = a[i][w]
    for i in range(w+1, e+1):
      a[s][i-1] = a[s][i]
    for i in range(s-1, n, -1):
      a[i+1][e] = a[i][e]
    a[n+1][e] = temp

def anticlockwise(a, n, e, w, s):
  if(n==s and w==e): return
  elif(n==s):
    temp = a[s][w]
    for i in range(w+1, e+1):
      a[s][i-1] = a[s][i]
    a[s][e] = temp
  elif(w==e):
    temp = a[n][e]
    for i in range(n+1, s+1):
      a[i-1][e]=a[i][e]
    a[s][e] = temp
  else:
    temp = a[n][w]
    for i in range(w+1, e+1):
      a[n][i-1] = a[n][i]
    for i in range(n+1, s+1):
      a[i-1][e] = a[i][e]
    for i in range(e-1, w-1, -1):
      a[s][i+1] = a[s][i]
    for i in range(s-1, n, -1):
      a[i+1][w] = a[i][w]
    a[n+1][w] = temp

def solve():
  r, c = map(int, input().split())
  a = [[0]*c for _ in range(r)]
  for i in range(r):
    a[i] = list(map(int, input().split()))

  l = int((min(r, c)+1)/2)
  for i in range(l):
    if(i%2==0): clockwise(a, i, c-1-i, i, r-1-i)
    else: anticlockwise(a, i, c-1-i, i, r-1-i)

  for row in a:
    print(" ".join(map(str, row)))

solve()
