# return list of ([str: first char of command], [int: amount]) tuples
def parse_input(inputfile):
    commands = []
    with open(inputfile) as f:
        for line in f.readlines():
            toks = line.split()
            cmd = toks[0].strip()[:1] # grab first char of command
            amt = int(toks[1].strip())
            commands.append((cmd, amt))
    return commands

def p1(commands):
    horz = 0
    depth = 0
    for cmd, amt in commands:
        if cmd == 'f':
            horz += amt
        elif cmd == 'd':
            depth += amt
        elif cmd == 'u':
            depth -= amt
    print("Part 1: Position: {}, depth: {}, product = {}".format(horz, depth, horz*depth))

def p2(commands):
    aim = 0
    horz = 0
    depth = 0
    for cmd, amt in commands:
        if cmd == 'f':
            horz += amt
            depth += aim * amt
        elif cmd == 'd':
            aim += amt
        elif cmd == 'u':
            aim -= amt
    print("Part 2 Position: {}, depth: {}, product = {}".format(horz, depth, horz*depth))


if __name__ == "__main__":
    commands = parse_input("inputs/d2.txt")
    p1(commands)
    p2(commands)
