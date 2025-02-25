# 8-Puzzle Solver

This project implements two 8-puzzle solvers of increasing complexity as part of the Discovery Piscine AI/ML Module 1 on Game Theory.

## Overview

The 8-puzzle is a classic sliding puzzle that consists of a 3×3 grid with 8 numbered tiles and one empty space. The goal is to rearrange the tiles from a given initial configuration to a specific goal configuration by sliding tiles into the empty space.

This repository contains two implementations:

1. **Basic Puzzle Solver (`puzzle_solver.py`)**: Finds a valid solution path to solve the puzzle.
2. **Advanced Puzzle Solver (`puzzle_solver_ad.py`)**: Explores all possible paths to find the shortest solution.

## Features

### Common Features

- Representation of puzzle states with tracking of moves and parent states
- Generation of random initial puzzle configurations
- Support for custom initial states via command line arguments or files
- Breadth-First Search (BFS) algorithm implementation
- Detection of unsolvable puzzles
- Visualization of the puzzle state and solution steps

### Advanced Puzzle Solver Enhancements

- Exploration of all possible paths to find the shortest solution
- Reporting of different solution paths as they are discovered
- Display of the number of moves for each solution found
- Presentation of the shortest solution path in detail

## Technical Implementation

Both solvers use a Breadth-First Search algorithm to explore the puzzle state space. The key components include:

- **PuzzleState class**: Represents a puzzle configuration with methods for:
  - Finding valid moves
  - Applying moves to create new states
  - Tracking the puzzle's solution path

- **BFS algorithm**: Ensures that the first found path to the goal is the shortest one by exploring states in order of their distance from the initial state.

- **Solution tracing**: Tracks the path from the goal state back to the initial state to reconstruct the solution.

## Usage

### Basic Solver

```bash
python3 puzzle_solver.py [--custom "1 2 3\n4 0 6\n7 5 8"] [--file input.txt]
```

### Advanced Solver

```bash
python3 puzzle_solver_ad.py [--custom "1 2 3\n4 0 6\n7 5 8"] [--file input.txt]
```

### Command Line Options

- `--custom`: Specify a custom initial state directly in the command line
- `--file`: Read the initial state from a file

### Example Output

#### Basic Solver

```
Initial state of the puzzle:
1 2 3
4 0 6
7 5 8
Solving the puzzle...
Solution found in 2 steps.
Step 1:
1 2 3
4 5 6
7 0 8
Step 2:
1 2 3
4 5 6
7 8 0
```

#### Advanced Solver

```
Initial state of the puzzle:
1 2 3
4 0 6
7 5 8
Solving the puzzle...
Solving in 2 moves
Shortest path found: 2 moves
Step 1:
1 2 3
4 5 6
7 0 8
Step 2:
1 2 3
4 5 6
7 8 0
```

## Algorithm Details

Both solvers use Breadth-First Search to find solutions, but with different termination conditions:

- The basic solver terminates as soon as it finds a valid solution.
- The advanced solver continues searching to ensure it finds the shortest possible solution.

For the 8-puzzle, BFS guarantees finding the optimal solution because:
1. It explores states in order of their distance from the initial state
2. The first time it reaches the goal state is guaranteed to be via the shortest path
3. It systematically explores all possible moves and positions

## Performance Considerations

- The 8-puzzle has 9!/2 = 181,440 possible states
- The maximum solution length for any 8-puzzle is 31 moves
- The algorithm uses a visited set to avoid exploring the same state multiple times
- For efficiency, a maximum depth limit is implemented to avoid excessive computation

## Project Structure

```
.
├── puzzle_solver.py       # Basic 8-puzzle solver
├── puzzle_solver_ad.py    # Advanced 8-puzzle solver with shortest path finding
└── README.md              # This documentation file
```

## Future Enhancements

Potential improvements for the project could include:

- Implementation of more efficient algorithms like A* with heuristics
- Support for larger puzzles (e.g., 15-puzzle, 24-puzzle)
- Graphical user interface for interactive solving
- Animation of the solution path
- Statistical analysis of puzzle difficulty and solution length

## License

This project is part of the Discovery Piscine AI/ML Module and is intended for educational purposes.

## Acknowledgments

This project was developed as part of the Discovery Piscine AI/ML Module 1 on Game Theory.