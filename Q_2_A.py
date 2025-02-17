import sys

grid = [
    [0, 0, 0, 0, 1],
    [0, 1, 0, 0, 3],
    [0, 3, 0, 1, 1],
    [0, 1, 0, 0, 1],
    [3, 0, 0, 0, 3]
]

n = 5
a_reward = 0
b_reward = 0
total_reward = 4

dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

visited1 = [[False] * n for _ in range(n)]
visited2 = [[False] * n for _ in range(n)]

def is_valid(x, y):
    return 0 <= x < n and 0 <= y < n

def clear_visited(player):
    if player == 1:
        for i in range(n):
            for j in range(n):
                visited1[i][j] = False
    else:
        for i in range(n):
            for j in range(n):
                visited2[i][j] = False

def base_case():
    if a_reward > b_reward:
        return 1
    elif a_reward < b_reward:
        return -1
    else:
        return 0

def minimax(i1, j1, i2, j2, is_max):
    global a_reward, b_reward, total_reward
    
    if total_reward == 0:
        return base_case()
    
    if is_max:
        max_val = -sys.maxsize
        for k in range(4):
            x, y = i1 + dx[k], j1 + dy[k]
            if is_valid(x, y) and not visited1[x][y] and grid[x][y] != 1:
                visited1[x][y] = True
                flag = False
                if grid[x][y] == 3:
                    a_reward += 1
                    grid[x][y] = 0
                    total_reward -= 1
                    flag = True
                max_val = max(max_val, minimax(x, y, i2, j2, False))
                visited1[x][y] = False
                
                if flag:
                    grid[x][y] = 3
                    a_reward -= 1
                    total_reward += 1
        return max_val
    else:
        min_val = sys.maxsize
        for k in range(4):
            x, y = i2 + dx[k], j2 + dy[k]
            if is_valid(x, y) and not visited2[x][y] and grid[x][y] != 1:
                visited2[x][y] = True
                flag = False
                if grid[x][y] == 3:
                    b_reward += 1
                    grid[x][y] = 0
                    total_reward -= 1
                    flag = True
                min_val = min(min_val, minimax(i1, j1, x, y, True))
                visited2[x][y] = False
                
                if flag:
                    grid[x][y] = 3
                    b_reward -= 1
                    total_reward += 1
        return min_val

clear_visited(1)
clear_visited(2)

ans = minimax(0, 0, 4, 3, True)

if ans == 1:
    print("Player A wins")
elif ans == -1:
    print("Player B wins")
else:
    print("Draw")
