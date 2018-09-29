from random import randint
import os

class Players:
    COMPUTER = "C"
    PLAYER1 = "P"

class Piece:
    def __init__(self, player, number, position = 0):
        self.player = player
        self.number = number
        self.position = position

    def move(self, dice):
        self.position += dice

def dice_throw():
    global dice
    for i in range(0, 4):
        dice[i] = randint(0, 1)

def draw():
    board1 = ["|    |", "|    |", "|    |", "|    |", "      ", "      ", "|    |", "|    |"]
    board2 = ["|    |" for x in range(8)]
    board3 = ["|    |", "|    |", "|    |", "|    |", "      ", "      ", "|    |", "|    |"]

    for p in pieces_computer:
        pos = p.position
        if pos > 0:
            if pos < 5:
                board1[4 - pos] = "| " + p.player + str(p.number) + " |"
            elif pos < 13:
                board2[pos - 5] = "| " + p.player + str(p.number) + " |"
            elif pos < 15:
                board1[8 - pos % 12] = "| " + p.player + str(p.number) + " |"

    for p in pieces_player:
        pos = p.position
        if pos > 0:
            if pos < 5:
                board3[4 - pos] = "| " + p.player + str(p.number) + " |"
            elif pos < 13:
                board2[pos - 5] = "| " + p.player + str(p.number) + " |"
            elif pos < 15:
                board3[8 - pos % 12] = "| " + p.player + str(p.number) + " |"

    print("".join(board1))
    print("".join(board2))
    print("".join(board3))

def find_piece(pieces, pos):
    found_piece = [piece for piece in pieces if piece.position < 15 and piece.position == pos]
    if not found_piece:
        return found_piece
    return found_piece[0]

# Checks if input piece is inside a rosette box, granting the player an extra turn if so.
def is_rosette_box(piece):
    return piece.position == 4 or piece.position == 8 or piece.position == 14

