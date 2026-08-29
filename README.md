# Breadth-First Search

**O(cells)** · [Watch the reel](https://www.facebook.com/reel/1541312373590517)

The working code from the [@ByteAnimates](https://www.facebook.com/ByteAnimates) reel.

```bash
python3 main.py
python3 test_solution.py
```

No dependencies. Python 3.9+.

### As shown in the reel

The panel holds twelve lines, so `grow` and `walk_back` were named on screen but not written.
`solution.py` writes them, under those same names.

```python
def bfs(start, goal):
    dist = {start: 0}
    while goal not in dist:
        grow(dist)
    return walk_back(dist, goal)
```

### Files

| | |
| --- | --- |
| `main.py` | run this — the demo, with real inputs and the claims asserted |
| `solution.py` | the working implementation, with the helpers the reel named |
| `test_solution.py` | the properties, checked — they survive a rewrite |

---

The snippet above is generated from the video itself — what you read is byte-for-byte
what was typed on screen. A fix to it belongs in the episode, so open an issue and the
next reel carries it. Everything else here is hand-written and welcome as a pull request.
