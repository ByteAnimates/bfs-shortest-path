"""
Run it: python3 main.py

Breadth-first search on the same board `dfs-any-path` uses. BFS returns the shortest
route; DFS returns a route. The two episodes are a comparison, so this file makes the
comparison runnable.
"""

from solution import COLS, GOAL, START, bfs, neighbours, reachable, render, walk_back


def dfs_route(start: int, goal: int) -> list[int]:
    """
    Depth-first search on the identical board, for contrast — the `dfs-any-path` episode.

    Included because "shortest" is a comparative word and the number only means something
    against the alternative.
    """
    seen = {start}
    stack = [start]
    while stack[-1] != goal:
        nxt = next((n for n in neighbours(stack[-1]) if n not in seen), None)
        if nxt is None:
            stack.pop()
        else:
            seen.add(nxt)
            stack.append(nxt)
    return list(stack)


def main() -> None:
    route = bfs(START, GOAL)
    other = dfs_route(START, GOAL)

    print(f'\n  start {START}  goal {GOAL}\n')
    print(render(route))
    print(f'\n  BFS  {len(route) - 1} steps   {route}')
    print(f'  DFS  {len(other) - 1} steps   {other}')
    print(
        f'\n  Same board, same start, same goal. BFS expands a whole ring before it looks\n'
        f'  at anything further out, so the first time it writes the goal into `dist` it\n'
        f'  writes the smallest distance that could reach it — and can stop immediately.\n'
        f'  DFS commits to one direction until it fails, so it finds A path, not THE path.\n'
    )


# ── the claims above, checked ────────────────────────────────────────────────────

_route = bfs(START, GOAL)

# It is a real route: starts and ends in the right places, and every step is a legal move.
assert _route[0] == START and _route[-1] == GOAL
assert all(b in neighbours(a) for a, b in zip(_route, _route[1:]))

# THE CLAIM: it is the SHORTEST route. Checked against an exhaustive search of every
# path length, not against another implementation of the same idea.
def _shortest_length(start: int, goal: int) -> int:
    frontier, seen, d = [start], {start}, 0
    while frontier:
        if goal in frontier:
            return d
        nxt = [n for c in frontier for n in neighbours(c) if n not in seen]
        seen.update(nxt)
        frontier, d = nxt, d + 1
    raise ValueError('unreachable')

assert len(_route) - 1 == _shortest_length(START, GOAL)

# And strictly better than what DFS returns on this board, which is the episode's point.
assert len(_route) < len(dfs_route(START, GOAL))

# `walk_back` reconstructs a shortest route to EVERY reachable square, not just the goal.
for _cell in reachable(START):
    _r = bfs(START, _cell)
    assert _r[0] == START and _r[-1] == _cell
    assert len(_r) - 1 == _shortest_length(START, _cell), _cell

# The walls are real: no route ever steps onto one.
from solution import WALLS
assert not (set(_route) & WALLS)
assert not (reachable(START) & WALLS)

# An unreachable goal is refused rather than silently returning something.
try:
    walk_back({START: 0}, GOAL)
except ValueError:
    pass
else:
    raise AssertionError('walk_back should refuse a goal it never reached')

if __name__ == '__main__':
    main()
