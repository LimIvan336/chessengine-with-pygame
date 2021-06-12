#Store the state, info of the game
from castleRights import CastleRights
from move import Move

class GameState():
    def __init__(self):
        #initialize 8x8 chess board
        #2 characters, bK - black King
        #"--" represents empty slot
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_to_move = True #white starts to move
        self.move_log = []
        self.move_functions = {"p": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                                "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}

        #for checking valid moves (check, checkmate) and castling moves
        self.white_king_location = (7,4)
        self.black_king_location = (0,4)

        self.checkmate = False
        self.stalemate = False

        #en passant
        self.enpassant_possible = () #coord where en passant is possible

        #castling rights
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castling_rights_log = [CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                                self.current_castling_rights.wqs, self.current_castling_rights.bqs)] #to undo

    #executes a move, doesnt work on en passant, castling, pawn promotion
    def make_move(self, move):
        self.board[move.start_row][move.start_col] ="--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move) #to undo it later

        #update king's location (for checking valid moves)
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

        #pawn promotion make to queen
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"

        #en passant
        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = "--" #capturing pawn

        #update enpassant_possible var
        if move.piece_moved[1] == "p" and abs(move.start_row - move.end_row) == 2: #only works on 2 square pawn adv
            self.enpassant_possible = ((move.start_row + move.end_row)//2, move.start_col)
        else:
            self.enpassant_possible = () #reset back to "no" moves

        #castling
        if move.is_castle_move:
            if move.end_col - move.start_col == 2: #this is a king side castle moves
                self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col + 1] #moves rook
                self.board[move.end_row][move.end_col+1] = "--" #removes old rook

            else: #this is a queen side castle move
                self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col - 2] #moves rook
                self.board[move.end_row][move.end_col-2] = "--"


        #update castling rights - when rook / king moves
        self.update_castling_rights(move)
        self.castling_rights_log.append(CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                                self.current_castling_rights.wqs, self.current_castling_rights.bqs)) #to undo later

        self.white_to_move = not self.white_to_move #swap players


    def update_castling_rights(self, move):
        #check white king
        if move.piece_moved == "wK":
            self.current_castling_rights.wks = False
            self.current_castling_rights.wqs = False
        #check black king
        elif move.piece_moved == "bK":
            self.current_castling_rights.bks = False
            self.current_castling_rights.bqs = False
        #check rooks
        elif move.piece_moved == "wR":
            if move.start_row == 7:
                if move.start_col == 0: #left rook
                    self.current_castling_rights.wqs = False
                elif move.start_col == 7: #right rook
                    self.current_castling_rights.wks = False
        elif move.piece_moved == "bR":
            if move.start_row == 0:
                if move.start_col == 0: #left rook
                    self.current_castling_rights.bqs = False
                elif move.start_col == 7: #right rook
                    self.current_castling_rights.bks = False

        #check if rook is taken
        if move.piece_captured == "wR":
            if move.end_row == 7:
                if move.end_col == 0: #left rook
                    self.current_castling_rights.wqs = False
                elif move.end_col == 7: #right rook
                    self.current_castling_rights.wks = False
        elif move.piece_captured == "bR":
            if move.end_col == 0:
                if move.end_col == 0: #left rook
                    self.current_castling_rights.bqs = False
                elif move.end_col == 7: #right rook
                    self.current_castling_rights.bks = False


    #undo last move
    def undo_move(self):
        if len(self.move_log) != 0: #make sure theres a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured

            #undo king's location (for checking valid moves)
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)

            #undo en passant move
            if move.is_enpassant_move:
                self.board[move.end_row][move.end_col] = "--"
                self.board[move.start_row][move.end_col] = move.piece_captured
                self.enpassant_possible = (move.end_row, move.end_col) #make sure enpassant_possible is set back

            #undo 2 square pawn advance
            if move.piece_moved[1] == "p" and abs(move.start_row - move.end_row) ==2:
                self.enpassant_possible = ()

            #undo castling rights
            self.castling_rights_log.pop() #remove last castling rights
            new_rights = self.castling_rights_log[-1]
            self.current_castling_rights = CastleRights(new_rights.wks, new_rights.bks, new_rights.wqs, new_rights.bqs) #set current_castling_rights to last castling rights

            #undo castle moves
            if move.is_castle_move:
                if move.end_col - move.start_col == 2: #kingside
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1] #moves rook back
                    self.board[move.end_row][move.end_col -1] = "--"
                else: #queenside
                    self.board[move.end_row][move.end_col -2] = self.board[move.end_row][move.end_col + 1] #moves rook back
                    self.board[move.end_row][move.end_col +1] = "--"


            self.white_to_move = not self.white_to_move



    #All moves considering checks (valid moves)
    def get_valid_moves(self):
        #Debugging castling_rights_log
        # for log in self.castling_rights_log:
        #     print(log.wks, log.wqs, log.bks, log.bqs, end=", ")
        # print()
        temp_enpassant_possible = self.enpassant_possible #save value when generating all possible moves
        temp_castling_rights = CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                            self.current_castling_rights.wqs, self.current_castling_rights.bqs)
        #generate all possible moves
        moves = self.get_all_possible_moves()

        if self.white_to_move:
            self.get_castling_moves(self.white_king_location[0], self.white_king_location[1], moves)
        else:
            self.get_castling_moves(self.black_king_location[0], self.black_king_location[1], moves)

        #for each move, make that move
        for idx in range(len(moves)-1,-1,-1): #backwards to reduce bugs
            self.make_move(moves[idx])
            self.white_to_move = not self.white_to_move #swap turns because self.make_move switch turns
            #generate oponent's move
            #for each opp moves, see if king is attacked
            if self.in_check():
                moves.remove(moves[idx])
            self.white_to_move = not self.white_to_move
            self.undo_move()

            #if king attacked, not a valid move, remove from moves


        #check if checkmate/stalemate
        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
                print("CHECKMATE")
            else:
                self.stalemate = True
                print("STALEMATE")
        else: #undo move
            self.checkmate = False
            self.stalemate = False

        self.enpassant_possible = temp_enpassant_possible
        self.current_castling_rights = temp_castling_rights

        #Debugging
        # for move in moves:
        #     print(move.piece_moved, move.piece_captured, move.move_id)

        return moves

    #All moves that dont consider checks
    def get_all_possible_moves(self):
        possible_moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0] #checking whose turn it is
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[row][col][1]

                    self.move_functions[piece](row, col, possible_moves) #call moves for all pieces

        return possible_moves

    #Pieces moves
    def get_pawn_moves(self, row, col, moves):
        if self.white_to_move: #white
            if self.board[row-1][col] == "--": #if is empty
                moves.append(Move((row,col) , (row-1,col) , self.board))
                if row == 6 and self.board[row-2][col] == "--": #2 square pawn move
                    moves.append(Move((row,col) , (row-2,col) , self.board))

            if col - 1 >= 0: #forward left
                if self.board[row-1][col-1][0] == "b": #capture black
                    moves.append(Move((row,col) , (row-1,col-1) , self.board))
                elif ((row-1, col-1) == self.enpassant_possible):
                    moves.append(Move((row,col) , (row-1,col-1) , self.board, is_enpassant_move=True))

            if col + 1 < 8: #forward right
                if self.board[row-1][col+1][0] == "b": #capture black
                    moves.append(Move((row,col) , (row-1,col+1) , self.board))
                elif ((row-1, col+1) == self.enpassant_possible):
                    moves.append(Move((row,col) , (row-1,col+1) , self.board, is_enpassant_move=True))

        else: #black
            if self.board[row+1][col] == "--": #if is empty
                moves.append(Move((row,col) , (row+1,col) , self.board))
                if row == 1 and self.board[row+2][col] == "--": #2 square pawn move
                    moves.append(Move((row,col) , (row+2,col) , self.board))

            if col - 1 >= 0: #downward left
                if self.board[row+1][col-1][0] == "w": #capture white
                    moves.append(Move((row,col) , (row+1,col-1) , self.board))
                elif ((row+1, col-1) == self.enpassant_possible):
                    moves.append(Move((row,col) , (row+1,col-1) , self.board, is_enpassant_move=True))

            if col + 1 < 8: #downward right
                if self.board[row+1][col+1][0] == "w": #capture white
                    moves.append(Move((row,col) , (row+1,col+1) , self.board))
                elif ((row+1, col+1) == self.enpassant_possible):
                    moves.append(Move((row,col) , (row+1,col+1) , self.board, is_enpassant_move=True))


    def get_rook_moves(self, row, col, moves):
        possible_directions = ((-1,0), (0,-1), (1,0), (0,1)) #(change_row, change_col)
        enemy_color = "b" if self.white_to_move else "w"
        for direction in possible_directions:
            for i in range(1,8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i

                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((row,col) , (end_row , end_col) , self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row,col) , (end_row , end_col) , self.board))
                        break
                    else: #friendly fire
                        break

                else: #off board
                    break


    def get_knight_moves(self, row, col, moves):
        l_moves = ((-2,-1), (-2,1), (2,-1), (2, 1), (-1,-2), (-1,2), (1,-2), (1,2))
        ally_color = "w" if self.white_to_move else "b"
        for l_move in l_moves:
            end_row = row + l_move[0]
            end_col = col + l_move[1]
            if 0 <= end_row < 8 and 0 <= end_col <8: #stays on board
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color: #empty/enemy
                    moves.append(Move((row,col) , (end_row , end_col) , self.board))


    def get_bishop_moves(self, row, col, moves):
        possible_directions = ((-1,-1), (-1,1), (1,-1), (1,1)) #(change_row, change_col)
        enemy_color = "b" if self.white_to_move else "w"
        for direction in possible_directions:
            for i in range(1,8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i

                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((row,col) , (end_row , end_col) , self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row,col) , (end_row , end_col) , self.board))
                        break
                    else: #friendly fire
                        break

                else: #off board
                    break


    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)


    def get_king_moves(self, row, col, moves):
        king_moves = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1))
        ally_color = "w" if self.white_to_move else "b"
        for king_move in king_moves:
            end_row = row + king_move[0]
            end_col = col + king_move[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((row,col) , (end_row , end_col) , self.board))



    #get castling moves
    def get_castling_moves(self, row, col, moves):
        #if king in check
        if self.square_under_attacked(row, col):
            return #cant castle if in check
        #king side
        if (self.white_to_move and self.current_castling_rights.wks) or (not self.white_to_move and self.current_castling_rights.bks):
            self.get_kingside_castling_moves(row, col, moves)
        #queen side
        if (self.white_to_move and self.current_castling_rights.wqs) or (not self.white_to_move and self.current_castling_rights.bqs):
            self.get_queenside_castling_moves(row, col, moves)


    def get_kingside_castling_moves(self, row, col, moves):
        #check 2 squares
        if self.board[row][col+1] == "--" and self.board[row][col+2] == "--":
            if not self.square_under_attacked(row, col+1) and not self.square_under_attacked(row, col+2):
                moves.append(Move((row, col), (row, col+2), self.board, is_castle_move = True))


    def get_queenside_castling_moves(self, row, col, moves):
        #check 3 square
        if self.board[row][col-1] == "--" and self.board[row][col-2] == "--" and self.board[row][col-3] == "--":
            if not self.square_under_attacked(row, col-1) and not self.square_under_attacked(row, col-2):
                moves.append(Move((row, col), (row, col-2), self.board, is_castle_move = True))


    #determine if player is in check
    def in_check(self):
        if self.white_to_move:
            return self.square_under_attacked(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attacked(self.black_king_location[0], self.black_king_location[1])

    #determine if the enemy can attack the square (row, col)
    def square_under_attacked(self, row, col):
        self.white_to_move = not self.white_to_move #switch to opponent
        opp_moves = self.get_all_possible_moves()
        for move in opp_moves:
            if move.end_row == row and move.end_col == col:
                self.white_to_move = not self.white_to_move #switch back
                return True #square is under attack

        self.white_to_move = not self.white_to_move
        return False
