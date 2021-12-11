def parse_input(inputfile):
    heights = []
    with open(inputfile) as f:
        for l in f.readlines():
            row = [int(c) for c in l.strip()]
            heights.append(row)
    return heights

def get_adjacent_heights(x, y, heights):
    return [heights[ay][ax] for ax, ay in get_adjacent_points(x, y, heights)]

def get_adjacent_points(x, y, heights):
    deltas = [(0,1),(0,-1),(1,0),(-1,0)]
    candidates = [(x+dx,y+dy) for dx,dy in deltas] # orthogonally adjacent points
    max_x = len(heights[0])
    max_y = len(heights)
    # cull points outside of grid
    adj = [pt for pt in candidates if pt[0] >= 0 and pt[0] < max_x and pt[1] >= 0 and pt[1] < max_y]
    return adj

def p1(heights):
    low_points = []
    for y, row in enumerate(heights):
        for x, h in enumerate(row):
            adj_test = [h < v for v in get_adjacent_heights(x, y, heights)]
            if False not in adj_test:
                low_points.append((x,y))
    return low_points

# Recurse through points adjacent to (x,y), stopping at height 9
def get_basin(x, y, heights, visited):
    if (x,y) in visited:
        return
    visited.append((x,y))
    adj = get_adjacent_points(x, y, heights)
    for adj_x, adj_y in adj:
        if heights[adj_y][adj_x] != 9:
            get_basin(adj_x, adj_y, heights, visited)

def p2(low_points, heights):
    basins = []
    for low_x, low_y in low_points:
        visited = []
        basin_pts = get_basin(low_x, low_y, heights, visited)
        basins.append(visited)
        # print(f"Low point ({low_x}, {low_y}) has basin {visited} len {len(visited)}")
    big3 = sorted(basins, key=lambda b:len(b), reverse=True)[:3]
    print(f"Product of three largest basins = {len(big3[0]) * len(big3[1]) * len(big3[2])}")
    

if __name__ == "__main__":
    heights = parse_input("inputs/d9.txt")
    low_points = p1(heights)
    risk = sum([heights[y][x] + 1 for x,y in low_points])
    print(f"Total risk = {risk}")
    p2(low_points, heights)