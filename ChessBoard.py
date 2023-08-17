import copy

class ChessPiece:
    directions = []  # Default to empty; specific pieces will override this

    def __init__(self, color):
        self.color = color

    def __str__(self):
        return f"{self.color}{self.symbol}"


class Pawn(ChessPiece):
    symbol = 'P'


class Rook(ChessPiece):
    symbol = 'R'
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Horizontal and vertical directions


class Knight(ChessPiece):
    symbol = 'N'
    directions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]


class Bishop(ChessPiece):
    symbol = 'B'
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonal directions


class Queen(ChessPiece):
    symbol = 'Q'
    directions = Rook.directions + Bishop.directions  # Concatenating Rook and Bishop directions


class King(ChessPiece):
    symbol = 'K'
    directions = Queen.directions  # Directly using Queen's directions


class SpecialInfo:
    def __init__(self):
        self.en_passant_target = None  # Position that can be captured en passant
        self.king_moved = {'w': False, 'b': False}
        self.rooks_moved = {'w': {'left': False, 'right': False},
                            'b': {'left': False, 'right': False}}

    def set_king_moved(self, color):
        self.king_moved[color] = True

    def set_rook_moved(self, color, side):
        self.rooks_moved[color][side] = True # Fixed the attribute name

    def set_en_passant(self, position):
        self.en_passant_target = position  # Fixed the attribute name


class Movement:
    def __init__(self, start_pos, end_pos, promotion_result=None, is_castling=False):
        self.start_pos = start_pos  # Starting position as a tuple (row, column)
        self.end_pos = end_pos  # Ending position as a tuple (row, column)
        self.promotion_result = promotion_result  # Resulting ChessPiece if the move is a promotion
        self.is_castling = is_castling  # Boolean flag indicating whether the move is a castling move
        self.is_promotion = promotion_result is not None

    def __str__(self, board):
        piece = board[self.start_pos[0]][self.start_pos[1]]
        move_str = f"Move {piece} from {self.start_pos} to {self.end_pos}"

        if self.is_castling:
            move_str += ", castling move"
        elif self.is_promotion:
            move_str += f", promote to {self.promotion_result}"

        return move_str


