<<<<<<< HEAD
import chess

class PositionEvaluator:
    def __init__(self):
        self.piece_values = {
            chess.PAWN: 2,
            chess.KNIGHT: 6,
            chess.BISHOP: 6.5,
            chess.ROOK: 10,
            chess.QUEEN: 18,
            chess.KING: 1000
        }
        self.center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]

    def evaluate(self, board):
        """
        Главный метод оценки позиции.
        """
        score = 0
        score += self.material_score(board)
        score += self.center_control_score(board)
        score += self.king_safety_score(board)
        score += self.piece_activity_score(board)
        score += self.pawn_structure_score(board)
        score += self.doubled_pawns_score(board)
        score += self.isolated_pawns_score(board)
        return score

    def material_score(self, board):
        material_score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    material_score += self.piece_values[piece.piece_type]
                else:
                    material_score -= self.piece_values[piece.piece_type]
        return material_score

    def center_control_score(self, board):
        center_score = 0
        for square in self.center_squares:
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    center_score += 0.5
                else:
                    center_score -= 0.5
        return center_score

    def king_safety_score(self, board):
        safety_score = 0
        for color in [chess.WHITE, chess.BLACK]:
            king_square = board.king(color)
            if king_square:
                king_attack_zone = board.attacks(king_square)
                pawn_shield = sum(
                    1 for square in king_attack_zone
                    if board.piece_at(square) and board.piece_at(square).piece_type == chess.PAWN and board.piece_at(square).color == color
                )
                under_attack = any(board.is_attacked_by(not color, square) for square in king_attack_zone)

                if color == chess.WHITE:
                    safety_score += pawn_shield * 0.5
                    if under_attack:
                        safety_score -= 2
                else:
                    safety_score -= pawn_shield * 0.5
                    if under_attack:
                        safety_score += 2
        return safety_score

    def piece_activity_score(self, board):
        activity_score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                mobility = len(list(board.attacks(square)))
                if piece.color == chess.WHITE:
                    activity_score += mobility * 0.1
                else:
                    activity_score -= mobility * 0.1
        return activity_score

    def pawn_structure_score(self, board):
        structure_score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                if piece.color == chess.WHITE:
                    if board.is_attacked_by(chess.WHITE, square):
                        structure_score += 0.2
                else:
                    if board.is_attacked_by(chess.BLACK, square):
                        structure_score -= 0.2
        return structure_score

    def doubled_pawns_score(self, board):
        doubled_pawns = 0
        for file in range(8):
            white_pawns = 0
            black_pawns = 0
            for rank in range(8):
                square = chess.square(file, rank)
                piece = board.piece_at(square)
                if piece and piece.piece_type == chess.PAWN:
                    if piece.color == chess.WHITE:
                        white_pawns += 1
                    else:
                        black_pawns += 1
            if white_pawns > 1:
                doubled_pawns -= (white_pawns - 1) * 0.2
            if black_pawns > 1:
                doubled_pawns += (black_pawns - 1) * 0.2
        return doubled_pawns

    def isolated_pawns_score(self, board):
        isolated_pawns = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                file = chess.square_file(square)
                neighbors = [file - 1, file + 1]
                has_support = any(
                    0 <= n <= 7 and board.pieces(chess.PAWN, piece.color) & chess.BB_FILES[n]
                    for n in neighbors
                )
                if not has_support:
                    if piece.color == chess.WHITE:
                        isolated_pawns -= 0.3
                    else:
                        isolated_pawns += 0.3
        return isolated_pawns
=======
import chess

class PositionEvaluator:
    def __init__(self):
        # Стоимость фигур
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3.5,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0 #оценка короля не имеет смысла, тут забрать короля нельзя, можно только поставить мат, а этим занимается king_safety
        }

        # Центральные клетки
        self.center_squares = [chess.E4, chess.D4, chess.E5, chess.D5]
        self.wider_center = [
            chess.C3, chess.D3, chess.E3, chess.F3,
            chess.C4, chess.F4,
            chess.C5, chess.F5,
            chess.C6, chess.D6, chess.E6, chess.F6
        ]

    def evaluate(self, board):
        """
        общая оценка позиции
        """
        score = 0
        score += self.material_balance(board) * 4
        score += self.center_control(board) * 3
        score += self.pawn_structure(board) * 2
        score += self.king_safety(board) * 5
        score += self.piece_activity(board) * 1
        score += self.threats(board) * 3
        return score

    def material_balance(self, board):
        """
        Оценка разницы в материале.
        """
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = self.piece_values.get(piece.piece_type, 0)
                if piece.color == chess.WHITE:
                    score -= value
                elif piece.color == chess.BLACK:
                    score += value
        return score

    def center_control(self, board):
        """
        Оценка контроля центра
        """
        score = 0
        for square in self.center_squares:
            piece = board.piece_at(square)
            if piece:
                score += 0.5 if piece.color == chess.BLACK else -0.5

        for square in self.wider_center:
            piece = board.piece_at(square)
            if piece:
                score += 0.25 if piece.color == chess.BLACK else -0.25

        return score

    def pawn_structure(self, board):
        """
        Оценка структуры пешек: изолированные, удвоенные
        """
        score = 0
        pawns = list(board.pieces(chess.PAWN, chess.BLACK)) + list(board.pieces(chess.PAWN, chess.WHITE))
        pawn_files = {file: [] for file in range(8)}

        for square in pawns:
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            pawn_files[file].append(rank)

        for file, ranks in pawn_files.items():
            if len(ranks) > 1:
                score -= 0.5  # Удвоенные пешки
            if len(ranks) == 1:
                neighbors = [file - 1, file + 1]
                if not any(neighbor in pawn_files and pawn_files[neighbor] for neighbor in neighbors):
                    score -= 0.5  # Изолированные пешки

        return score

    def king_safety(self, board):
        score = 0
        """
        Оценка безопасности короля (МНОГА ОЧКОВ ЗА МАТ)
        """

        """
        простая оценка безопасности (устаревшее)
        if black_king_square in [chess.G8, chess.C8]:
            score += 1
        if white_king_square in [chess.G1, chess.C1]:
            score -= 1
        if board.is_checkmate() and board.turn == chess.WHITE:
            score += 1000  # Черные выигрывают, если белый король в мате
        """

        if board.is_checkmate() and board.turn == chess.WHITE:
            score += 10000  #накидываем боту очки за мат белым, шоб было к чему стремится
        elif board.is_checkmate() and board.turn == chess.BLACK:
            score -= 10000 
        return score

    def piece_activity(self, board):
        """
        Оценка активности фигур: количество доступных ходов
        """
        score = 0
        for move in board.legal_moves:
            if board.color_at(move.from_square) == chess.BLACK:
                score += 0.1
            else:
                score -= 0.1
        return score

    def threats(self, board):
        """
        Оценка угроз: атакуемые фигуры противника
        """
        score = 0
        for square in chess.SQUARES:
            attackers = board.attackers(chess.BLACK, square)
            piece = board.piece_at(square)
            if piece and piece.color == chess.WHITE:
                score += len(attackers) * self.piece_values.get(piece.piece_type, 0)

            attackers = board.attackers(chess.WHITE, square)
            piece = board.piece_at(square)
            if piece and piece.color == chess.BLACK:
                score -= len(attackers) * self.piece_values.get(piece.piece_type, 0)

        return score
>>>>>>> 01c5b21 (better DFS, still barely working UCS and better position evaluation)
