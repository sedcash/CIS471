import usc_ai as usc

def createGrid(m, n):
    return [["#" if (x == 1 and i in [1, 2, 3, 4]) or (x in [2, 3] and i == 4) else [] for i in range(n)] for x in range(m)]

def printGrid(grid):
    for row in grid:
        print(row)

def calculateHNCost(start, end):
    north = abs(end[0] - start[0])
    east = abs(end[1] - start[1])
    return (north * 1) + (east * 2)

def calculateTotalCost(costGrid, position, hN):
    row = position[0]
    col = position[1]
    temp = costGrid[row][col][1]
    return  temp + hN

def aStar(grid, costGrid, start, end):
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
        north = [row - 1, col]
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
                    hN = calculateHNCost(direction,end)
                    cost = calculateTotalCost(costGrid, direction, hN)
                    if cost in costDict:
                        costDict[cost].append(direction)
                    else:
                        costDict[cost] = [direction]
                    grid[i][j] = (count, cost)
                    count += 1
        if stop:
            break
        minCost = min(costDict.keys())
        queue.append(costDict[minCost].pop(0))
        if costDict[minCost] == []:
            del costDict[minCost]

    return grid


grid = createGrid(6, 6)
costGrid = createGrid(6,6)
start = [3, 2]
end = [0, 5]
printGrid(grid)
costGrid = usc.ucs(costGrid, start, end)
print()
print()
printGrid(costGrid)
grid = aStar(grid, costGrid, start, end)
print()
print()
printGrid(grid)
