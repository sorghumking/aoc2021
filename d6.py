def parse_input(inputfile):
    fish = []
    with open(inputfile) as f:
        for l in f.readlines():
            fish = [int(tok) for tok in l.split(',')]
    return fish

# brute force build-a-list-of-every-fish approach
def p1(_fish, days):
    fish = _fish.copy()
    new_count = 0
    for d in range(days):
        fish = [6 if f == 0 else f-1 for f in fish]
        for new in range(new_count):
            fish.append(8)
            new_count = 0
        for idx, f in enumerate(fish):
            if f == 0:
                new_count += 1
    print(f"After {days} days, {len(fish)} fish")

# more efficient approach: group and count fish by remaining days (0-8)
def p2(fish, days):
    state = []
    for num in range(9):
        state.append(len([f for f in fish if f == num]))
    # Now state[0] is the number of fish at day 0...state[8] the number at day 8

    for d in range(days):
        new_fish = state[0] # how many fish at day zero?
        new_state = state[1:] # trim 0th element, shift all others left
        new_state.append(new_fish) # add new fish at 8th element
        new_state[6] += new_fish # add day zero fish back to 6th
        state = new_state
    print(f"After {days} days, {sum(state)} fish")

if __name__ == "__main__":
    fish = parse_input("inputs/d6.txt")
    # fish = [3,4,3,1,2] # example
    p2(fish, days=256)