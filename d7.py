def parse_input(inputfile):
    crabs = []
    with open(inputfile) as f:
        for l in f.readlines():
            crabs = [int(tok) for tok in l.split(',')]
    return crabs

def min_fuel_cost(crabs, fuel_calc):
    min_cost = None
    max_pos = max(crabs)
    for dest in range(max_pos+1):
        fuel_cost = sum([fuel_calc(dest, pos) for pos in crabs])
        if min_cost is None or fuel_cost < min_cost:
            min_cost = fuel_cost
    return min_cost

# Return fuel cost for moving from pos to dest, where each move
# costs 1 more fuel than preceding move.
def get_fuel_cost(dest, pos):
    a = 0
    l = abs(dest - pos)
    n = l - a + 1
    return int((n * (a + l)) / 2)

if __name__ == "__main__":
    # crabs = [16,1,2,0,4,2,7,1,2,14] # example
    crabs = parse_input("inputs/d7.txt")
    p1 = min_fuel_cost(crabs, fuel_calc=lambda dest, pos: abs(dest-pos))
    print(f"Part 1: minimum total fuel = {p1}")
    p2 = min_fuel_cost(crabs, get_fuel_cost)
    print(f"Part 2: minimum total fuel = {p2}")

