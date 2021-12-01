def parse_input(inputfile):
    depths = []
    with open(inputfile) as f:
        for line in f.readlines():
            depths.append(int(line.strip()))
    return depths

def p1(depths):
    increases = 0
    for idx, _ in enumerate(depths):
        if idx > 0 and depths[idx] > depths[idx-1]:
            increases += 1
    return increases

def p2(depths):
    increases = 0
    for idx, _ in enumerate(depths):
        if idx >= 3 and sum(depths[idx-2:idx+1]) > sum(depths[idx-3:idx]):
            increases += 1
    return increases

if __name__ == "__main__":
    # depths = [199,200,208,210,200,207,240,269,260,263]
    depths = parse_input("inputs/d1.txt")
    print(f"{p1(depths)} increases")
    print(f"{p2(depths)} increases with with sliding window.")