def create_grid(a, b):
    # Creates the structure of the grid
    grid = [["##" if (x == 1 and i in [1, 2, 3, 4]) or
                    (x in [2, 3, 4] and i == 4) or (x in [2, 3] and i == 1) or
                (x == 4 and i == 3) else 0 for i in range(a)] for x in range(b)]

    grid[0][5] = 100
    return grid


def show(grid):
    for row in grid:
        print(row)
    print()
    print()


def reward(a):
    if a == "N":
        cost = -1
    if a == "W":
        cost = -2
    if a == "E":
        cost = -2
    if a == "S":
        cost = -3
    if a == "pie":
        cost = 0
    return cost


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


def calculate_cost(maze, action, dir_1, dir_2, dir_3):
    cost = 0
    cost += reward(action)
    cost += 0.8 * check_maze(dir_1, maze)
    cost += 0.1 * check_maze(dir_2, maze)
    cost += 0.1 * check_maze(dir_3, maze)
    return round(cost, 2)


def policy_improvement(maze, u, dir_1, dir_2, dir_3):
    cost = 0
    cost += 0.8 * check_maze(dir_1, maze) * u
    cost += 0.1 * check_maze(dir_2, maze) * u
    cost += 0.1 * check_maze(dir_3, maze) * u
    return round(cost, 2)


def find_max(sums):
    result = []
    max = sums[0][0]
    for sum in sums:
        if sum[0] >= max:
            max = sum[0]
            result = sum
    return result


def utility(maze, state):
    sums = []

    row = state[0]
    col = state[1]

    west = [row, col - 1, "W"]
    north = [row - 1, col, "N"]
    east = [row, col + 1, "E"]
    south = [row + 1, col, "S"]

    directions = [north, south, east, west]

    for direction in directions:
        action = direction[2]
        if action == 'N':
            util = calculate_cost(maze, action, north, east, west)
            sums.append([util, "^^"])

        elif action == 'S':
            util = calculate_cost(maze, action, south, east, west)
            sums.append([util, "VV"])

        elif action == 'E':
            util = calculate_cost(maze, action, east, north, south)
            sums.append([util, ">>"])

        elif action == 'W':
            util = calculate_cost(maze, action, west, north, south)
            sums.append([util, "<<"])

    return find_max(sums)


def policy_eval(maze, state, a, gamma):
    row = state[0]
    col = state[1]

    west = [row, col - 1]
    north = [row - 1, col]
    east = [row, col + 1]
    south = [row + 1, col]

    u_s = utility(maze, state)

    pie_N = policy_improvement(maze, u_s[0], north, east, west)
    pie_S = policy_improvement(maze, u_s[0], south, east, west)
    pie_E = policy_improvement(maze, u_s[0], east, north, south)
    pie_W = policy_improvement(maze, u_s[0], west, north, south)
    pol_list = pie_N + pie_S + pie_E + pie_W

    pie = pol_list

    if a == 'N':
        updated_utlity = reward(a) + gamma * pie * u_s[0]
        return [round(updated_utlity, 2), '^^']

    if a == 'S':
        updated_utlity = reward(a) + gamma * pie * u_s[0]
        return [round(updated_utlity, 2), 'VV']

    if a == 'E':
        updated_utlity = reward(a) + gamma * pie * u_s[0]
        return [round(updated_utlity, 2), '>>']

    if a == 'W':
        updated_utlity = reward(a) + gamma * pie * u_s[0]
        return [round(updated_utlity, 2), '<<']


def value_iter():
    maze = create_grid(6, 6)
    rows = len(maze)
    columns = len(maze[0])
    end = maze[0][5]

    util_maze = maze
    arrow_maze = create_grid(6, 6)

    for i in range(rows):
        for j in range(columns):
            if maze[i][j] == '##':
                continue
            elif maze[i][j] == end:
                continue

            results = utility(maze, (i, j))
            util_maze[i][j] = results[0]
            arrow_maze[i][j] = results[1]

    arrow_maze[0][5] = 'GG'
    arrow_maze[0][0] = 'SS'

    return [util_maze, arrow_maze]


def policy_iter():
    best_policy = value_iter()[1]
    rows = len(best_policy)
    columns = len(best_policy)
    policy_maze = create_grid(6, 6)
    goal = policy_maze[0][5]

    for i in range(rows):
        for j in range(columns):
            if policy_maze[i][j] == '##':
                continue
            elif policy_maze[i][j] == goal:
                continue
            elif best_policy[i][j] == '^^':
                results = policy_eval(policy_maze, (i, j), 'N', 0.1)
            elif best_policy[i][j] == 'VV':
                results = policy_eval(policy_maze, (i, j), 'S', 0.1)
            elif best_policy[i][j] == '>>':
                results = policy_eval(policy_maze, (i, j), 'E', 0.1)
            elif best_policy[i][j] == '<<':
                results = policy_eval(policy_maze, (i, j), 'W', 0.1)
            else:
                continue

            policy_maze[i][j] = results[0]

    best_policy[0][5] = 'GG'
    best_policy[0][0] = 'SS'

    return [policy_maze, best_policy]


if __name__ == '__main__':
    value_iteration_grid = value_iter()
    policy_iteration_grid = policy_iter()

    print("\nYesha Lester")
    print("CIS 479")
    print("Project 2")
    print("Time: 5:18pm\n")

    for grid in value_iteration_grid:
        print("Value Iteration Grids")
        show(grid)

    for maze in policy_iteration_grid:
        print("Policy Iteration Grids")
        show(maze)
