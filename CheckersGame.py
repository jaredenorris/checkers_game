#Author: Jared Norris
#Github username: jaredenorris
#Date: 3/7/2023
#Description: A checkers came using international draughts rules

class Checkers:
    """initializes board and game of checkers, communicates with player class"""
    def __init__(self):
        """creates checkers game and initializes board"""
        self._board = [[False, " W ", False, " W ", False, " W ", False, " W "],
                       [" W ", False, " W ", False, " W ", False, " W ", False],
                       [False, " W ", False, " W ", False, " W ", False, " W "],
                       [None, False, None, False, None, False, None, False],
                       [False, None, False, None, False, None, False, None],
                       [" B ", False, " B ", False, " B ", False, " B ", False],
                       [False, " B ", False, " B ", False, " B ", False, " B "],
                       [" B ", False, " B ", False, " B ", False, " B ", False]]
        self._turn = 0
        self._players = []


    def play_game(self, player_name, starting_square_location, destination_square_location):
        """method to move piece across checkers board, takes player_name, starting_square_location, and
        destination_square_location as parameters. Returns the number of opponent pieces captured. If piece
        makes it across board it becomes king, and if king makes it back across it becomes triple king.
        method will also assess whether move is valid for each type of piece"""
        captured_pieces = 0
        # raise exception if square does not exist
        if starting_square_location[0] > 7:
            raise InvalidSquare
        if starting_square_location[0] < 0:
            raise InvalidSquare
        if starting_square_location[1] > 7:
            raise InvalidSquare
        if starting_square_location[1] < 0:
            raise InvalidSquare

        # raise out of turn exception if White player goes first
        if self._turn % 2 == 0:
            for player in self._players:
                if player.get_player_name() == player_name:
                    if player.get_piece_color() != 'Black':
                        raise OutofTurn
        if self._turn % 2 != 0:
            for player in self._players:
                if player.get_player_name() == player_name:
                    if player.get_piece_color() != 'White':
                        raise OutofTurn

        # raise exception if player name is invalid
        if self._turn % 2 == 0:
            for player in self._players:
                if player.get_player_name() != player_name:
                    if player.get_piece_color() == 'Black':
                        raise InvalidPlayer
        if self._turn % 2 != 0:
            for player in self._players:
                if player.get_player_name() != player_name:
                    if player.get_piece_color() == 'White':
                        raise InvalidPlayer

        # raise exception if player does not own start piece
        start_row = self._board[starting_square_location[0]]
        start_pos = start_row[starting_square_location[1]]
        if start_pos == ' B ':
            for player in self._players:
                if player.get_player_name() == player_name:
                    if player.get_piece_color() != 'Black':
                        raise InvalidSquare
        if start_pos == ' W ':
            for player in self._players:
                if player.get_player_name() == player_name:
                    if player.get_piece_color() != 'White':
                        raise InvalidSquare
        if start_pos == 'BK ':
            for player in self._players:
                if player.get_player_name() == player_name:
                    if player.get_piece_color() != 'Black':
                        raise InvalidSquare
        if start_pos == 'BTK':
            for player in self._players:
                if player.get_player_name() == player_name:
                    if player.get_piece_color() != 'Black':
                        raise InvalidSquare
        if start_pos == 'WK ':
            for player in self._players:
                if player.get_player_name() == player_name:
                    if player.get_piece_color() != 'White':
                        raise InvalidSquare
        if start_pos == 'WTK':
            for player in self._players:
                if player.get_player_name() == player_name:
                    if player.get_piece_color() != 'White':
                        raise InvalidSquare

        # move piece
        self._board[destination_square_location[0]][destination_square_location[1]] = start_pos
        self._board[starting_square_location[0]][starting_square_location[1]] = None

        # if capture move check if piece is king
        if abs(starting_square_location[0] - destination_square_location[0]) > 1:
            if start_pos == "BK ":
                self.king_capture(player_name, starting_square_location, destination_square_location)
                captured_pieces += 1
                return captured_pieces
            if start_pos == "WK ":
                self.king_capture(player_name, starting_square_location, destination_square_location)
                captured_pieces += 1
                return captured_pieces
            if start_pos == "BTK ":
                self.king_capture(player_name, starting_square_location, destination_square_location)
                captured_pieces += 1
                return captured_pieces
            if start_pos == "WTK ":
                self.king_capture(player_name, starting_square_location, destination_square_location)
                captured_pieces += 1
                return captured_pieces

        # capture piece
        if abs(starting_square_location[0] - destination_square_location[0]) > 1:
            if self._turn % 2 != 0: #white capturing black
                capture_row = destination_square_location[0] - 1
                if destination_square_location[1] < starting_square_location[1]: #white jumped left
                    capture_piece = destination_square_location[1] + 1
                    self._board[capture_row][capture_piece] = None
                if destination_square_location[1] > starting_square_location[1]: #White jumped right
                    capture_piece = destination_square_location[1] - 1
                    self._board[capture_row][capture_piece] = None
                for player in self._players:
                    if player.get_piece_color() == "White":
                        player.set_captured_pieces_count(1)
                        captured_pieces += 1

            if self._turn % 2 == 0: #Black capturing white
                capture_row = destination_square_location[0] + 1
                if destination_square_location[1] < starting_square_location[1]: #black jumped left
                    capture_piece = destination_square_location[1] + 1
                    self._board[capture_row][capture_piece] = None
                if destination_square_location[1] > starting_square_location[1]: #black jumped right
                    capture_piece = destination_square_location[1] - 1
                    self._board[capture_row][capture_piece] = None
                for player in self._players:
                    if player.get_piece_color() == "Black":
                        player.set_captured_pieces_count(1)
                        captured_pieces += 1

        #promote to king
        if self._turn % 2 == 0: #Black made it to other side
            if destination_square_location[0] == 0:
                self._board[destination_square_location[0]][destination_square_location[1]] = "BK "
                for player in self._players:
                    if player.get_piece_color() == "Black":
                        player.set_king_count(1)
        if self._turn % 2 != 0: #White made it to other side
            if destination_square_location[0] == 7:
                self._board[destination_square_location[0]][destination_square_location[1]] = "WK "
                for player in self._players:
                    if player.get_piece_color() == "White":
                        player.set_king_count(1)

        self._turn += 1
        return captured_pieces

    def king_capture(self, player_name, starting_square_location, destination_square_location):
        """method defines rules for a king capturing opponents"""
        start_row = starting_square_location[0]
        start_column = starting_square_location[1]
        destination_row = destination_square_location[0]
        destination_column = destination_square_location[1]
        distance = abs(start_row - destination_row)


        # king jumps up
        if destination_row < start_row:
            if destination_column > start_column: # king jumps right
                count = 1
                while count < distance:
                    destination_row += 1
                    destination_column -= 1
                    self._board[destination_row][destination_column] = None
                    count += 1
            if destination_column < start_column: # king jumps left
                count = 1
                while count < distance:
                    destination_row += 1
                    destination_column += 1
                    self._board[destination_row][destination_column] = None
                    count += 1
        # king jumps down
        if destination_row > start_row:
            if destination_column > start_column: # king jumps right
                count = 1
                while count < distance:
                    destination_row -= 1
                    destination_column -= 1
                    self._board[destination_row][destination_column] = None
                    count += 1
            if destination_column < start_column: # king jumps left
                count = 1
                while count < distance:
                    destination_row -= 1
                    destination_column += 1
                    self._board[destination_row][destination_column] = None
                    count += 1
        #promote triple king
        destination_row = destination_square_location[0]
        destination_column = destination_square_location[1]
        destination_pos = self._board[destination_row][destination_column]
        if destination_pos == "WK ":
            if destination_row == 0:
                self._board[destination_row][destination_column] = "WTK"
                for player in self._players:
                    if player.get_player_name() == player_name:
                        player.set_triple_king_count(1)
                        player.set_king_count(-1)
        if destination_pos == "BK ":
            if destination_row == 7:
                self._board[destination_row][destination_column] = "BTK"
                for player in self._players:
                    if player.get_player_name() == player_name:
                        player.set_triple_king_count(1)
                        player.set_king_count(-1)



        self._turn += 1
        for player in self._players:
            if player.get_player_name() == player_name:
                player.set_captured_pieces_count(1)




    def get_checker_details(self, square_location):
        """takes as parameter a square_location and returns the checker details in the square_location"""
        if square_location[0] < 0:
            raise InvalidSquare
        if square_location[0] > 7:
            raise InvalidSquare
        if square_location[1] < 0:
            raise InvalidSquare
        if square_location[1] > 7:
            raise InvalidSquare

        row = square_location[0]
        column = square_location[1]
        checker = self._board[row][column]
        if checker == " W ":
            return "White"
        if checker == " B ":
            return "Black"
        if checker is None:
            return None
        if checker == "WK ":
            return "White_king"
        if checker == "BK ":
            return "Black_king"
        if checker == "BTK":
            return "Black_Triple_King"
        if checker == "WTK":
            return "White_Triple_King"



    def create_player(self, player_name, piece_color):
        """create's player object. Takes player_name and piece_color as paramaters. Creates and returns
        player object"""
        player = Player(player_name, piece_color)
        self._players.append(player)
        return player


    def print_board(self):
        """Takes no parameters and prints board in the form of a list of lists"""
        for row in self._board:
            print(row)
        print(" ")

    def game_winner(self):
        """takes no parameters and returns the player name who won the game"""
        for player in self._players:
            if player.get_captured_pieces_count() == 12:
                return player.get_player_name()
        return "Game has not ended"

