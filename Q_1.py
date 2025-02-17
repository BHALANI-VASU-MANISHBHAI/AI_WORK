import random

def is_valid(i, j, matrix, n):
    return 0 <= i < n and 0 <= j < n and matrix[i][j] != 1

def clear_visited(visited, n):
    for i in range(n):
        for j in range(n):
            visited[i][j] = 0

def generate_random():
    loop = random.randint(0, 3)
    for _ in range(loop):
        random_index = random.randint(0, 3)
        dx[0], dx[random_index] = dx[random_index], dx[0]
        dy[0], dy[random_index] = dy[random_index], dy[0]

def dfs(i, j, visited, matrix, reward, move, n):
    global move_a
    
    if reward == 4:
        move_a = move
        return True
    
    visited[i][j] = 1
    
    for k in range(4):
        x, y = i + dx[k], j + dy[k]
        
        if is_valid(x, y, matrix, n) and not visited[x][y]:
            new_reward = reward
            if matrix[x][y] == 3:
                new_reward += 1
                clear_visited(visited, n)
            
            if dfs(x, y, visited, matrix, new_reward, move + 1, n):
                return True
            
            visited[x][y] = 0
    
    return False

# Initialize matrix
grid = [
    [0, 0, 0, 0, 1],
    [0, 1, 0, 0, 3],
    [0, 3, 0, 1, 1],
    [0, 1, 0, 0, 1],
    [3, 0, 0, 0, 3]
]

n = len(grid)
dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

random.seed()

start_points = [(0, 0), (4, 3)]
a_win, b_win = 0, 0

with open("out_advsearch.txt", "w") as f:
    for _ in range(10):
        visited = [[0] * n for _ in range(n)]
        player_moves = {}
        
        for i, (x, y) in enumerate(start_points):
            player = chr(65 + i)  # 'A' or 'B'
            move_a = 0
            
            if dfs(x, y, visited, grid, 0, 0, n):
                f.write(f"Player {player} Moves: {move_a}\n")
                player_moves[player] = move_a
        
        generate_random()
        
        if player_moves['A'] < player_moves['B']:
            f.write("Player A wins\n")
            a_win += 1
        elif player_moves['A'] > player_moves['B']:
            f.write("Player B wins\n")
            b_win += 1
        else:
            f.write("Match Draw\n")

    if a_win > b_win:
        f.write("Player A wins the series\n")
    elif a_win < b_win:
        f.write("Player B wins the series\n")
    else:
        f.write("Series Draw\n")
