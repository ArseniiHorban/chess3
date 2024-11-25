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