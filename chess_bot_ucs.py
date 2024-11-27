<<<<<<< HEAD
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

=======
import heapq
import chess

class ChessBotUCS:
    def __init__(self, depth, evaluator):
        self.max_depth = depth
        self.evaluator = evaluator
        self.nodes_explored = 0

    def get_best_move(self, board):
        priority_queue = []
        # Начальный элемент: (стоимость, FEN строки, первый ход, глубина)
        heapq.heappush(priority_queue, (0, board.fen(), None, 0))
        best_move = None

        while priority_queue:
            current_cost, current_fen, first_move, depth = heapq.heappop(priority_queue)

            current_board = chess.Board(current_fen)  # Восстанавливаем доску из FEN

            if depth >= self.max_depth or current_board.is_game_over():
                return first_move

            for move in current_board.legal_moves:
                current_board.push(move)
                print(f"Текущая доска после хода: {current_board}")

                move_cost = self.evaluator.evaluate(current_board)
                # Добавляем новое состояние доски в очередь в виде FEN строки
                # Преобразуем ход в строку перед добавлением в очередь
                heapq.heappush(priority_queue, (current_cost + move_cost, current_board.fen(), first_move if depth > 0 else move, depth + 1))
                current_board.pop()

>>>>>>> 01c5b21 (better DFS, still barely working UCS and better position evaluation)
        return best_move