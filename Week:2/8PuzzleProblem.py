# 8-Puzzle Problem using Depth First Search (DFS)

class PuzzleState:
    def __init__(self, board, parent=None, move="", depth=0):
        self.board = board       # Current board configuration as a 1D list
        self.parent = parent     # Pointer to the previous state (Parent Node)
        self.move = move         # The move made to reach this state (Up, Down, Left, Right)
        self.depth = depth       # Current depth level in the search tree

    # Check if two states are identical
    def __eq__(self, other):
        return self.board == other.board

    # Hash function to store states in a set (for visited tracking)
    def __hash__(self):
        return hash(tuple(self.board))

# Generate all possible valid moves (successors) from the current state
def get_successors(state):
    successors = []
    board = state.board
    blank_idx = board.index(0)  # Find the index of the blank tile '0'
    row, col = divmod(blank_idx, 3)  # Convert 1D index to 2D (row, col)

    # Define moves with their row and column changes
    moves = {
        "Up": (-1, 0),
        "Down": (1, 0),
        "Left": (0, -1),
        "Right": (0, 1)
    }

    for move_name, (dr, dc) in moves.items():
        new_row, new_col = row + dr, col + dc
        
        # Ensure the move stays within the boundaries of the 3x3 board
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank_idx = new_row * 3 + new_col
            
            # Create a copy of the board and swap the blank space with the target tile
            new_board = list(board)
            new_board[blank_idx], new_board[new_blank_idx] = new_board[new_blank_idx], new_board[blank_idx]
            
            # Append the new state
            successors.append(PuzzleState(new_board, state, move_name, state.depth + 1))
            
    return successors

# DFS Solver Algorithm
def dfs_solver(start_board, goal_board, max_depth=20):
    start_state = PuzzleState(start_board)
    
    stack = [start_state]       # Use a Python list as a LIFO stack for DFS
    visited = set()             # Keep track of already visited board states
    
    while stack:
        current_state = stack.pop()
        
        # If the goal state is reached, reconstruct the path
        if current_state.board == goal_board:
            path = []
            while current_state.parent:
                path.append(current_state.move)
                current_state = current_state.parent
            return path[::-1]  # Reverse the path to get the correct chronological order
        
        # Process the state if it hasn't been visited and is within depth limits
        if current_state not in visited and current_state.depth < max_depth:
            visited.add(current_state)
            
            # Add all non-visited neighbor states to the stack
            for successor in get_successors(current_state):
                if successor not in visited:
                    stack.append(successor)
                    
    return None  # Return None if no solution is found within the depth limit

# Helper function to pretty-print the board as a 3x3 matrix
def print_board(board):
    for i in range(0, 9, 3):
        print(board[i:i+3])
    print()

# Main execution block
if __name__ == "__main__":
    # '0' represents the blank/empty space
    # Simple configuration that is solvable within low depth limits
    initial_state = [1, 2, 3, 
                     0, 4, 6, 
                     7, 5, 8]
    
    goal_state =    [1, 2, 3, 
                     4, 5, 6, 
                     7, 8, 0]

    print("Initial State:")
    print_board(initial_state)
    
    print("Goal State:")
    print_board(goal_state)

    print("Searching for a solution using DFS...")
    solution = dfs_solver(initial_state, goal_state, max_depth=25)

    if solution:
        print(f"Solution Found! Total Moves: {len(solution)}")
        print("Sequence of moves:", solution)
    else:
        print("No solution found within the specified Max Depth limit.")
