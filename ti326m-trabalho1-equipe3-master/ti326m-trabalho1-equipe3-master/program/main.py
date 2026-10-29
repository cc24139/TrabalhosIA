import os
import random
import time

from othello import Minimax, Othello

othelloGame = Othello()

# Define if player is human or computer
playerB = None
playerW = None

# track time and nodes for each player
time1 = 0
time2 = 0
nodes1 = 0
nodes2 = 0

# saves minimax instances and depths for each computer player
miniMaxB, miniMaxW = None, None
depthB, depthW = None, None

# tracks some metrics for the games
winners = []
times = []
timeNodes1 = []
timeNodes2 = []
NodesExpanded1 = []
NodesExpanded2 = []
game_results = []


# ------------------------------------------------------------------------------
# Heuristic functions
# ------------------------------------------------------------------------------
def heuristicOfCorners(board, player):
    """
    Return a score based on the corners of the board, the more corners the better,
    and if the corner is empty but adjacent to a piece of the player it is bad,
    and if it is adjacent to an opponent's piece it is good
    """
    opponent = "W" if player == "B" else "B"
    corners = {
        (0, 0): [(0, 1), (1, 0), (1, 1)],
        (0, 7): [(0, 6), (1, 7), (1, 6)],
        (7, 0): [(6, 0), (7, 1), (6, 1)],
        (7, 7): [(6, 7), (7, 6), (6, 6)],
    }

    score = 0
    for corner, adjacent in corners.items():
        cornerValue = board[corner[0]][corner[1]]
        if cornerValue == player:
            score += 5
        elif cornerValue == opponent:
            score -= 5
        else:
            for adj in adjacent:
                if board[adj[0]][adj[1]] == player:
                    score -= 3
                elif board[adj[0]][adj[1]] == opponent:
                    score += 3
    return score


def heuristicOfPossibleMoves(board, player):
    """
    Return the difference of possible moves for the current player and the opponent,
    the more possible moves the better
    """
    opponent = "W" if player == "B" else "B"
    return len(othelloGame.actions(board, player)) - len(
        othelloGame.actions(board, opponent)
    )


def heuristicOfPieceCount(board, player):
    """
    Return the difference in piece count between the current player and the opponent,
    the more pieces the better
    """
    opponent = "W" if player == "B" else "B"
    playerCount = sum(row.count(player) for row in board)
    opponentCount = sum(row.count(opponent) for row in board)
    return playerCount - opponentCount


def heuristicOfCombination(board, player):
    """
    Return the combination of the other 3 heuristics, each with different weights
    """
    return (
        heuristicOfCorners(board, player) * 0.5
        + heuristicOfPossibleMoves(board, player) * 0.3
        + heuristicOfPieceCount(board, player) * 0.2
    )

# ------------------------------------------------------------------------------

def print_table(headers, rows):
    
    col_widths = [len(str(h)) for h in headers]

    for row in rows:
        for i, item in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(item)))

    def format_row(row):
        return (
            "| "
            + " | ".join(f"{str(item):^{col_widths[i]}}" for i, item in enumerate(row))
            + " |"
        )

    separator = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"

    print(separator)
    print(format_row(headers))
    print(separator)
    for row in rows:
        print(format_row(row))
    print(separator)


def print_results_table(results):
    headers = ["Game", "Winner", "B Score", "W Score", "Time (s)", "Nodes B", "Nodes W"]

    rows = []
    for r in results:
        rows.append(
            [
                r["game"],
                r["winner"],
                r["scoreB"],
                r["scoreW"],
                f"{r['time']:.2f}",
                r["nodesB"],
                r["nodesW"],
            ]
        )

    print_table(headers, rows)
    
