#main driver file, handling user input and displaying current game state

import pygame as p
import GameState

WIDTH = HEIGHT = 512
DIMENSION = 8 #8x8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations
IMAGES = {}

#loading images is very slow, so initialize a global dictionary once in the main
def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        #scale the images, then load it into dictionary
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

#Graphics on a game state
def draw_game_state(screen, game_state, valid_moves, square_selected):
    draw_board(screen) #draw squares on board
    highlight_squares(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state.board) #draw pieces (after drawing board to make it on top)


#draw the squares on the board (top left square is always light)
#light squares = even, dark square = odd
def draw_board(screen):
    global colors
    colors = [p.Color((188,210,232)), p.Color((115, 165, 198))]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row+col)%2)]
            #draw column by row
            p.draw.rect(screen, color, p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

#draw pieces
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--": #not empty
                screen.blit(IMAGES[piece], p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

#graphics
#higlights squares selected and valid moves from the square
def highlight_squares(screen, game_state, valid_moves, square_selected):
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == ("w" if game_state.white_to_move else "b"): #make sure the square selected is the same color as the current player
            #highlight selected square
            surface = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            surface.set_alpha(100) #transparency value, 0 : transparent, 255: opaque
            surface.fill(p.Color("orange"))
            screen.blit(surface, (col*SQUARE_SIZE, row*SQUARE_SIZE))

            #highlight moves from that square
            surface.fill(p.Color("yellow"))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(surface, (move.end_col*SQUARE_SIZE, move.end_row*SQUARE_SIZE))

    #highlight last move
    if game_state.move_log != []:
        last_move = game_state.move_log[-1]
        surface = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        surface.set_alpha(100)
        surface.fill(p.Color("orange"))
        screen.blit(surface, (last_move.end_col*SQUARE_SIZE, last_move.end_row*SQUARE_SIZE))
        screen.blit(surface, (last_move.start_col*SQUARE_SIZE, last_move.start_row*SQUARE_SIZE))


#animating moves
def animate_moves(screen, board, move, clock):
    global colors
    delta_row = move.end_row - move.start_row
    delta_col = move.end_col - move.start_col
    frames_per_sqaure = 5 #no of frames for 1 square of animation, higher -> slower animation, lower -> faster animation
    frame_count = (abs(delta_row) + abs(delta_col)) * frames_per_sqaure
    for frame in range(frame_count + 1):
        row, col = (move.start_row + delta_row * frame/frame_count, move.start_col + delta_col * frame/frame_count)
        draw_board(screen)
        draw_pieces(screen, board)

        #erase piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col*SQUARE_SIZE, move.end_row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)

        #draw captured piece onto rectangle
        if move.piece_captured != "--":
            screen.blit(IMAGES[move.piece_captured], end_square)

        #draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)

def draw_text(screen, text):
    #create pygame font obj, parameters: font type, size, bold, italic
    font = p.font.SysFont("Helvitca", 38, True, False)
    #parameters: text, antialias, color, background = True
    text_object = font.render(text, 0, p.Color("Gray"))
    text_location = p.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - text_object.get_width()/2, HEIGHT/2 - text_object.get_height()/2) #center text
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color("Black"))
    screen.blit(text_object, text_location.move(2,2))

#main driver
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT)) #screen
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = GameState.GameState()
    load_images()
    running = True
    square_selected = () #initalize that no square is selected. Shld be tuple (row,col)
    player_clicks = [] #keep track on the player clicks. Shld be two tuples: [(6,1),(4,1)] <- moving pawn [(initial_row, initial_col), (final_row, final_col)]


    valid_moves = game_state.get_valid_moves()
    move_made = False #flag variable for when a move is made
    animate = False #flag variable for animating a move (undo doesnt animate the move)
    game_over = False #flag variable for when

    #sound effects
    move_sound = p.mixer.Sound("./Sound Effects/move.mp3")
    capture_sound = p.mixer.Sound("./Sound Effects/capture.mp3")

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos() #returns (x,y) location of mouse
                    col = location[0] // SQUARE_SIZE #column of square picked
                    row = location[1] // SQUARE_SIZE #row of square picked

                    if square_selected == (row, col): #prevent clicking on same square twice
                        square_selected = () #deselect
                        player_clicks = [] #restart
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected) #append, inital_pos and final_pos

                    if len(player_clicks) == 2: #second click
                        move = GameState.Move(player_clicks[0], player_clicks[1], game_state.board)
                        print(move.get_chess_notation())
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.make_move(valid_moves[i])
                                if move.piece_captured == "--":
                                    move_sound.play()
                                else:
                                    capture_sound.play()
                                move_made = True
                                animate = True
                                square_selected = () #Reset user clicks
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]

                # print(player_clicks)
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when z is pressed
                    game_state.undo_move()
                    print("Move undoed")
                    move_made = False
                    animate = False
                    game_over = False
                    valid_moves = game_state.get_valid_moves()

                elif e.key == p.K_r: #reset the board when r is pressed
                    game_state = GameState.GameState()
                    valid_moves = game_state.get_valid_moves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    print("Game restarted.")

        if move_made:
            if animate:
                animate_moves(screen, game_state.board, game_state.move_log[-1], clock)
            valid_moves = game_state.get_valid_moves()
            move_made = False
            animate = False

        draw_game_state(screen, game_state, valid_moves, square_selected)

        if game_state.checkmate:
            game_over = True
            if game_state.white_to_move: #black wins
                draw_text(screen, "Black wins by checkmate")
            else:
                draw_text(screen, "White wins by checkmate")
        elif game_state.stalemate:
            game_over = True
            draw_text(screen, "Stalemate")
        #update clock
        clock.tick(MAX_FPS)
        #update screen display
        p.display.flip()

if __name__ == "__main__":
    main()
