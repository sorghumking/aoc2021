import time
import heapq

def parse_input(inputfile):
    grid = []
    with open(inputfile) as f:
        for l in f.readlines():
            grid.append([int(c) for c in l.strip()])
    return grid

# I am too dumb to derive Dijkstra's Algorithm myself, but here is my
# incredibly slow implementation. God bless Reddit and Wikipedia.
def dijkstra(grid, start_pos, end_pos):
    verts = set()
    dists = {}
    prevs = {}

    for y in range(len(grid[0])):
        for x in range(len(grid[0])):
            dists[(x,y)] = float('inf') # infinity
            prevs[(x,y)] = None
            verts.add((x,y))
    dists[start_pos] = 0
    
    grid_wid = len(grid[0])
    while len(verts) > 0:
        if len(verts) % 1000 == 0:
            print(f"{len(verts)}, ", end='')
        v = min(verts, key=lambda v:dists[v]) # this is the bottleneck
        verts.remove(v)
        if v == end_pos:
            break
        for pt in get_adjacent(v[0], v[1], grid_wid):
            if pt in verts:
                new_dist = dists[v] + grid[pt[1]][pt[0]]
                if new_dist < dists[pt]:
                    dists[pt] = new_dist
                    prevs[pt] = v
    return dists, prevs

# My impl is way too slow for Part 2!
# A heapq-based impl of Dijkstra's cribbed from StackOverflow,
# with a tweak to not add the first point's risk.
def dijkstra_heapq(grid, start_pos, end_pos):
    verts = [(0, start_pos, [])]
    dists = {}
    for y in range(len(grid[0])):
        for x in range(len(grid[0])):
            dists[(x,y)] = float('inf') # infinity
    dists[start_pos] = 0
    seen = set()
    grid_wid = len(grid[0])
    while True:
        risk, v, path = heapq.heappop(verts)
        if v not in seen:
            seen.add(v)
            if v == end_pos:
                risk += grid[v[1]][v[0]]
                return risk, path + [v]
            for pt in get_adjacent(v[0], v[1], grid_wid):
                new_risk = grid[v[1]][v[0]] if v != start_pos else 0 # don't add risk of start_pos
                if risk + new_risk < dists[pt]:
                    dists[pt] = risk + new_risk
                    heapq.heappush(verts, (risk + new_risk, pt, path + [v]))


def get_adjacent(x, y, grid_wid):
    deltas = [(0,1),(0,-1),(1,0),(-1,0)]
    candidates = [(x+dx,y+dy) for dx,dy in deltas] # orthogonally adjacent points
    return [pt for pt in candidates if pt[0] >= 0 and pt[0] < grid_wid and pt[1] >= 0 and pt[1] < grid_wid]

def p1_dijkstra(grid, end_point):
    risk, path = dijkstra_heapq(grid, (0,0), end_point)
    print(f"Part 1: Risk = {risk}")
    print(f"Path = {path}")

def p2_dijkstra(megagrid, end_point):
    risk, path = dijkstra_heapq(megagrid, (0,0), end_point)
    print(f"Part 2: Risk = {risk}")
    print(f"Part 2: Path 1-10 {path[:10]}, last ten {path[len(path)-10:]}")

def make_megagrid(grid):
    megagrid = []
    for yoff in range(5):
        for row in grid:
            megarow = []
            for xoff in range(5):
                megarow += [increase_risk(risk, xoff+yoff) for risk in row]
            megagrid.append(megarow)
    return megagrid

def increase_risk(risk, amt):
    return risk+amt if risk+amt <= 9 else ((risk+amt) % 9)


if __name__ == "__main__":
    grid = parse_input("inputs/d15.txt")
    p1_dijkstra(grid, (99,99))
    megagrid = make_megagrid(grid)
    p2_dijkstra(megagrid, (499,499))
