def createGrid(m,n):
    return [["#" if (x == 1 and i in [1, 2, 3, 4]) or (x in [2, 3] and i == 4) else [] for i in range(n)] for x in range(m)]

def printGrid(grid):
    for row in grid:
        print(row)

def calculateCost(start, end):
    north = start[0] - end[0]
    east = end[1] - start[1]
    return (north * 1) + (east * 2)

def gbfs(grid, start, end):
    costDict = {}
    m = len(grid)
    n = len(grid[0])
    stop = False
    count = 0
    queue = [start]
    while queue:
        pos = queue.pop()
        row = pos[0]
        col = pos[1]
        if grid[row][col] == []:
            grid[row][col] = count
            count += 1
        west = [row, col - 1]
        north = [row -1, col]
        east = [row, col + 1]
        south = [row + 1, col]
        directions = [west, north, east, south]
        for direction in directions:
            if direction == end:
                stop = True
            i = direction[0]
            j = direction[1]
            if i < 0 or i >= m:
                continue
            elif j >= n or j < 0:
                continue
            elif grid[i][j] == '#':
                continue
            else:
                if grid[i][j] == []:
                    cost = calculateCost(direction, end)
                    if cost in costDict:
                        costDict[cost].append(direction)
                    else:
                        costDict[cost] = [direction]
                    grid[i][j] = (count,cost)
                    count += 1
        if stop:
            break
        minCost = min(costDict.keys())
        queue.append(costDict[minCost].pop(0))
        if costDict[minCost] == []:
            del costDict[minCost]

    return grid

grid = createGrid(6,6)
start = [3,2]
end = [0,5]
printGrid(grid)
grid = gbfs(grid, start, end)
print()
print()
printGrid(grid)
