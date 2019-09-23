import sys
sys.path.append('..')

from nnetwork import life
from nnetwork import neural_network as network
from snapshots import snapshotgen as ssgen
from snapshots import snapshotparse as sspar
from game_2048 import game_AI as game

# Used for getting the move of a 2048 board
# Tranlsates the 2048 board to a stimuli to pass to the AI
# The stimuli is a list of the inputs for the board
def get_move_2048(active_game, active_network):
    stimuli = []
    
    for entry in active_game.curr_board.matrix:
        if entry == 0:
            stimuli.append(0)
        else:
            stimuli.append(1)

    other_stimuli = find_moves_2048_board(active_game.curr_board)

    stimuli += other_stimuli
    return active_network.feed(stimuli)

def find_moves_2048_board(board):
    '''
    classifies the rows and columns of the matrix with a 1 if there is an available move and 0 if there isnt
    Args:
        board (Board Object) - the current game board object
    Returns:
        stimuli (list) - the results of the algorithm, the first four are the rows and the last four are the columns
    Raises:
        None
    '''
    to_return = []
    # For each row, determine if its possible to move
    for row_slice in board.rows:
        row = board.matrix[row_slice]
        if 0 in row:
            to_return.append(1)
        elif can_move(row):
            to_return.append(2)
        else:
            to_return.append(0)
    
    # For each column, determine if its possible to move
    for column_slice in board.columns:
        column = board.matrix[column_slice]
        if 0 in column:
            to_return.append(1)
        elif can_move(column):
            to_return.append(2)
        else:
            to_return.append(0)
    
    return to_return

def can_move(data):
    curr = data[0]
    for entry in data[1:]:
        if curr == entry:
            return True
        else:
            curr = entry
    return False

def game_loop(identifier, individual):
    test_game = game.Game(init_board=init_board.copy())
    return test_game.run(identifier, get_move_2048, individual)

def game_loop_vis(identifier, individual):
    test_game = game.Game_Visual(init_board=init_board.copy())
    return test_game.run(identifier, get_move_2048, individual)

MAX_GENERATIONS = 10
RUNS_PER_IND = 5

# Initialize the game
dummy_game = game.Game()
init_board = dummy_game.curr_board.matrix

# Determine if we are loading from a snapshot
if len(sys.argv) >= 2: 
    parser = sspar.Parser(sys.argv[1])
    parser.build_world()
    exit()
else:
    all_life = life.Life()
    all_life.population = network.create_init_population(30, 
                            [
                            0,0,0,0,
                            0,0,0,0,
                            0,0,0,0,
                            0,0,0,0,
                            0,0,0,0,
                            0,0,0,0
                            ], 
                            ["up", "down", "left", "right"])

# Run the training
all_life.run(game_loop, MAX_GENERATIONS=MAX_GENERATIONS, RUNS_PER_IND=RUNS_PER_IND)

# Run the top networks to show off results
# all_life.run_visualization(game_loop_vis, amount=1)

# Print the top performers
all_life.print_top_performers()

# Print all the genes
all_life.print_genes()

# Print all the species
all_life.print_species_info()

# Generate a snapshot after the current run ends
generator = ssgen.Snapshot(all_life.population, life.Life.species, network.Network.gene_to_innovation_key)
generator.create_snapshot()