# Implementation of the move for each player.
# The parameter is_computer must be true if the move is from the computer. It is false if it's the player who is moving a piece.
def move(dice_count, is_computer):
    global pieces_computer, pieces_player, repeat_turn
    repeat_turn = False

    # This is necessary in order to use the same code for a computer move and a player move.
    own_pieces = []
    enemy_pieces = []
    if is_computer:
        own_pieces = pieces_computer
        enemy_pieces = pieces_player
    else:
        own_pieces = pieces_player
        enemy_pieces = pieces_computer

    # Now we find the possible legal moves.
    # not_colliding_moves saves all own pieces wich won't land in an already occupied own piece.
    not_colliding_moves = []
    # kill_moves stores every own piece that could kill an enemy piece.
    kill_moves = []

    for p in own_pieces:
        if p.position < 15 and p.position + dice_count <= 15:
            # If the dice throw makes the piece land on a legal position.
            # Position 0 is the start.
            # Position 1 is the first square.
            # Position 14 is the last square.
            # Position 15 is the end. If you are near position 15, to end the game
            other_pieces = [x for x in own_pieces if x is not p]
            found = False
            i = 0
            while not found and i < len(other_pieces):
                # First, detect own pieces which could have collisions with the current dice throw. If there is one collision, ignore this piece p.
                found = p.position + dice_count == other_pieces[i].position and other_pieces[i].position < 15
                if not found:
                    i += 1
            if not found:
                # If it doesn't collide with own pieces, check landing conditions.
                if p.position + dice_count < 5 or p.position + dice_count > 12:
                    # If piece lands inside own lane.
                    not_colliding_moves.append(p)
                elif not find_piece(enemy_pieces, p.position + dice_count):
                    # If piece lands in mid lane and there is NOT a player piece.
                    not_colliding_moves.append(p)
                elif p.position + dice_count != 8:
                    # If piece lands in mid lane and there IS a player piece and it's not in square number 8 safespot.
                    kill_moves.append(p)

    print("Number of not colliding moves: " + str(len(not_colliding_moves)))
    print("Number of kill moves: " + str(len(kill_moves)))

    if is_computer:
        # Implementation of the computer AI. Choose a random move between the list of possible moves.
        if len(not_colliding_moves) > 0 and len(kill_moves) > 0:
            rnd_not_colliding = randint(0, len(not_colliding_moves) - 1)
            rnd_kill = randint(0, len(kill_moves) - 1)

            rnd = randint(0, 1)
            if rnd == 0:
                not_colliding_moves[rnd_not_colliding].move(dice_count)
                repeat_turn = is_rosette_box(not_colliding_moves[rnd_not_colliding])
            else:
                kill_moves[rnd_kill].move(dice_count)
                repeat_turn = is_rosette_box(kill_moves[rnd_kill])
                player_killed = find_piece(pieces_player, kill_moves[rnd_kill].position)
                player_killed.position = 0
        elif len(not_colliding_moves) > 0:
            rnd_not_colliding = randint(0, len(not_colliding_moves) - 1)
            not_colliding_moves[rnd_not_colliding].move(dice_count)
            repeat_turn = is_rosette_box(not_colliding_moves[rnd_not_colliding])
        elif len(kill_moves) > 0:
            rnd_kill = randint(0, len(kill_moves) - 1)
            kill_moves[rnd_kill].move(dice_count)
            repeat_turn = is_rosette_box(kill_moves[rnd_kill])
            player_killed = find_piece(pieces_player, kill_moves[rnd_kill].position)
            player_killed.position = 0
        else:
            print("Computer doesn't have legal moves.")
    else:
        # Implementation of the player move.

        # First, we find every piece number with a legal move.
        piece_numbers = []
        for p in not_colliding_moves:
            piece_numbers.append(p.number)
        for p in kill_moves:
            piece_numbers.append(p.number)

        if len(piece_numbers) > 0:
            piece_numbers.sort()

        # Then, we show the possible piece moves.
        if len(piece_numbers) > 0:
            str_pieces = "Possible piece movements: "
            for n in piece_numbers:
                str_pieces += str(n) + " "
            print(str_pieces)
        else:
            print ("Player doesn't have any legal move.")

        # Now, we ask the user for the piece to move.
        if len(piece_numbers) > 0:
            user_input = False
            while not user_input:
                try:
                    pos = int(input("Which piece do you want to move?: "))
                    user_input = True
                    if pos < 0 or pos > 6:
                        print("Invalid piece position.")
                        user_input = False
                    if pos not in piece_numbers:
                        print("Not a legal move.")
                        user_input = False
                except ValueError:
                    print("Invalid number.")

            # After that, we find the chosen piece in the not colliding moves and kill moves lists.
            moving_piece = [p for p in not_colliding_moves if p.number == pos]
            if moving_piece:
                # If it's a not colliding move.
                moving_piece[0].move(dice_count)
                repeat_turn = is_rosette_box(moving_piece[0])
            else:
                moving_piece = [p for p in kill_moves if p.number == pos]
                if moving_piece:
                    # If it's a kill move.
                    moving_piece[0].move(dice_count)
                    repeat_turn = is_rosette_box(moving_piece[0])
                    killed_enemy = find_piece(pieces_computer, moving_piece[0].position)
                    killed_enemy.position = 0
                    print("Enemy killed")
            print("Player moved piece " + str(pos) + " " + str(dice_count) + " tiles.")
    if repeat_turn:
        print("The piece landed in a rosette. Extra turn!")


dice = [0, 0, 0, 0]
pieces_player = []
pieces_computer = []
repeat_turn = False

def player_win():
    for p in pieces_player:
        if p.position != 15:
            return False
    return True

def computer_win():
    for p in pieces_computer:
        if p.position != 15:
            return False
    return True

def start():
    playing = True
    game = True
    while playing:
        print("Welcome to The Game of AntiqUr.")

        pieces_player.clear()
        pieces_computer.clear()
        for i in range(0, 7):
            pieces_player.append(Piece(Players.PLAYER1, i))
            pieces_computer.append(Piece(Players.COMPUTER, i))

        game = True
        turn = False
        while game:
            #if not turn:
            #    clear = lambda: os.system("cls")
            #    clear()
            draw()
            dice_throw()
            dice_count = sum(dice)
            print("Dice throw: " + str(dice_count))
            if not turn:
                print("Computer turn.")
                if dice_count > 0:
                    move(dice_count, True)
            else:
                print("Player turn.")
                if dice_count > 0:
                    move(dice_count, False)

            while repeat_turn:
                draw()
                dice_throw()
                dice_count = sum(dice)
                print("Dice throw: " + str(dice_count))
                if not turn:
                    print("Computer turn.")
                    if dice_count > 0:
                        move(dice_count, True)
                else:
                    print("Player turn.")
                    if dice_count > 0:
                        move(dice_count, False)

            game = not (player_win() or computer_win())
            turn = not turn

            if not game:
                if player_win():
                    print("Player won the game!")
                elif computer_win():
                    print("Computer won the game...")
                print("Do you want to play another match?")
                choice = input("Type Y if yes, another key if you want to exit: ")
                if choice != "Y" and choice != "y":
                    playing = False

start()
