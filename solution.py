"""
The working version of what the reel shows.

The reel's `bfs()` fits in five lines because two things are named but not written:
`grow`, which pushes the frontier out by one ring, and `walk_back`, which turns the
distance map into a route. Both are here, under those names.

WHY A RING AT A TIME IS THE WHOLE ALGORITHM. `grow` expands every cell at the current
distance before it touches any cell one further out, so the first time the goal is
written into `dist` it is written with the smallest distance that could possibly reach
it. Nothing later can improve on it, which is why BFS can stop the moment it arrives and
why it needs no priority queue to do it — on an unweighted grid, ring order IS cost order.

That guarantee is exactly what depth-first search gives up, and why it finds a path
rather than the shortest one. Same board, both episodes.
"""

COLS = 8
ROWS = 4

#: Squares nothing can enter. Identical to the `dfs-any-path` board on purpose — the two
#: episodes are a comparison, and changing the maze would forfeit it.
WALLS = frozenset({2, 10, 18, 13, 21, 29})

START = 8
GOAL = 15


def neighbours(i: int) -> list[int]:
    """Up, down, left, right. Walls and the edges of the board are not neighbours."""
    r, c = divmod(i, COLS)
    out = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            n = nr * COLS + nc
            if n not in WALLS:
                out.append(n)
    return out


def grow(dist: dict[int, int]) -> None:
    """
    Push the frontier out by exactly one ring. Mutates `dist`, as the snippet expects.

    Every cell at the current maximum distance gets its unvisited neighbours written in
    at one more. Doing a whole ring per call is what keeps the distances correct: a cell
    is written once, by the first ring that reaches it.
    """
    edge = max(dist.values())
    frontier = [c for c, d in dist.items() if d == edge]
    for cell in frontier:
        for n in neighbours(cell):
            if n not in dist:
                dist[n] = edge + 1


def walk_back(dist: dict[int, int], goal: int) -> list[int]:
    """
    The route, rebuilt from the distances alone — no predecessor map needed.

    From the goal, step to any neighbour whose distance is one less, and repeat. That
    neighbour must be on a shortest path, because it was reached one ring earlier. This
    is the trick that lets `bfs` carry a single dict instead of two.
    """
    if goal not in dist:
        raise ValueError(f'{goal} was never reached')
    route = [goal]
    while dist[route[-1]]:
        here = route[-1]
        route.append(next(n for n in neighbours(here) if dist.get(n) == dist[here] - 1))
    return route[::-1]


def bfs(start: int, goal: int) -> list[int]:
    """Line for line what is on screen, with `grow` and `walk_back` filled in."""
    dist = {start: 0}
    while goal not in dist:
        grow(dist)
    return walk_back(dist, goal)


def reachable(start: int) -> set[int]:
    """Everything the board can get to from `start`, for checking the walls are honest."""
    dist = {start: 0}
    while True:
        before = len(dist)
        grow(dist)
        if len(dist) == before:
            return set(dist)


def render(route: list[int]) -> str:
    """The board with the route on it."""
    marks = {c: str(i % 10) for i, c in enumerate(route)}
    rows = []
    for r in range(ROWS):
        cells = []
        for c in range(COLS):
            i = r * COLS + c
            cells.append('##' if i in WALLS else f'{marks.get(i, " ."):>2}')
        rows.append(' '.join(cells))
    return '\n'.join(rows)
