# Return list of lines [[x1,y1],[x2,y2]]
def parse_input(inputfile):
    lines = []
    with open(inputfile) as f:
        for l in f.readlines():
            toks = l.split(" -> ")
            pt1 = [int(t) for t in toks[0].split(',')]
            pt2 = [int(t) for t in toks[1].split(',')]
            lines.append([pt1, pt2])
    return lines

def count_vents(lines, count_diagonals):
    vent_coords = {}
    for pt1, pt2 in lines:
        if pt1[0] == pt2[0]: # vertical
            x = pt1[0]
            ymin = min(pt1[1], pt2[1])
            ymax = max(pt1[1], pt2[1])
            for y in range(ymin, ymax+1):
                add_vent((x,y), vent_coords)
        elif pt1[1] == pt2[1]: # horizontal
            y = pt1[1]
            xmin = min(pt1[0], pt2[0])
            xmax = max(pt1[0], pt2[0])
            for x in range(xmin, xmax+1):
                add_vent((x,y), vent_coords)
        elif count_diagonals:
            dx = 1 if pt1[0] < pt2[0] else -1
            dy = 1 if pt1[1] < pt2[1] else -1
            for count in range(abs(pt1[0] - pt2[0]) + 1):
                pt = (pt1[0] + (dx*count), pt1[1] + (dy*count))
                add_vent(pt, vent_coords)
    return vent_coords

def add_vent(pt, vent_coords):
    if pt in vent_coords:
        vent_coords[pt] += 1
    else:
        vent_coords[pt] = 1

if __name__ == "__main__":
    lines = parse_input("inputs/d5.txt")
    vent_coords = count_vents(lines, count_diagonals=False)
    overlap_count = len([v for v in vent_coords.values() if v > 1])
    print(f"Part 1: Found {overlap_count} points with 2+ lines")

    vent_coords = count_vents(lines, count_diagonals=True)
    overlap_count = len([v for v in vent_coords.values() if v > 1])
    print(f"Part 2: Found {overlap_count} points with 2+ lines")
