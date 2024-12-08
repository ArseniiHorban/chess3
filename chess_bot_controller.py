<<<<<<< HEAD
from chess_bot_dfs import ChessBotDFS
from chess_bot_bfs import ChessBotBFS
from chess_bot_ucs import ChessBotUCS

class ChessBotController:
    def __init__(self, dfs_depth=30, bfs_depth=10, ucs_depth=10):
        # Инициализация ботов для каждого алгоритма
        self.dfs_bot = ChessBotDFS(dfs_depth)
        self.bfs_bot = ChessBotBFS(bfs_depth)
        self.ucs_bot = ChessBotUCS(ucs_depth)

    def choose_bot(self, board):
        """
        Выбор бота в зависимости от стадии игры.
        """
        legal_moves_count = sum(1 for _ in board.legal_moves)

        if board.fullmove_number <= 10:  # Первые 10 ходов
            print("Используем DFS для начала игры.")
            return self.dfs_bot
        elif 11 <= board.fullmove_number <= 30:  # Средние ходы
            print("Используем BFS для средней стадии игры.")
            return self.bfs_bot
        else:  # Эндшпиль
            print("Используем UCS для сложных ситуаций.")
            return self.ucs_bot

    def get_best_move(self, board):
        """
        Получение лучшего хода от выбранного бота.
        """
        chosen_bot = self.choose_bot(board)
=======
from chess_bot_dfs import ChessBotDFS
from chess_bot_bfs import ChessBotBFS
from chess_bot_ucs import ChessBotUCS
from position_evaluator import PositionEvaluator

class ChessBotController:
    def __init__(self, dfs_depth, bfs_depth, ucs_depth):
        # Создаем один экземпляр PositionEvaluator
        self.position_evaluator = PositionEvaluator()  
        
        # Передаем его в каждый бот
        self.dfs_bot = ChessBotDFS(dfs_depth, self.position_evaluator)
        self.bfs_bot = ChessBotBFS(bfs_depth, self.position_evaluator)
        self.ucs_bot = ChessBotUCS(ucs_depth, self.position_evaluator)

    def choose_bot(self, board):
        """
        Выбор бота в зависимости от стадии игры.
        """
        piece_count = sum(1 for square in board.piece_map().values())
        moves_count = sum(1 for _ in board.legal_moves)

        if piece_count > 24 and moves_count < 1000000:  # Первые 30 ходов (временно заменено на отладочное значение)
            print("Используем DFS для начала игры.")
            return self.dfs_bot
        elif 10 <= piece_count <= 24 and moves_count <50:  # Средние ходы
            print("Используем BFS для средней стадии игры.")
            return self.bfs_bot
        else:  
            print("Используем UCS для сложных ситуаций.") # Эндшпиль
            return self.ucs_bot

    def get_best_move(self, board):
        """
        Получение лучшего хода от выбранного бота.
        """
        chosen_bot = self.choose_bot(board)
>>>>>>> 01c5b21 (better DFS, still barely working UCS and better position evaluation)
        return chosen_bot.get_best_move(board)