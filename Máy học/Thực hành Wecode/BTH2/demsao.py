def solve(grid):
    star = 0
    n = len(grid)
    m = len(grid[0])
    vis = [[0] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '-' and vis[i][j] == 0:
                star += 1
                DFS(grid, vis, n, m, i, j)
    return star

def DFS(grid, vis, n, m, row, col):
    delRow=[1, -1, 0, 0]
    delCol= [0, 0, -1, 1]
    if row < 0 or row >= n or col < 0 or col >= m or vis[row][col] == 1:
        return
    vis[row][col] = 1
    for i in range(4):
        nRow = row + delRow[i]
        nCol = col + delCol[i]

        if 0 <= nRow < n and 0 <= nCol < m and grid[nRow][nCol] == '-' and vis[nRow][nCol] == 0:
            DFS(grid, vis, n, m, nRow, nCol)
for i in range (8):
    m,n=map(int,input().split())
    grid=[]
    for _ in range(m):
        row=list(input())
        grid.append(row)
    result = solve(grid)
    print("Case " + str(i+1) + ": " + str(result))
