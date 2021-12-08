def parse_input(inputfile):
    entries = []
    with open(inputfile) as f:
        for l in f.readlines():
            patterns = (l.split(' | ')[0].strip()).split(' ')
            output = (l.split(' | ')[1].strip()).split(' ')
            entries.append((patterns, output))
    return entries

def p1(entries):
    count = 0
    for _, output in entries:
        for digits in output:
            if len(digits) in [2,3,4,7]:
                count += 1
    return count

def p2(entries):
    total = 0
    for patterns, output in entries:
        known = {} # key:known digit, value:pattern
        fives = [] # patterns of length five
        sixes = [] # patterns of length six
        for p in patterns:
            if len(p) == 2:
                known[1] = p
            elif len(p) == 3:
                known[7] = p
            elif len(p) == 4:
                known[4] = p
            elif len(p) == 7:
                known[8] = p
            elif len(p) == 5:
                fives.append(p)
            elif len(p) == 6:
                sixes.append(p)
        decode_fives(fives, known)
        decode_sixes(sixes, known)
        total += output_value(output, known)
    return total

def output_value(output, known):
    value = ''
    for digit in output:
        for k, v in known.items():
            if set(digit) == set(v):
                value += str(k)
    return int(value)

# five-segment numbers are 2, 3, and 5
def decode_fives(fives, known):
    # 3 has both segments of 1
    one = known[1]
    for idx, f in enumerate(fives):
        if one[0] in f and one[1] in f:
            break
    known[3] = fives.pop(idx)

    # 5 has three segments of 4 (2 has two)
    four = known[4]
    for idx, f in enumerate(fives):
        matches = [c for c in four if c in f]
        if len(matches) == 3:
            break
    known[5] = fives.pop(idx)
    known[2] = fives[0] # 2 leftover

# six-segment numbers are 0, 6, and 9
def decode_sixes(sixes, known):
    # 6 has only one segment in common with 1
    one = known[1]
    for idx, s in enumerate(sixes):
        if not (one[0] in s and one[1] in s):
            break
    known[6] = sixes.pop(idx)
    
    # 9 has all the segments of 4
    four = known[4]
    for idx, s in enumerate(sixes):
        matches = [c for c in four if c in s]
        if len(matches) == 4:
            break
    known[9] = sixes.pop(idx)
    known[0] = sixes[0] # 0 leftover


if __name__ == "__main__":
    entries = parse_input("inputs/d8.txt")
    count = p1(entries)
    print(f"Total 1,4,7,8 digits in output values = {count}")
    total = p2(entries)
    print(f"Total of values = {total}")