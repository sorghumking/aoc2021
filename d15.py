def parse_input(inputfile):
    grid = []
    with open(inputfile) as f:
        for l in f.readlines():
            grid.append([int(c) for c in l.strip()])
    return grid

def p1(grid):
    grid_wid = len(grid[0])
    path = []
    risks = []
    walk_grid((0,0), grid, grid_wid, path, risks)
    print(f"{len(risks)} paths walked, lowest risk = {min(risks)}.")

def walk_grid(pos, grid, grid_wid, path, risks):
    path.append(pos)
    if pos == (grid_wid-1, grid_wid-1): # reached lower-right corner
        path_risk = sum([grid[y][x] for x,y in path[1:]]) # skip first pos
        risks.append(path_risk)
    else:
        deltas = []
        if pos[0] + 1 < grid_wid:
            deltas.append((pos[0]+1, pos[1]))
        if pos[1] + 1 < grid_wid:
            deltas.append((pos[0], pos[1]+1))
        for d in deltas:
            walk_grid(d, grid, grid_wid, path, risks)
    path.pop()

if __name__ == "__main__":
    grid = parse_input("inputs/d15ex.txt")
    p1(grid)
    # p2(tmpl, rules, 40)