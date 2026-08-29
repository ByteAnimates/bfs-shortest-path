"""
Run it: python3 main.py

Breadth-first search on the same board `dfs-any-path` uses. BFS returns the shortest
route; DFS returns a route. The two episodes are a comparison, so this file makes the
comparison runnable.
"""

from solution import COLS, GOAL, START, bfs, neighbours, reachable, render, walk_back


def shortest_length(start: int, goal: int) -> int:
    """
    The shortest route length, found by expanding rings and counting them.

    A second, dumber implementation on purpose: checking `bfs` against something that
    shares its helpers would only prove the helpers agree with themselves.
    """
    frontier, seen, d = [start], {start}, 0
    while frontier:
        if goal in frontier:
            return d
        nxt = [n for c in frontier for n in neighbours(c) if n not in seen]
        seen.update(nxt)
        frontier, d = nxt, d + 1
    raise ValueError(f'{goal} is unreachable from {start}')


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



if __name__ == '__main__':
    main()
