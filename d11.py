def parse_input(inputfile):
    grid = []
    with open(inputfile) as f:
        for line in f.readlines():
            grid.append([int(c) for c in line.strip()])
    return grid

def p1(grid, width, max_step, do_part_2=False):
    step = 0
    flash_count = 0
    while step < max_step:
        # increment all octos by 1
        for y in range(width):
            for x in range(width):
                grid[y][x] += 1

        while True: # until no new flashes
            # gather flashing octos
            flashes = []
            for y in range(width):
                for x in range(width):
                    if grid[y][x] > 9:
                        flashes.append((x,y))
                        grid[y][x] = -1 # mark as flashed by setting negative

            if len(flashes) > 0: # there were flashes, increment flash-adjacent octos
                for fx,fy in flashes:
                    for ax,ay in get_adjacent(fx,fy,width):
                        if grid[ay][ax] >= 0: # don't increment negative (already-flashed) octos
                            grid[ay][ax] += 1
            else: # no flashes, set flashed octos to 0 and wrap up this step
                step_flash_count = 0
                for y in range(width):
                    for x in range(width):
                        if grid[y][x] < 0:
                            grid[y][x] = 0
                            flash_count += 1
                            step_flash_count += 1
                step += 1
                if do_part_2 and step_flash_count == width*width: # did all octos flash?
                    print(f"Part 2: all octos flashed after step {step}.")
                    step = max_step # force end of top-level while loop
                # print(f"After step {step}:")
                # print_grid(grid)
                break
    if not do_part_2:
        print(f"Part 1: {flash_count} flashes after step {step}.")

def get_adjacent(x, y, width):
    deltas = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    pts = [(x+dx, y+dy) for dx,dy in deltas if x+dx >= 0 and x+dx < width and y+dy >= 0 and y+dy < width]
    return pts

def print_grid(grid):
    for row in grid:
        print(''.join([str(c) for c in row]))

if __name__ == "__main__":
    grid = parse_input("inputs/d11.txt")
    width = len(grid[0])
    p1(grid, width, max_step=100)
    p1(grid, width, max_step=1000, do_part_2=True)