class ChessBoard:
    EMPTY_GRID = '..'  # Constant to represent an empty grid
    RANK_IDX = '12345678'
    FILE_IDX = 'abcdefgh'

    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.populate_board()
        self.special_info = SpecialInfo()
        self.current_color = 'w'  # Starting with white's turn

    def opposing_color(color):
        return 'w' if color == 'b' else 'b'

    def is_empty(self, row, col):
        return self.is_within_bounds(row, col) and self.board[row][col] == ChessBoard.EMPTY_GRID

    def is_within_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def populate_board(self):
        # Set up the initial board position with ChessPiece instances
        colors = ['w', 'b']
        for color in colors:
            rank = 0 if color == 'w' else 7
            pawn_rank = 1 if color == 'w' else 6
            self.board[rank] = [Rook(color), Knight(color), Bishop(color), Queen(color), King(color), Bishop(color), Knight(color), Rook(color)]
            self.board[pawn_rank] = [Pawn(color) for _ in range(8)]

    def print_board(self):
        print("   " + "  ".join(ChessBoard.FILE_IDX))
        print("  +" + "--+" * 8)
        for i in range(8):
            row_str = f"{8 - i} |"
            for j in range(8):
                piece = self.board[8 - i - 1][j]
                symbol = str(piece) if piece else ChessBoard.EMPTY_GRID
                row_str += f"{symbol}|"
            print(row_str, f"{8 - i}")
            print("  +" + "--+" * 8)
        print("   " + "  ".join(ChessBoard.FILE_IDX))

    def apply_move(self, move):
        # Create a new ChessBoard object by copying the current state
        new_board = copy.deepcopy(self)

        # Extract the start and end positions from the move
        start_row, start_col = move.start_pos
        end_row, end_col = move.end_pos

        # Get the piece being moved
        moving_piece = new_board.board[start_row][start_col]

        # Move the piece from the start position to the end position
        new_board.board[end_row][end_col] = moving_piece
        new_board.board[start_row][start_col] = ChessBoard.EMPTY_GRID

        # Handle en passant
        if new_board.special_info.en_passant_target == move.end_pos and moving_piece in ['wP', 'bP']:
            # Capture the pawn that moved two squares in the previous turn
            new_board.board[start_row][end_col] = ChessBoard.EMPTY_GRID

        # Update en passant target for the next turn if a pawn moves two squares forward
        new_board.special_info.en_passant_target = None
        if moving_piece in ['wP', 'bP'] and abs(end_row - start_row) == 2:
            new_board.special_info.en_passant_target = ((start_row + end_row) // 2, start_col)

        # Handle castling
        if move.is_castling:
            new_board.perform_castling(start_row, end_col)

        # Handle promotion
        if move.is_promotion:
            new_board.board[end_row][end_col] = move.promotion_result

        return new_board

    def perform_castling(self, start_row, end_col):
        # Determine if it's kingside or queenside based on the end column
        if end_col == 6:  # Kingside
            self.board[start_row][5] = self.board[start_row][7]
            self.board[start_row][7] = ChessBoard.EMPTY_GRID
        elif end_col == 2:  # Queenside
            self.board[start_row][3] = self.board[start_row][0]
            self.board[start_row][0] = ChessBoard.EMPTY_GRID

    def can_castle(self, row, king_col, direction):
        # Check if the king has moved before
        if self.special_info.king_moved[self.current_color]:
            return False

        side = 'right' if direction == 'king' else 'left'
        # Check if the rook has moved before
        if self.special_info.rooks_moved[self.current_color][side]:
            return False

        step = 1 if direction == 'king' else -1
        range_limit = 3 if direction == 'king' else 4

        # Check if the squares between the king and the rook are empty
        for col_offset in range(1, range_limit):
            if self.board[row][king_col + col_offset * step] != ChessBoard.EMPTY_GRID:
                return False

        # Check if the king is in, moves through, or ends up in check
        for col_offset in range(0, range_limit - 1):
            if self.is_square_under_attack(row, king_col + col_offset * step):
                return False

        return True

    def generate_all_simple_moves(self, color):
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    start_pos = (row, col)
                    if isinstance(piece, Pawn):
                        all_moves += self.generate_pawn_moves(row, col, piece)
                    else:
                        all_moves += self.generate_non_pawn_piece_moves(row, col, piece)

        return all_moves

    def generate_pawn_moves(self, row, col, pawn):
        moves = []
        direction = 1 if pawn.color == 'w' else -1
        start_row = 1 if pawn.color == 'w' else 6

        # Function to add a move, handling promotion if necessary
        def add_move(end_row, end_col):
            if end_row in (0, 7):  # Promotion rank
                for promoted_piece in (Queen(pawn.color), Rook(pawn.color), Bishop(pawn.color), Knight(pawn.color)):
                    moves.append(Movement((row, col), (end_row, end_col), promotion_result=promoted_piece))
            else:
                moves.append(Movement((row, col), (end_row, end_col)))

        # Check one step forward
        if self.is_empty(row + direction, col):
            add_move(row + direction, col)

        # Check two steps forward if it's the pawn's first move
        if row == start_row and self.is_empty(row + 2 * direction, col) and self.is_empty(row + direction, col):
            add_move(row + 2 * direction, col)

        # Check captures
        for capture_col in (col - 1, col + 1):
            if self.is_within_bounds(row + direction, capture_col):
                target_piece = self.board[row + direction][capture_col]
                if target_piece and target_piece.color != pawn.color:
                    add_move(row + direction, capture_col)

                # En passant
                if self.special_info.en_passant_target and self.special_info.en_passant_target == (row + direction, capture_col):
                    add_move(row + direction, capture_col)

        return moves

    def generate_non_pawn_piece_moves(self, row, col, piece):
        directions = piece.directions
        moves = []

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            while self.is_within_bounds(new_row, new_col):
                target_piece = self.board[new_row][new_col]

                if self.is_empty(new_row, new_col) or target_piece.color != piece.color:
                    moves.append(Movement((row, col), (new_row, new_col)))

                if not self.is_empty(new_row, new_col) or isinstance(piece, (King, Knight)):
                    break  # Stop sliding if a piece is encountered or if it's a single-step move

                new_row, new_col = new_row + dr, new_col + dc

        return moves

    def can_castle(self, color, side, threat):
        if side not in ['king', 'queen']:
            return False

        # Determine the row based on the color
        row = 7 if color == 'w' else 0

        # Check if the king has moved
        if self.special_info.king_moved[color]:
            return False

        # Check the specific side for castling
        if side == 'king':
            rook_col = 7
            # Check if the king-side rook has moved
            if self.special_info.rooks_moved[color]['right']:
                return False
            # Check that the squares between the king and rook are empty and not threatened
            for col in [5, 6]:
                if self.board[row][col] != ChessBoard.EMPTY_GRID or threat[row][col]:
                    return False
        elif side == 'queen':
            rook_col = 0
            # Check if the queen-side rook has moved
            if self.special_info.rooks_moved[color]['left']:
                return False
            # Check that the squares between the king and rook are empty and not threatened
            for col in [1, 2, 3]:
                if self.board[row][col] != ChessBoard.EMPTY_GRID or threat[row][col]:
                    return False

        return True

    def all_valid_moves(self, color):
        # Generate all simple moves for the opposing color to determine threatened squares
        threat_moves = self.generate_all_simple_moves(ChessBoard.opposing_color(color))
        threat = [[False] * 8 for _ in range(8)]
        for move in threat_moves:
            row, col = move.end_pos
            threat[row][col] = True

        all_moves = self.generate_all_simple_moves(color)  # Get the simple moves for the current color

        # Determine the king's position and the ending positions for castling
        row = 7 if color == 'w' else 0
        king_col = 4
        king_pos = (row, king_col)
        king_castle_end_pos = (row, king_col + 2)
        queen_castle_end_pos = (row, king_col - 2)

        # Check king-side castling
        if self.can_castle(color, 'king', threat):
            all_moves.append(Movement(king_pos, king_castle_end_pos, is_castling=True))

        # Check queen-side castling
        if self.can_castle(color, 'queen', threat):
            all_moves.append(Movement(king_pos, queen_castle_end_pos, is_castling=True))

        valid_moves = []

        for move in all_moves:
            # Create a copy of the current board
            temp_board = self.copy()

            # Apply the move to the temporary board
            temp_board.apply_move(move)

            # Check if the move places the king of the moving color in threat
            if color not in temp_board.kings_in_threat():
                valid_moves.append(move)

        return valid_moves



def play_chess(board):
    repetition_count = {}
    fifty_move_counter = 0

    while True:
        print(board)  # Print the current state of the board
        moves = board.all_valid_moves(board.current_color)

        # Check for stalemate
        if not moves:
            if board.king_in_threat(board.current_color):
                print(f"{board.opposing_color(board.current_color)} wins by checkmate!")
            else:
                print("Stalemate! The game is a draw.")
            break

        # Code to take player input for the move
        move = get_player_move(moves)  # Assuming this function takes care of user input

        # Apply the move
        board = board.apply_move(move)

        # Update repetition count
        board_fen = str(board)  # Assuming board's __str__ method represents the state
        repetition_count[board_fen] = repetition_count.get(board_fen, 0) + 1

        # Update fifty-move counter
        if isinstance(board.board[move.start_pos[0]][move.start_pos[1]], Pawn) or board.board[move.end_pos[0]][move.end_pos[1]] is not None:
            fifty_move_counter = 0
        else:
            fifty_move_counter += 1

        # Check for threefold repetition
        if any(count >= 3 for count in repetition_count.values()):
            print("Draw by threefold repetition. Game over.")
            break

        # Check for fifty-move rule
        if fifty_move_counter >= 50:
            print("Draw by the fifty-move rule. Game over.")
            break

        # Switch to the other player
        board.current_color = board.opposing_color(board.current_color)

    print("Thanks for playing!")


if __name__ == "__main__":
    chess_board = ChessBoard()
    chess_board.print_board()
