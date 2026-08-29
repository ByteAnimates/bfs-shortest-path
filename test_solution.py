"""
Run it: python3 test_solution.py   (or: pytest)
"""

from main import dfs_route, shortest_length
from solution import GOAL, START, WALLS, bfs, neighbours, reachable, walk_back


def test_it_returns_a_legal_route():
    route = bfs(START, GOAL)
    assert route[0] == START and route[-1] == GOAL
    assert all(b in neighbours(a) for a, b in zip(route, route[1:]))


def test_the_route_is_the_shortest_one():
    # The claim, checked against an exhaustive ring-by-ring search rather than against
    # another implementation of the same idea.
    assert len(bfs(START, GOAL)) - 1 == shortest_length(START, GOAL)


def test_it_beats_depth_first_search_on_this_board():
    # 13 against 19. The two episodes share a board precisely so this is comparable.
    assert len(bfs(START, GOAL)) - 1 == 13
    assert len(dfs_route(START, GOAL)) - 1 == 19


def test_it_is_shortest_to_every_reachable_square():
    for cell in reachable(START):
        route = bfs(START, cell)
        assert route[0] == START and route[-1] == cell
        assert len(route) - 1 == shortest_length(START, cell), cell


def test_no_route_ever_steps_on_a_wall():
    assert not (set(bfs(START, GOAL)) & WALLS)
    assert not (reachable(START) & WALLS)


def test_an_unreachable_goal_is_refused():
    try:
        walk_back({START: 0}, GOAL)
    except ValueError:
        return
    raise AssertionError('walk_back should refuse a goal it never reached')


if __name__ == '__main__':
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith('test_'):
            fn()
            print(f'  ok  {name}')
            passed += 1
    print(f'\n{passed} tests passed\n')
