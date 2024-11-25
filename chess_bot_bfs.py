import chess
from collections import deque
from position_evaluator import PositionEvaluator

class ChessBotBFS:
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.evaluator = PositionEvaluator()

    def get_best_move(self, board):
        best_move = None
        best_value = float('-inf')
        queue = deque([(board.copy(), 0, None)])

        while queue:
            current_board, depth, first_move = queue.popleft()

            if depth >= self.max_depth or current_board.is_game_over():
                value = self.evaluator.evaluate(current_board)
                if value > best_value:
                    best_value = value
                    best_move = first_move
                continue

            for move in current_board.legal_moves:
                current_board.push(move)
                queue.append((current_board.copy(), depth + 1, move if depth == 0 else first_move))
                current_board.pop()

        return best_move