# prints results for each game and tracks metrics for summary after all games are done
def scoreboard(startTime):
    global time1, time2, nodes1, nodes2
    global winners, times, game_results
    global timeNodes1, timeNodes2, NodesExpanded1, NodesExpanded2

    finalTime = time.time()
    timeGame = finalTime - startTime
    times.append(timeGame)

    scoreB = sum(row.count("B") for row in othelloGame.board)
    scoreW = sum(row.count("W") for row in othelloGame.board)

    winner = othelloGame.utility(othelloGame.board)
    winner_char = "B" if winner == 1 else "W" if winner == -1 else "E"
    winners.append(winner_char)

    game_results.append(
        {
            "game": len(game_results) + 1,
            "scoreB": scoreB,
            "scoreW": scoreW,
            "winner": winner_char,
            "time": timeGame,
            "nodesB": nodes1,
            "nodesW": nodes2,
        }
    )

    timeNodes1.append((time1 * 1000, nodes1))
    timeNodes2.append((time2 * 1000, nodes2))
    NodesExpanded1.append(nodes1)
    NodesExpanded2.append(nodes2)

    # reset per-game counters
    time1 = 0
    time2 = 0
    nodes1 = 0
    nodes2 = 0

# displays the current board state
def ShowBoard(board):
    print("    " + " ".join(f"{col:^3}" for col in range(8)))
    print("   +" + "---+" * 8)

    for i, row in enumerate(board):
        cells = [(cell if cell is not None else " ") for cell in row]
        print(f" {i} |" + "|".join(f"{str(cell):^3}" for cell in cells) + "|")
        print("   +" + "---+" * 8)

# allows user to select game mode and configures computer players
def SelectOptions():
    global playerB, playerW

    print("Select an option:")
    print("1. Player vs Computer")
    print("2. Computer vs Computer")
    print("3. Exit")

    choice = input("Enter your choice: ")
    while choice <= "0" or choice > "3":
        print("Invalid choice. Please select a valid option.")
        choice = input("Enter your choice: ")

    match choice:
        case "1":
            playerB = "P"
            playerW = "C"
        case "2":
            playerB = "C"
            playerW = "C"
        case "3":
            exit()

# handles ther games flow
def play():
    player = othelloGame.player()
    print(f"Player {player}'s turn.")

    if player == "B":
        if playerB == "C":
            playComputer()
        else:
            playPlayer()
    else:
        if playerW == "C":
            playComputer()
        else:
            playPlayer()


def playComputer():
    global nodes1, nodes2, time1, time2
    global miniMaxB, miniMaxW, depthB, depthW

    player = othelloGame.player()

    if player == "B":
        move_start = time.time()
        action, _ = miniMaxB.run(othelloGame.board, depth=depthB)
        move_elapsed = time.time() - move_start

        nodes1 += miniMaxB.nodes_expanded
        time1 += move_elapsed
        othelloGame.play_turn(action)

    else:
        move_start = time.time()
        action, _ = miniMaxW.run(othelloGame.board, depth=depthW)
        move_elapsed = time.time() - move_start

        nodes2 += miniMaxW.nodes_expanded
        time2 += move_elapsed
        othelloGame.play_turn(action)


def playPlayer():
    actions = sorted(othelloGame.actions(othelloGame.board))
    col_width = 10
    boardschematic = [row[:] for row in othelloGame.board]

    if not actions:
        print("No valid moves available. Skipping turn.")
        othelloGame.play_turn(None)
        return

    numPlay = 1
    for i in actions:
        row = i[0]
        col = i[1]
        boardschematic[row][col] = str(numPlay)
        numPlay += 1

    ShowBoard(boardschematic)
    print("".join(f"{i + 1:^{col_width}}" for i in range(len(actions))))
    print("".join(f"{str(action):^{col_width}}" for action in actions))

    numChoice = int(input("Select an action: ")) - 1
    while numChoice < 0 or numChoice >= len(actions):
        print("Invalid choice. Please select a valid action.")
        numChoice = int(input("Select an action: ")) - 1

    othelloGame.play_turn(actions[numChoice])

