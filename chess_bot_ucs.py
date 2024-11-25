import chess
import heapq
from position_evaluator import PositionEvaluator

class ChessBotUCS:
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.evaluator = PositionEvaluator()

    def get_best_move(self, board):
        priority_queue = []
        heapq.heappush(priority_queue, (0, board.copy(), None, 0))
        best_move = None

        while priority_queue:
            current_cost, current_board, first_move, depth = heapq.heappop(priority_queue)

            if depth >= self.max_depth or current_board.is_game_over():
                return first_move

            for move in current_board.legal_moves:
                current_board.push(move)
                move_cost = self.evaluator.evaluate(current_board)
                heapq.heappush(priority_queue, (current_cost + move_cost, current_board.copy(), move if depth == 0 else first_move, depth + 1))
                current_board.pop()

        return best_move