class OutofTurn(Exception):
    """exception raised if player tries to move piece out of turn"""
    pass

class InvalidSquare(Exception):
    """exception raised if the player does not own the checker present at the square_location
    or if the square_location does not exist on the board"""
    pass

class InvalidPlayer(Exception):
    """exception raised if player name is not valid"""
    pass

class Player:
    """initializes player, communicates with Checkers class for create player method"""

    def __init__(self, player_name, piece_color):
        """creates player initialize player_name and piece_color"""
        self._player_name = player_name
        self._piece_color = piece_color
        self._king_count = 0
        self._triple_king_count = 0
        self._captured_pieces_count = 0
        self._score = 0

    def get_king_count(self):
        """returns number of kings a player has"""
        return self._king_count

    def get_triple_king_count(self):
        """returns number of triple kings a player has"""
        return self._triple_king_count

    def get_captured_pieces_count(self):
        """returns the number of opponent pieces that the player has captured"""
        return self._captured_pieces_count

    def get_piece_color(self):
        """returns piece color for use in other methods"""
        return self._piece_color

    def get_player_name(self):
        """returns player name for use in other methods"""
        return self._player_name

    def set_captured_pieces_count(self, piece):
        """sets captured pieces count"""
        self._captured_pieces_count += piece

    def set_king_count(self, king):
        """sets number of kings player has"""
        self._king_count += king

    def set_triple_king_count(self, king):
        """sets number of triple kings player has"""
        self._triple_king_count += king

