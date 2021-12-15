def parse_input(inputfile):
    grid = []
    with open(inputfile) as f:
        for l in f.readlines():
            grid.append([int(c) for c in l.strip()])
    return grid

# I am too dumb to derive Dijkstra's Algorithm myself.
# God bless Reddit and Wikipedia.
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
        v = min(verts, key=lambda v:dists[v])
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

def get_adjacent(x, y, grid_wid):
    deltas = [(0,1),(0,-1),(1,0),(-1,0)]
    candidates = [(x+dx,y+dy) for dx,dy in deltas] # orthogonally adjacent points
    return [pt for pt in candidates if pt[0] >= 0 and pt[0] < grid_wid and pt[1] >= 0 and pt[1] < grid_wid]

def p1_dijkstra(grid):
    end_point = (99,99)
    dists, prevs = dijkstra(grid, (0,0), end_point)
    print(f"Distance = {dists[end_point]}")


if __name__ == "__main__":
    grid = parse_input("inputs/d15.txt")
    p1_dijkstra(grid)
