
from position_evaluator import PositionEvaluator

class ChessBotDFS:
    def __init__(self, depth):
        self.depth = depth  # Максимальная глубина поиска
        self.evaluator = PositionEvaluator()  # Оценщик позиции
        self.nodes_explored = 0  # Счетчик просмотренных узлов

    def get_best_move(self, board):
        """
        Получает лучший ход с использованием поиска в глубину (DFS).
        """
        best_move = None
        best_value = float('-inf')
        alpha, beta = float('-inf'), float('inf')  # Значения для отсечения

        # Перебираем все легальные ходы
        for move in board.legal_moves:
            board.push(move)  # Делаем ход
            board_value = self.minimax(board, self.depth - 1, alpha, beta, False)
            board.pop()  # Возвращаем позицию назад

            # Если ход лучше текущего лучшего
            if board_value > best_value:
                best_value = board_value
                best_move = move

        print(f"Nodes explored (DFS): {self.nodes_explored}")
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Алгоритм Минимакс с отсечениями альфа-бета.
        """
        self.nodes_explored += 1  # Увеличиваем счетчик

        # Если достигли максимальной глубины или игра окончена
        if depth == 0 or board.is_game_over():
            return self.evaluator.evaluate(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:  # Отсечение
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                # Штраф за избегание взятий, если ход полезный
                if board.is_capture(move) and eval > 0:
                    eval -= 0.5
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:  # Отсечение
                    break
            return min_eval