import sys
import numpy as np

n = 5
grid = np.array([
    [0, 0, 0, 0, 1],
    [0, 1, 0, 0, 3],
    [0, 3, 0, 1, 1],
    [0, 1, 0, 0, 1],
    [3, 0, 0, 0, 3]
])

visited1 = np.zeros((5, 5), dtype=bool)
visited2 = np.zeros((5, 5), dtype=bool)

dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

def isvalid(x, y):
    return 0 <= x < n and 0 <= y < n

def clear_visited(player):
    if player == 1:
        visited1.fill(False)
    else:
        visited2.fill(False)

a_reward = 0
b_reward = 0
total_reward = 4

def base_case(i1, j1, i2, j2):
    if a_reward > b_reward:
        return 1
    elif a_reward < b_reward:
        return -1
    return 0

def alpha_beta(i1, j1, i2, j2, ismax, alpha, beta):
    global a_reward, b_reward, total_reward
    if total_reward == 0:
        return base_case(i1, j1, i2, j2)
    
    if ismax:
        max_val = -sys.maxsize
        for k in range(4):
            x, y = i1 + dx[k], j1 + dy[k]
            if isvalid(x, y) and not visited1[x, y] and grid[x, y] != 1:
                visited1[x, y] = True
                flag = False
                if grid[x, y] == 3:
                    a_reward += 1
                    grid[x, y] = 0
                    total_reward -= 1
                    flag = True
                max_val = max(max_val, alpha_beta(x, y, i2, j2, False, alpha, beta))
                alpha = max(alpha, max_val)
                visited1[x, y] = False
                if flag:
                    grid[x, y] = 3
                    a_reward -= 1
                    total_reward += 1
                if beta <= alpha:
                    break
        return max_val
    else:
        min_val = sys.maxsize
        for k in range(4):
            x, y = i2 + dx[k], j2 + dy[k]
            if isvalid(x, y) and not visited2[x, y] and grid[x, y] != 1:
                visited2[x, y] = True
                flag = False
                if grid[x, y] == 3:
                    b_reward += 1
                    grid[x, y] = 0
                    total_reward -= 1
                    flag = True
                min_val = min(min_val, alpha_beta(i1, j1, x, y, True, alpha, beta))
                beta = min(beta, min_val)
                visited2[x, y] = False
                if flag:
                    grid[x, y] = 3
                    b_reward -= 1
                    total_reward += 1
                if beta <= alpha:
                    break
        return min_val

if __name__ == "__main__":
    clear_visited(1)
    clear_visited(2)
    
    ans = alpha_beta(0, 0, 4, 3, True, -sys.maxsize, sys.maxsize)

    if ans == 1:
        print("Player A wins")
    elif ans == -1:
        print("Player B wins")
    else:
        print("Draw")
