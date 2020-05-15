def createGrid(m,n):
    return [["#" if (x == 1 and i in [1, 2, 3, 4]) or (x in [2, 3] and i == 4) else [] for i in range(n)] for x in range(m)]

def printGrid(grid):
    for row in grid:
        print(row)

def bfs(grid, start, end):
    m = len(grid)
    n = len(grid[0])
    count = 0
    queue = [start]
    while queue:
        pos = queue.pop(0)
        row = pos[0]
        col = pos[1]
        west = [row, col - 1]
        north = [row -1, col]
        east = [row, col + 1]
        south = [row + 1, col]
        directions = [west, north, east, south]
        for direction in directions:
            i = direction[0]
            j = direction[1]
            if i < 0 or i >= m:
                continue
            elif j >= n or j < 0:
                continue
            elif grid[i][j] == '#':
                continue
            else:
                queue.append(direction)
        if grid[row][col] == []:
            grid[row][col] = count
            count += 1
        if pos == end:
            break

    return grid

grid = createGrid(6,6)
start = [3,2]
end = [0,5]
printGrid(grid)
grid = bfs(grid, start, end)
print()
print()
printGrid(grid)