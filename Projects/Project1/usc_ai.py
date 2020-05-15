def createGrid(m,n):
    return [["#" if (x == 1 and i in [1, 2, 3, 4]) or (x in [2, 3] and i == 4) else [] for i in range(n)] for x in range(m)]

def printGrid(grid):
    for row in grid:
        print(row)

def calculateCost(minCost, dir):
    if dir == "N":
        minCost += 1
    if dir == "W":
        minCost += 2
    if dir == "E":
        minCost += 2
    if dir == "S":
        minCost += 3
    return minCost

def ucs(grid, start, end):
    costDict = {}
    m = len(grid)
    n = len(grid[0])
    stop = False
    count = 1
    minCost = 0
    grid[start[0]][start[1]] = 0
    queue = [start]
    while queue:
        pos = queue.pop(0)
        row = pos[0]
        col = pos[1]
        west = [row, col - 1]
        north = [row -1, col]
        east = [row, col + 1]
        south = [row + 1, col]
        directions = [[west, "W"], [north,"N"], [east,"E"], [south,"S"]]
        for direction in directions:
            if direction[0] == end:
                stop = True
            i = direction[0][0]
            j = direction[0][1]
            if i < 0 or i >= m:
                continue
            elif j >= n or j < 0:
                continue
            elif grid[i][j] == '#':
                continue
            else:
                if grid[i][j] == []:
                    cost = calculateCost(minCost, direction[1])
                    if cost in costDict:
                        costDict[cost].append(direction[0])
                    else:
                        costDict[cost] = [direction[0]]
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
grid = ucs(grid, start, end)
print()
print()
printGrid(grid)