# configures the minimax instances for a computer player based on user input for heuristics, pruning, time limits, and depth limits
def SelectMiniMax(player_color):
    print(f"\n--- Configuring Computer ({player_color}) ---")
    UsePruning = input("Use alpha-beta pruning? (y/n): ").lower() == "y"
    time_lim = input(
        "Select time limit for the computer's move (in seconds) -> default is 3: "
    )
    depth_lim = input(
        "Select maximum iterative deepening depth (e.g., 3, 5, 10) -> default is 4: "
    )

    if time_lim.strip() == "":
        time_lim = 3
    else:
        time_lim = int(time_lim)

    if depth_lim.strip() == "":
        depth_lim = 4
    else:
        depth_lim = int(depth_lim)

    print("Select heuristic for the computer:")
    print("1. Corners")
    print("2. Possible Moves")
    print("3. Piece Count")
    print("4. Combination")

    choice = input("Enter your choice (1-4): ")
    if choice == "1":
        heuristic = heuristicOfCorners
    elif choice == "2":
        heuristic = heuristicOfPossibleMoves
    elif choice == "3":
        heuristic = heuristicOfPieceCount
    else:
        heuristic = heuristicOfCombination

    return (
        Minimax(
            othelloGame, heuristic, use_pruning=UsePruning, time_limit=time_lim
        ),
        depth_lim
    )

# plays the games and shows results and summaries after all games are done
def start():
    global miniMaxB, miniMaxW, depthB, depthW

    os.system("cls" if os.name == "nt" else "clear")
    print("Welcome to Othello!")
    SelectOptions()

    games_input = input("\nHow many games would you like to play? (default is 1): ")
    if games_input.strip() == "":
        num_games = 1
    else:
        num_games = int(games_input)

    # Configure each active computer player
    if playerB == "C":
        miniMaxB, depthB = SelectMiniMax("Black - Player B")
    if playerW == "C":
        miniMaxW, depthW = SelectMiniMax("White - Player W")

    for i in range(num_games):
        print(f"\nStarting game {i + 1}/{num_games}...")
        startTimer = time.time()

        while not othelloGame.terminal(othelloGame.board):
            play()
            ShowBoard(othelloGame.board)

        scoreboard(startTimer)
        othelloGame.__init__()


    # prints results and overviews
    print(f"\n--- Results of {num_games} Game(s) ---")
    print_results_table(game_results)

    summary_headers = ["Metric", "Value"]
    summary_rows = [
        ["Black (B) Wins", winners.count("B")],
        ["White (W) Wins", winners.count("W")],
        ["Draws", winners.count("E")],
        [
            "Average time per game (s)",
            f"{sum(times) / len(times):.2f}" if times else "-",
        ],
        [
            "Average nodes expanded for player B",
            f"{sum(NodesExpanded1) / len(NodesExpanded1):.2f}"
            if NodesExpanded1
            else "-",
        ],
        [
            "Average nodes expanded for player W",
            f"{sum(NodesExpanded2) / len(NodesExpanded2):.2f}"
            if NodesExpanded2
            else "-",
        ],
        [
            "Max time for player B (ms)",
            f"{max(timeNodes1[i][0] for i in range(len(timeNodes1))):.2f}"
            if timeNodes1
            else "-",
        ],
        [
            "Max time for player W (ms)",
            f"{max(timeNodes2[i][0] for i in range(len(timeNodes2))):.2f}"
            if timeNodes2
            else "-",
        ],
        [
            "Max nodes expanded for player B",
            f"{max(NodesExpanded1):.2f}" if NodesExpanded1 else "-",
        ],
        [
            "Max nodes expanded for player W",
            f"{max(NodesExpanded2):.2f}" if NodesExpanded2 else "-",
        ],
    ]

    print("\n--- Summary ---")
    print_table(summary_headers, summary_rows)


if __name__ == "__main__":
    start()