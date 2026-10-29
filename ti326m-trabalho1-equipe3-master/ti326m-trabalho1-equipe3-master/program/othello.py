import math

import time

W = 'W'
B = 'B'
EMPTY = None


class Othello:
    
    def __init__(self):

        self.board = [
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, W,     B,     EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, B,     W,     EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
        ]
        self._current_player = B
    
    def _opponent(self, player):
        return B if player == W else W
        
    def play_turn(self, action):
        # updates the board and switches the player after a move is made
            
        if action is None:
            # pass turn if no valid moves
            self._current_player = self._opponent(self._current_player)
            return
        
        # validates action and updates the board
        self.board = self.result(self.board, action, self._current_player)
        self._current_player = self._opponent(self._current_player)
    
    def player(self):
        '''
            returns player who has the next turn on a board
        '''
        return self._current_player
    
    def actions(self, board, player = None):
        ''''
            returns set of all possible actions avaiable on the board
        '''
        if player is None:
            player = self._current_player
        
        actions = set()
        opponent = self._opponent(player)
        
        directions = [
            (-1, 0), (1, 0),
            (0, -1), (0, 1),
            (-1, -1), (-1, 1),
            (1, -1), (1, 1)
        ]
        
        for row in range(8):
            for col in range(8):
                if board[row][col] is not EMPTY:
                    continue
                
                for d_row, d_col in directions:
                    r, c = row + d_row, col + d_col
                    found_opponent = False
                    
                    while 0 <= r < 8 and 0 <= c < 8:
                        if board[r][c] == opponent:
                            found_opponent = True
                        elif board[r][c] == player:
                            if found_opponent:
                                actions.add((row, col))
                            break
                        else:
                            break
                        
                        r += d_row
                        c += d_col
        
        return actions
    
    def result(self, board, action, player):
        
        '''
            returns the board that results from making a move on the board
        '''
        
        # validates action
        if action not in self.actions(board, player):
            raise ValueError(f"Invalid action for player {player}: {action}\nValid actions are: {self.actions(board, player)}")
        
        row, col = action
        opponent = self._opponent(player)
        
        directions = [
            (-1, 0), (1, 0),
            (0, -1), (0, 1),
            (-1, -1), (-1, 1),
            (1, -1), (1, 1)
        ]
        
        new_board = [r[:] for r in board]
        new_board[row][col] = player
        
        for d_row, d_col in directions:
            r, c = row + d_row, col + d_col
            to_flip = []
            
            while 0 <= r < 8 and 0 <= c < 8:
                if new_board[r][c] == opponent:
                    to_flip.append((r, c))
                elif new_board[r][c] == player:
                    for f_row, f_col in to_flip:
                        new_board[f_row][f_col] = player
                    break
                else:
                    break
                
                r += d_row
                c += d_col
        
        return new_board
    
    def terminal(self, board):
        '''
            returns True if game is over, False otherwise
        '''
        
        count = 0
        for row in board:
            for square in row:
                if square == EMPTY:
                    count +=1
        
        # if count == 0, all the squares will be occupied
        if count == 0:
            return True
        
        if not self.actions(board, B) and not self.actions(board, W):
            return True
        
        return False
    
    def utility(self, board):
        '''
            returns 1 if B has won the game, -1 if W has won, 0 otherwise
        '''
        
        # returns who won the game -> 1 for B, -1 for W, 0 for a draw
        if self.terminal(board):
            count_w = 0
            count_b = 0
            for row in board:
                for square in row:
                    if square == W:
                        count_w += 1
                    if square == B:
                        count_b += 1
            if count_w > count_b:
                return -1
            if count_w < count_b:
                return 1
            return 0
        raise ValueError("Game is not over yet")

class Minimax:

    def __init__(self, game, heuristic, time_limit = 3.0, use_pruning = True):

        self.game = game
        self.heuristic = heuristic
        self.time_limit = time_limit
        self.use_pruning = use_pruning
        self.nodes_expanded = 0
        self.start_time = 0.0

    def run(self, state, depth=4, alpha=-math.inf, beta=math.inf):
        self.start_time = time.time()
        self.nodes_expanded = 0
        
        current_player = self.game.player()
        
        # prevents returning the opponent's action if the current player has no valid actions
        if not self.game.actions(state, current_player):
            return None, self.heuristic(state, current_player)
        
        # saves best action and value found so far to return if the time runs out while the seartch has not ended
        best_action = None
        best_value = self.heuristic(state, current_player)
        
        # iterative deepening -> increasing depth
        for current_depth in range(1, depth + 1):
            if time.time() - self.start_time > self.time_limit:
                break
            
            value, action = self._run(state, current_player, current_depth, alpha, beta)
             
            # updates the best action and value if the search has 
            # not ended yet and the time limit has not been exceeded
            if time.time() - self.start_time <= self.time_limit and action is not None:
                best_value = value
                best_action = action
        

        return best_action, best_value
    
    def _run(self, state, current_player, depth, alpha, beta):
        self.nodes_expanded += 1
        
        # base cases
        
        # time limit exceeded
        if time.time() - self.start_time > self.time_limit:
            return self.heuristic(state,current_player), None
        
        # game is over
        if self.game.terminal(state):
            return self.game.utility(state), None
        
        # has reached maximum depth
        if depth == 0:
            return self.heuristic(state,current_player), None
        
        actions = self.game.actions(state, current_player)
        
        if not actions:
            # no valid moves -> pass turn
            # does not reduce depth
            return self._run(state, self.game._opponent(current_player), depth, alpha, beta)
        
        if current_player == B:
            best_value = -math.inf
            best_action = None
            
            for action in actions:
                # gets the child state from this action
                child_state = self.game.result(state, action, current_player)
                # runs search
                child_value, _ = self._run(child_state, self.game._opponent(current_player), depth - 1, alpha, beta)
                
                # updates best value and action if a better one is found
                if child_value > best_value:
                    best_value = child_value
                    best_action = action
                
                # uses alpha-beta pruning to cut off branches that wouldnt 
                # influence the final outcome to reduce the number of nodes expanded
                if self.use_pruning:
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        break
            
            return best_value, best_action
        
        else:
            best_value = math.inf
            best_action = None
            
            for action in actions:
                child_state = self.game.result(state, action, current_player)
                child_value, _ = self._run(child_state, self.game._opponent(current_player), depth - 1, alpha, beta)
                
                if child_value < best_value:
                    best_value = child_value
                    best_action = action
                
                if self.use_pruning:
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        break
            
            return best_value, best_action
