# Snake and Ladder: Minimum Dice Throws using BFS

This project finds the **minimum number of dice throws** required to travel
from square `1` to the final square of a Snake and Ladder board. It uses
**Breadth-First Search (BFS)** and Python's standard library only.

## Features

- Generates a sample board with random snakes and ladders.
- Uses BFS to find the minimum number of dice throws.
- Prints the board's snake and ladder jumps.
- Displays the minimum throw count and one optimal route.
- Supports different board sizes and repeatable random boards using a seed.
- No third-party packages are needed.

## Requirements

- Python 3.8 or newer
- No external dependencies

## Run the project

In a terminal opened in this folder:

```bash
python snake_ladder_bfs.py
```

Use a smaller board and repeatable jumps:

```bash
python snake_ladder_bfs.py --size 30 --seed 42
```

Use the standard 100-square board without listing every jump:

```bash
python snake_ladder_bfs.py --size 100 --no-board
```

## How it works

### 1. Model the board as a graph

Each square is a vertex. From a square `u`, a dice throw can move to any
square from `u + 1` to `u + 6`, provided the destination does not exceed the
last square. If the landing square is the start of a snake or ladder, the
player moves immediately to that jump's destination.

### 2. Apply Breadth-First Search

BFS explores reachable squares in increasing order of the number of dice
throws needed to reach them. It uses a queue to process positions in
first-in, first-out order and a visited set to avoid repeatedly exploring
squares. A parent map is used to reconstruct one optimal route.

Because every dice throw counts as one edge, BFS finds the minimum number of
throws.

## Complexity analysis

Let `N` be the number of squares.

- **Time complexity:** `O(N)` for a board with a fixed six-sided die.
- **Space complexity:** `O(N)` for the queue, visited set, and parent map.

Each square is visited at most once, and each visited square considers at
most six dice outcomes.

## Example output (format)

```text
SNAKE AND LADDER: MINIMUM DICE THROWS USING BFS
Board: squares 1 to 100

Ladders (start -> destination):
   14 -> 35
   ...

Snakes (head -> tail):
   48 -> 12
   ...

Result:
Minimum dice throws: 7
One optimal route (square positions after each throw):
1 -> 7 -> 13 -> 35 -> ...

Note: a snake or ladder is applied immediately after landing.
```

The exact jumps, route, and answer depend on the generated board and seed.
The output above is illustrative.

## Project structure

```text
snake_ladder_bfs_project/
├── snake_ladder_bfs.py
└── README.md
```

## Assumptions

- The game starts on square `1` and ends at the final square.
- The die has faces 1 through 6.
- A throw that would move beyond the final square is not allowed.
- Snakes and ladders are applied immediately after landing.
- Each dice throw has equal cost, making BFS appropriate for the minimum path.
