"""
Snake and Ladder: Minimum Dice Throws using Breadth-First Search (BFS)
------------------------------------------------------------------------
Find the minimum number of dice throws needed to reach the final square.
Uses the standard BFS approach for an unweighted graph.

Run:
    python snake_ladder_bfs.py
    python snake_ladder_bfs.py --size 30 --seed 42
    python snake_ladder_bfs.py --size 100 --no-board
"""

import argparse
import random
from collections import deque
from typing import Dict, List, Optional, Tuple

JumpMap = Dict[int, int]


def generate_jumps(size: int = 100, seed: Optional[int] = None) -> JumpMap:
    """
    Create a sample board with random snakes and ladders.

    Squares 1 and `size` are excluded from jumps. Jump starts and destinations
    are unique to keep the sample board easy to understand.
    """
    rng = random.Random(seed)
    jumps: JumpMap = {}
    available_starts = list(range(2, size))
    rng.shuffle(available_starts)

    # Keep a reasonable number of jumps for small boards too.
    count = min(max(2, size // 10), max(0, (size - 2) // 2))
    used_destinations = set()

    for start in available_starts:
        if len(jumps) >= count:
            break

        # About half ladders, half snakes. Ladders go up; snakes go down.
        if len(jumps) % 2 == 0:
            possible = [d for d in range(start + 1, size)
                        if d not in used_destinations and d not in jumps]
        else:
            possible = [d for d in range(2, start)
                        if d not in used_destinations and d not in jumps]

        if not possible:
            continue

        destination = rng.choice(possible)
        jumps[start] = destination
        used_destinations.add(destination)

    return jumps


def minimum_dice_throws(size: int, jumps: JumpMap) -> Tuple[Optional[int], List[int]]:
    """
    Use BFS to calculate the minimum dice throws from square 1 to `size`.

    Returns (throw_count, route). The route includes each landing square after
    a dice throw, and jump destinations are shown as actual positions reached.
    If the end cannot be reached, returns (None, []).
    """
    if size < 2:
        raise ValueError("Board size must be at least 2.")

    # Queue items are (square, number of throws).
    queue = deque([(1, 0)])
    visited = {1}
    parent: Dict[int, Optional[int]] = {1: None}
    throw_count: Dict[int, int] = {1: 0}

    while queue:
        square, throws = queue.popleft()
        if square == size:
            route = []
            current: Optional[int] = size
            while current is not None:
                route.append(current)
                current = parent[current]
            route.reverse()
            return throws, route

        for dice in range(1, 7):
            landing = square + dice
            if landing > size:
                continue

            # Apply a snake or ladder immediately after landing.
            destination = jumps.get(landing, landing)
            if destination in visited:
                continue

            visited.add(destination)
            parent[destination] = square
            throw_count[destination] = throws + 1
            queue.append((destination, throws + 1))

    return None, []


def print_board(size: int, jumps: JumpMap) -> None:
    """Print a compact list of snakes and ladders."""
    ladders = sorted((start, end) for start, end in jumps.items() if end > start)
    snakes = sorted((start, end) for start, end in jumps.items() if end < start)

    print(f"Board: squares 1 to {size}")
    print("\nLadders (start -> destination):")
    if ladders:
        for start, end in ladders:
            print(f"  {start:>3} -> {end}")
    else:
        print("  None")

    print("\nSnakes (head -> tail):")
    if snakes:
        for start, end in snakes:
            print(f"  {start:>3} -> {end}")
    else:
        print("  None")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find the minimum dice throws in Snake and Ladder using BFS."
    )
    parser.add_argument("--size", type=int, default=100,
                        help="number of board squares (default: 100)")
    parser.add_argument("--seed", type=int, default=None,
                        help="optional seed for repeatable random jumps")
    parser.add_argument("--no-board", action="store_true",
                        help="skip listing the snakes and ladders")
    args = parser.parse_args()

    if args.size < 2:
        parser.error("--size must be at least 2")

    jumps = generate_jumps(args.size, args.seed)

    print("SNAKE AND LADDER: MINIMUM DICE THROWS USING BFS")
    if not args.no_board:
        print_board(args.size, jumps)

    result, route = minimum_dice_throws(args.size, jumps)
    print("\nResult:")
    if result is None:
        print("The final square cannot be reached with this board.")
    else:
        print(f"Minimum dice throws: {result}")
        print("One optimal route (square positions after each throw):")
        print(" -> ".join(map(str, route)))
        print("\nNote: a snake or ladder is applied immediately after landing.")


if __name__ == "__main__":
    main()
