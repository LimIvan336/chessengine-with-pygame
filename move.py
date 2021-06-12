class Move():

    ranks_to_rows = {"1": 7, "2": 6, "3" :5 , "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v:k for k,v in files_to_cols.items()}


    def __init__(self, start_square, end_square, board, is_enpassant_move = False, is_castle_move = False):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

        #pawn promotion
        self.is_pawn_promotion = ((self.piece_moved == "wp" and self.end_row == 0) or (self.piece_moved == "bp" and self.end_row == 7))

        #en passant
        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.piece_captured = "wp" if self.piece_moved == "bp" else "bp"

        #castle moves
        self.is_castle_move = is_castle_move

        self.move_id = self.start_row * 1000 + self.start_col*100 + self.end_row*10 + self.end_col #for comparing if both moves are equal


    def get_chess_notation(self):
        # making real chess notation, file-rank ex: "a6"
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    #Override wquals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False
