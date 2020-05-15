import random
import operator

def create_grid(a, b):
    # Creates the structure of the grid
    invalid  =
    grid = [[{"N": "####","S": "####","E": "####","W": "####"} if (x == 1 and i in [1, 2, 3, 4]) or
                    (x in [2, 3] and i == 4) else {"N" :[0,0], "S" :[0,0], "W" :[0,0], "E" :[0,0]}  for i in range(a)] for x in range(b)]

    grid[0][5] = {"N": [50,1],"S": [50,1],"E": [50,1],"W": [50,1]}
    return grid

def showMaze(grid):
    for row in grid:
        print(row)
    print()
    print()


def findReward(a):
    reward = 0
    if a == "N":
        reward = -1
    if a == "W":
        reward = -2
    if a == "E":
        reward = -2
    if a == "S":
        reward = -3
    return reward

def calculateAplha(value):
    alpha = 1 / (value + 1)
    return alpha

def calculateCost(currentCost, action, access, nextCost):
    reward = findReward(action)
    alpha = calculateAplha(access)
    gamma = 1
    cost = currentCost + alpha * (reward + (gamma * nextCost) - currentCost)
    return round(cost, 2)

def updateAccess(value):
    return value + 1

def selectRandonDirection():
    actions = ["N", "S", "E", "W"]
    action = random.choice(actions)
    return action

def findMaxKey(dictionary):
    return max(dictionary.items(), key=operator.itemgetter(1))[0]

def sarsa(grid, start, end):
    m = len(grid)
    n = len(grid[0])
    queue = [start]
    while queue:
        currPos = queue.pop()
        if currPos == end:
            break
        row = currPos[0]
        col = currPos[1]
        west = [row, col - 1]
        north = [row -1, col]
        east = [row, col + 1]
        south = [row + 1, col]
        action = selectRandonDirection()
        if action == "N":
            nextPos = north
        if action == "S":
            nextPos = south
        if action == "W":
            nextPos = west
        if action == "E":
            nextPos = east
        currCell = grid[row][col]
        currState = currCell[action]
        currCost = currState[0]
        currState[1] = updateAccess(currState[1])
        currStateAccess = currState[1]

        i = nextPos[0]
        j = nextPos[1]
        if i < 0 or i >= m:
            nextPos = currPos
        elif j >= n or j < 0:
            nextPos = currPos
        elif grid[i][j] == {"N": "####","S": "####","E": "####","W": "####"}:
            nextPos = currPos

        row = nextPos[0]
        col = nextPos[1]

        nextCell = grid[row][col]
        nextState = nextCell[action]
        nextCost = nextState[0]
        currState[0] = calculateCost(currCost, action, currStateAccess, nextCost)
        queue.append(nextPos)

    return grid


def qlearning(grid, start, end):
    m = len(grid)
    n = len(grid[0])
    queue = [start]
    while queue:
        currPos = queue.pop()
        if currPos == end:
            break
        row = currPos[0]
        col = currPos[1]
        west = [row, col - 1]
        north = [row -1, col]
        east = [row, col + 1]
        south = [row + 1, col]
        action = selectRandonDirection()
        if action == "N":
            nextPos = north
        if action == "S":
            nextPos = south
        if action == "W":
            nextPos = west
        if action == "E":
            nextPos = east
        currCell = grid[row][col]
        currState = currCell[action]
        currCost = currState[0]
        currState[1] = updateAccess(currState[1])
        currStateAccess = currState[1]

        i = nextPos[0]
        j = nextPos[1]
        if i < 0 or i >= m:
            nextPos = currPos
        elif j >= n or j < 0:
            nextPos = currPos
        elif grid[i][j] == {"N": "####","S": "####","E": "####","W": "####"}:
            nextPos = currPos

        row = nextPos[0]
        col = nextPos[1]

        nextCell = grid[row][col]
        maxDirection = findMaxKey(nextCell)
        nextState = nextCell[maxDirection]
        nextCost = nextState[0]
        currState[0] = calculateCost(currCost, action, currStateAccess, nextCost)
        queue.append(nextPos)

    return grid


def showDirectiongrid(grid):
    for i in range(len(grid)):
        north = []
        west_east = []
        south = []
        for j in range(len(grid[i])):
            cell = grid[i][j]
            if cell == {"N": "####","S": "####","E": "####","W": "####"}:
                north.append("####")
                west_east.append("#### ####")
                south.append("####")
            north.append("    " + str(cell["N"][0]) + "     ")
            west_east.append(str(cell["W"][0]) + " " + str(cell["E"][0]))
            south.append("   " + str(cell["S"][0]) + "    ")

        northStr = "  ".join(north)
        west_eastStr = "      ".join(west_east)
        southStr = "    ".join(south)
        print(northStr)
        print(west_eastStr)
        print(southStr)
        print()
    print()
    print()

def check_maze(position, maze):
    i = position[0]
    j = position[1]

    if i < 0 or i >= len(maze):
        return 0
    elif j >= len(maze[0]) or j < 0:
        return 0
    elif maze[i][j] == '##':
        return 0
    else:
        return maze[i][j]

def createArrowGrid(grid):
    rows = len(grid)
    columns = len(grid[0])
    for i in range(rows):
        for j in range(columns):
            cell = grid[i][j]
            if cell == {"N": "####","S": "####","E": "####","W": "####"}:
                grid[i][j] = "####"
            max_dir = findMaxKey(cell)
            if max_dir == "N":
                grid[i][j] = "^^"
            if max_dir == "S":
                grid[i][j] = "vv"
            if max_dir =="E":
                grid[i][j] = ">>"
            if max_dir == "W":
                grid[i][j] = "<<"
    return grid



if __name__ == '__main__':
    grid = create_grid(6,6)
    start = [3,2]
    end = [0,5]
    for i in range(100):
       grid = sarsa(grid, start, end)

    showDirectiongrid(grid)
    maze = createArrowGrid(grid)
    showMaze(maze)

    newgrid = create_grid(6,6)
    for i in range(300):
        newgrid = qlearning(newgrid, start, end)

    showDirectiongrid(newgrid)
    newmaze = createArrowGrid(newgrid)
    showMaze(newmaze)

    # value_iteration_grid = value_iter()
    # policy_iteration_grid = policy_iter()
    #
    # print("\nYesha Lester")
    # print("CIS 479")
    # print("Project 2")
    # print("Time: 5:18pm\n")

    # for grid in value_iteration_grid:
    #     print("Value Iteration Grids")
    #     show(grid)
    #
    # for maze in policy_iteration_grid:
    #     print("Policy Iteration Grids")
    #     show(maze)