def main():
    """Exception handling for exception classes"""
    test = Checkers()
    test.create_player("Daryl", "Black")
    try:
        test.play_game("Daryl", (5, 0), (4,1))
    except (OutofTurn):
        print("It is not this players turn")
    except (InvalidPlayer):
        print("Player Invalid")
    except (InvalidSquare):
        print("Invalid Square")


if __name__ == '__main__':
    main()




#game = Checkers()
#game.create_player("Joe", "Black")
#game.create_player("Jim", "White")
#game.print_board()
#game.play_game("Joe", (5, 2), (4, 3))
#game.print_board()
#game.play_game("Jim", (2, 3), (3, 2))
#game.print_board()
#game.play_game("Joe", (5, 0), (4, 1))
#game.print_board()
#game.play_game("Jim", (2, 1), (3, 0))
#game.print_board()
#game.play_game("Joe", (4, 1), (2, 3))
#game.print_board()
#game.play_game("Jim", (1, 2), (2, 1))
#game.print_board()
#game.play_game("Joe", (5, 6), (4, 5))
#game.print_board()
#game.play_game("Jim", (0, 1), (1, 2))
#game.print_board()
#game.play_game("Joe", (2, 3), (0, 1))
#game.print_board()
#game.play_game("Jim", (3, 0), (4, 1))
#game.print_board()
#game.play_game("Joe", (6, 5), (5, 6))
#game.print_board()
#game.play_game("Jim", (4, 1), (5, 2))
#game.print_board()
#game.play_game("Joe", (7, 4), (6, 5))
#game.print_board()
#game.play_game("Jim", (5, 2), (7, 4))
#game.print_board()
#game.play_game("Joe", (5, 6), (4, 7))
#game.print_board()
#game.play_game("Jim", (7, 4), (5, 6))
#game.print_board()
#game.play_game("Joe", (4, 5), (3, 4))
#game.print_board()
#game.play_game("Jim", (5, 6), (2, 3))
#game.print_board()
#game.play_game("Joe", (7, 2), (6, 3))
#game.print_board()
#game.play_game("Jim", (2, 3), (4, 1))
#game.print_board()
#game.play_game("Joe", (5, 4), (4, 5))
#game.print_board()
#game.play_game("Jim", (1, 4), (2, 3))
#game.print_board()
#game.play_game("Joe", (0, 1), (3, 4))
#game.print_board()
#game.play_game("Jim", (4, 1), (2, 3))
#game.print_board()
#game.play_game("Joe", (3, 4), (5, 2))
#game.print_board()
#game.play_game("Jim", (2, 3), (0, 1))
#game.print_board()
#ame.play_game("Joe", (5, 2), (7, 4))
#game.print_board()
#game.play_game("Jim", (0, 1), (5, 6))
#game.print_board()


