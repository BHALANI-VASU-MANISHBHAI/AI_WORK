#include <iostream>
#include <vector>
#include <limits>

using namespace std;

const int COMP = +1;  // AI maximizing player
const int HUMAN = -1; // Human minimizing player

vector<vector<int>> board(3, vector<int>(3, 0));

void render() {
    cout << "\n---------------\n";
    for (auto &row : board) {
        for (auto &cell : row) {
            char symbol = (cell == HUMAN) ? 'O' : (cell == COMP) ? 'X' : ' ';
            cout << "| " << symbol << " |";
        }
        cout << "\n---------------\n";
    }
}

bool wins(vector<vector<int>> &state, int player) {
    for (int i = 0; i < 3; i++) {
        if (state[i][0] == player && state[i][1] == player && state[i][2] == player) return true;
        if (state[0][i] == player && state[1][i] == player && state[2][i] == player) return true;
    }
    if (state[0][0] == player && state[1][1] == player && state[2][2] == player) return true;
    if (state[2][0] == player && state[1][1] == player && state[0][2] == player) return true;
    return false;
}

int evaluate(vector<vector<int>> &state) {
    if (wins(state, COMP)) return +1;  
    if (wins(state, HUMAN)) return -1;
    return 0;
}

vector<pair<int, int>> empty_cells(vector<vector<int>> &state) {
    vector<pair<int, int>> cells;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            if (state[i][j] == 0)
                cells.emplace_back(i, j);
    return cells;
}

int minimax(vector<vector<int>> &state, int depth, int player) {
    if (wins(state, COMP)) return +1;
    if (wins(state, HUMAN)) return -1;
    if (empty_cells(state).empty()) return 0; // Draw

    int best_score = (player == COMP) ? numeric_limits<int>::min() : numeric_limits<int>::max();

    for (auto &cell : empty_cells(state)) {
        int x = cell.first, y = cell.second;
        state[x][y] = player;
        int score = minimax(state, depth - 1, -player);
        state[x][y] = 0;

        if (player == COMP) best_score = max(best_score, score);
        else best_score = min(best_score, score);
    }

    return best_score;
}

void ai_turn() {
    int best_score = numeric_limits<int>::min();
    int best_x = -1, best_y = -1;

    for (auto &cell : empty_cells(board)) {
        int x = cell.first, y = cell.second;
        board[x][y] = COMP;
        int score = minimax(board, empty_cells(board).size(), HUMAN);
        board[x][y] = 0;

        if (score > best_score) {
            best_score = score;
            best_x = x;
            best_y = y;
        }
    }

    board[best_x][best_y] = COMP;
    cout << "AI moves:\n";
    render();
}

void human_turn() {
    int move;
    vector<pair<int, int>> moves = {{0, 0}, {0, 1}, {0, 2}, {1, 0}, {1, 1}, {1, 2}, {2, 0}, {2, 1}, {2, 2}};

    render();
    while (true) {
        cout << "Your turn (O). Enter move (1-9): ";
        cin >> move;
        if (move < 1 || move > 9 || board[moves[move - 1].first][moves[move - 1].second] != 0) {
            cout << "Invalid move. Try again.\n";
        } else {
            board[moves[move - 1].first][moves[move - 1].second] = HUMAN;
            break;
        }
    }
}

int main() {
    cout << "Tic-Tac-Toe\n";
    render();

    while (!empty_cells(board).empty() && !wins(board, HUMAN) && !wins(board, COMP)) {
        ai_turn();
        if (!empty_cells(board).empty() && !wins(board, HUMAN) && !wins(board, COMP)) {
            human_turn();
        }
    }

    if (wins(board, COMP)) cout << "AI Wins!\n";
    else if (wins(board, HUMAN)) cout << "You Win!\n";
    else cout << "It's a Draw!\n";

    return 0;
}
