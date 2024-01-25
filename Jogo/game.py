
class Game():
    def __init__(self, pieces, game_board):
        self.game_board = game_board
        self.pieces = pieces
        self.cost = 0


    def print_game(self):
        for row in self.game_board:
            print(' '.join(row))


    def valid_move(self, piece_id, new_piece_coordinates):
        # Check if all new coordinates are valid, i.e., the cell is either '0' or the same as the piece_id
        all_moves = ['valid' if self.game_board[new_coords[0]][new_coords[1]] in ['0', piece_id] else 'not valid' for new_coords in new_piece_coordinates]
            
        if 'not valid' in all_moves:
            return 'not valid'
        else:
            return 'valid'
    

    def update_game_board(self, piece_id, new_piece_coordinates):
         # Update the game board with the new piece coordinates
        for position in self.pieces[piece_id]:
            position_x = position[0]
            position_y = position[1]
            self.game_board[position_x][position_y] = '0'

        for new_coordinate in new_piece_coordinates:
            new_coordinate_x = new_coordinate[0]
            new_coordinate_y = new_coordinate[1]
            self.game_board[new_coordinate_x][new_coordinate_y] = piece_id


    def update_pieces_coordinates(self, piece_id, new_piece_coordinates):
        # Update the piece coordinates in the pieces dictionary
        new_list = []
        for new_coordinate in new_piece_coordinates:
            new_list.append(new_coordinate)
        self.pieces[piece_id] = new_list


    def pieces_movements(self, piece_id, direction):
        # Calculate the new coordinates of a piece based on the given direction
        piece_coordenates = self.pieces[piece_id]

        if direction == 'up':
            move_x, move_y = -1, 0
        elif direction == 'down':
            move_x, move_y = 1, 0
        elif direction == 'left':
            move_x, move_y = 0, -1
        elif direction == 'right':
            move_x, move_y = 0, 1

        new_piece_coordenates = []
        for coordenates in piece_coordenates:
            new_x = coordenates[0] + move_x
            new_y = coordenates[1] + move_y
            new_piece_coordenates.append((new_x, new_y))
        
        return new_piece_coordenates
        

    def move_pieces(self, piece_id, direction, stamp):
        # Move a piece in the given direction if the move is valid, update game board, piece coordinates, and cost
        new_piece_coordenates = self.pieces_movements(piece_id, direction)

        if self.valid_move(piece_id, new_piece_coordenates) == 'valid':
            self.update_game_board(piece_id, new_piece_coordenates)
            self.update_pieces_coordinates(piece_id, new_piece_coordenates)
            self.cost += 1
            if stamp == True:
                self.print_game()
            if (self.win() == True) and (stamp == True):
                print("YOU WON!")
        else:
            if stamp == True:
                print("You can't move that piece to that place")
                self.print_game()
            else:
                pass


    def win(self):
        # Check if the winning condition is met
        winning_location = [(4,2),(4,3),(5,2),(5,3)]
        counter = 0
        for position in self.pieces['!']:
            if position in winning_location:
                counter += 1

        if counter == 4:
            return True
        else:
            return False
        

    def manhattan_distance(self):
        
        # Calculate the Manhattan distance for a piece with a given piece_id
        piece_id = '!'
        piece_coordinates = self.pieces[piece_id]
        winning_location = [(4,2),(4,3),(5,2),(5,3)]
        current_distance = -1

        # Calculate Manhattan distance for each piece coordinate to the winning location
        for coordinate in piece_coordinates:
            distances = []
            for win_coordinate in winning_location:
                distance = abs(coordinate[0] - win_coordinate[0]) + abs(coordinate[1] - win_coordinate[1])
                distances.append(distance)
            min_distance = min(distances)

            # Update current distance with the minimum distance calculated
            if current_distance < min_distance:
                current_distance = min_distance

        cost_h = current_distance
        
        return cost_h
    

def get_possible_moves(new_game):
    # Get all possible moves for the current game state
    possible_moves = []

    # Iterate through all pieces and directions to generate possible moves
    for piece_id in new_game.pieces:
        for direction in ['up', 'down', 'left', 'right']:
            new_piece_coordenates = new_game.pieces_movements(piece_id, direction)
            if new_game.valid_move(piece_id, new_piece_coordenates) == 'valid':
                possible_moves.append((piece_id, direction))
    
    return possible_moves

def execute_moves(new_game, move):
    # Execute a move for a piece in a given direction
    piece_id = move[0]
    direction = move[1]
    new_piece_coordenates = new_game.pieces_movements(piece_id, direction)
    new_game.update_game_board(piece_id, new_piece_coordenates)
    new_game.update_pieces_coordinates(piece_id, new_piece_coordenates)
    new_game.cost += 1
    