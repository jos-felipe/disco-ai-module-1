#!/usr/bin/env python3
import random
import sys
import argparse
import copy
import time
from collections import deque

class PuzzleState:
    """Represents a state of the 8-puzzle."""
    
    def __init__(self, board, parent=None, move=None, depth=0):
        self.board = board  # 2D list representing the puzzle board
        self.parent = parent  # Parent state that led to this state
        self.move = move  # Move that led to this state ('up', 'down', 'left', 'right')
        self.depth = depth  # Number of moves from initial state
        self.blank_pos = self._find_blank_position()
    
    def _find_blank_position(self):
        """Find the position of the blank (0) tile."""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def get_possible_moves(self):
        """Return a list of valid moves from the current state."""
        moves = []
        i, j = self.blank_pos
        
        # Check up move
        if i > 0:
            moves.append('up')
        
        # Check down move
        if i < 2:
            moves.append('down')
        
        # Check left move
        if j > 0:
            moves.append('left')
        
        # Check right move
        if j < 2:
            moves.append('right')
        
        return moves
    
    def apply_move(self, move):
        """Apply a move to the current state and return the new state."""
        new_board = [row[:] for row in self.board]  # Create a deep copy
        i, j = self.blank_pos
        
        if move == 'up':
            # Swap blank with tile above
            new_board[i][j], new_board[i-1][j] = new_board[i-1][j], new_board[i][j]
        elif move == 'down':
            # Swap blank with tile below
            new_board[i][j], new_board[i+1][j] = new_board[i+1][j], new_board[i][j]
        elif move == 'left':
            # Swap blank with tile to the left
            new_board[i][j], new_board[i][j-1] = new_board[i][j-1], new_board[i][j]
        elif move == 'right':
            # Swap blank with tile to the right
            new_board[i][j], new_board[i][j+1] = new_board[i][j+1], new_board[i][j]
        
        return PuzzleState(new_board, self, move, self.depth + 1)
    
    def __eq__(self, other):
        """Check if two states are equal."""
        return self.board == other.board
    
    def __hash__(self):
        """Hash function for state to use in visited set."""
        return hash(str(self.board))
    
    def __str__(self):
        """String representation of the state."""
        result = ""
        for row in self.board:
            result += " ".join(str(tile) for tile in row) + "\n"
        return result

def generate_random_board():
    """Generate a random 3x3 puzzle board."""
    # Create a solved board
    board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    
    # Apply random moves to shuffle the board
    current_state = PuzzleState(board)
    for _ in range(100):  # Apply 100 random moves
        moves = current_state.get_possible_moves()
        move = random.choice(moves)
        current_state = current_state.apply_move(move)
    
    return current_state.board

def parse_custom_board(input_str):
    """Parse a custom board from a string."""
    rows = input_str.strip().split('\n')
    board = []
    for row in rows:
        board.append([int(tile) for tile in row.split()])
    return board

# The solvability check has been removed

def solve_puzzle_bfs(initial_state):
    """Solve the puzzle using Breadth-First Search to find ALL solutions."""
    goal_board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    if initial_state.board == goal_board:
        return [initial_state], 0, []  # Already solved
    
    # We'll keep track of all solutions found
    all_solutions = []
    all_solution_paths = []  # Store all solution paths
    shortest_length = float('inf')
    
    # BFS setup
    queue = deque([initial_state])
    visited = {hash(str(initial_state.board))}
    
    # We'll set a maximum depth to avoid excessive computation
    max_depth = 31  # This should be more than enough for an 8-puzzle
    
    # Limit the number of solutions we store to avoid memory issues
    max_solutions_to_store = 10
    
    while queue:
        current_state = queue.popleft()
        
        # If we're at the maximum depth, skip
        if current_state.depth >= max_depth:
            continue
        
        # Get all possible moves from the current state
        for move in current_state.get_possible_moves():
            new_state = current_state.apply_move(move)
            
            # Check if we've seen this state before
            new_state_hash = hash(str(new_state.board))
            if new_state_hash in visited:
                continue
            
            # Check if we've reached the goal state
            if new_state.board == goal_board:
                solution_path = trace_solution_path(new_state)
                solution_length = len(solution_path) - 1  # Subtract 1 for initial state
                print(f"Solving in {solution_length} moves")
                
                # Store this solution
                if len(all_solution_paths) < max_solutions_to_store:
                    all_solution_paths.append((solution_path, solution_length))
                
                # Update the shortest solution if needed
                if solution_length < shortest_length:
                    shortest_length = solution_length
                    all_solutions = [solution_path]
                elif solution_length == shortest_length:
                    all_solutions.append(solution_path)
                
                # We don't need to explore further from this goal state
                continue
            
            # Mark as visited and add to queue
            visited.add(new_state_hash)
            queue.append(new_state)
    
    if all_solutions:
        # Sort solutions by length (shortest first)
        all_solution_paths.sort(key=lambda x: x[1])
        return all_solutions[0], shortest_length, all_solution_paths  # Return the first shortest solution and all paths
    return None, -1, []  # No solution found

def trace_solution_path(final_state):
    """Trace the path from the initial state to the goal state."""
    if not final_state:
        return []
    
    # Start from the final state and work backwards
    path = []
    current = final_state
    while current:
        path.append(current)
        current = current.parent
    
    # Reverse the path to get it from initial to goal
    path.reverse()
    return path

def display_puzzle(board):
    """Display the puzzle in a readable format."""
    for row in board:
        print(" ".join(str(tile) for tile in row))

def main():
    parser = argparse.ArgumentParser(description='Advanced 8-Puzzle Solver')
    parser.add_argument('--custom', type=str, help='Custom initial state (e.g., "1 2 3\\n4 0 6\\n7 5 8")')
    parser.add_argument('--file', type=str, help='Read initial state from file')
    args = parser.parse_args()
    
    # Determine the initial board state
    if args.custom:
        initial_board = parse_custom_board(args.custom)
    elif args.file:
        with open(args.file, 'r') as f:
            initial_board = parse_custom_board(f.read())
    else:
        initial_board = generate_random_board()
    
    print("Initial state of the puzzle:")
    display_puzzle(initial_board)
    
    print("Solving the puzzle...")
    
    # The solvability check has been removed
    
    # Solve the puzzle
    initial_state = PuzzleState(initial_board)
    solution_path, shortest_length, all_solution_paths = solve_puzzle_bfs(initial_state)
    
    if solution_path:
        print(f"\nShortest path found: {shortest_length} moves")
        
        # Display only the steps of the shortest path
        # Display the solution steps
        for i, state in enumerate(solution_path):
            if i > 0:  # Skip the initial state since we've already displayed it
                print(f"Step {i}:")
                print(state, end="")
    else:
        print("Puzzle is unsolvable!")

if __name__ == "__main__":
    main()