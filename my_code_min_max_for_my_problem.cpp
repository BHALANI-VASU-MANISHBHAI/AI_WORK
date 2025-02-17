#include <bits/stdc++.h>
using namespace std;

// Player 1 = (0,0)
// Player 2 = (1,1)

int actual_vis[5][5];
vector<vector<int>> grid = {
    {0, 0, 0, 0, 1},
    {0, 1, 0, 0, 3},
    {0, 3, 0, 1, 1},
    {0, 1, 0, 0, 1},
    {3, 0, 0, 0, 3}};

vector<pair<int, int>> reward = {{1, 4}, {2, 1}, {4, 0}, {4, 4}};

bool vis1[5][5];
bool vis2[5][5];

bool is_valid(int i, int j) {
    return (i >= 0 && i < 5 && j >= 0 && j < 5);
}

bool is_all_reward_collected() {
    for (auto r : reward) {
        if (grid[r.first][r.second] == 3) {
            return false;
        }
    }
    return true;
}

int wins(vector<vector<int>> &grid) {
    int player_1_point = 0, player_2_point = 0;

    for (auto r : reward) {
        if (grid[r.first][r.second] == 5) player_1_point++;
        else if (grid[r.first][r.second] == 6) player_2_point++;
    }

    return (player_1_point > player_2_point) ? player_1_point : player_2_point;
}

int dx[] = {0, 0, 1, -1};
int dy[] = {1, -1, 0, 0};

int min_max(int i1, int j1, int i2, int j2, int player, int firstturn) {
    if (is_all_reward_collected()) {
        return wins(grid);
    }

    int bestscore = (firstturn == player) ? INT_MIN : INT_MAX;
    if (player == 1) {
        for (int i = 0; i < 4; i++) {
            int x1 = i1 + dx[i], y1 = j1 + dy[i];

            if (is_valid(x1, y1) && !vis1[x1][y1] && grid[x1][y1] != 1) {
                bool prev_vis[5][5];
                memcpy(prev_vis, vis2, sizeof(vis2));

                vis1[x1][y1] = true;
                if (grid[x1][y1] == 3) grid[x1][y1] = 5;

                int score = min_max(x1, y1, i2, j2, 2, firstturn);

                memcpy(vis1, prev_vis, sizeof(vis1));
                if (grid[x1][y1] == 5) grid[x1][y1] = 3;
                vis1[x1][y1] = false;

                bestscore = (firstturn == player) ? max(bestscore, score) : min(bestscore, score);
            }
        }
        return bestscore;
    } else {
        for (int i = 0; i < 4; i++) {
            int x2 = i2 + dx[i], y2 = j2 + dy[i];

            if (is_valid(x2, y2) && !vis2[x2][y2] && grid[x2][y2] != 1) {
                bool prev_vis[5][5];
                memcpy(prev_vis, vis1, sizeof(vis1));

                vis2[x2][y2] = true;
                if (grid[x2][y2] == 3) grid[x2][y2] = 6;

                int score = min_max(i1, j1, x2, y2, 1, firstturn);

                memcpy(vis2, prev_vis, sizeof(vis2));
                if (grid[x2][y2] == 6) grid[x2][y2] = 3;
                vis2[x2][y2] = false;

                bestscore = (firstturn == player) ? max(bestscore, score) : min(bestscore, score);
            }
        }
        return bestscore;
    }
}

int main() {
    memset(vis1, false, sizeof(vis1));
    memset(vis2, false, sizeof(vis2));
    memset(actual_vis, false, sizeof(actual_vis));

    pair<int, int> p1 = {0, 0};  
    pair<int, int> p2 = {1, 1};  

    vis1[p1.first][p1.second] = true;
    vis2[p2.first][p2.second] = true;

    int score = min_max(p1.first, p1.second, p2.first, p2.second, 1, 1);
    cout << score << endl;
    return 0;
}
