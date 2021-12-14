from collections import Counter

def parse_input(inputfile):
    tmpl = None
    rules = {} # key=pair : value=char to insert
    with open(inputfile) as f:
        for idx, line in enumerate(f.readlines()):
            if idx == 0:
                tmpl = line.strip()
            elif idx >= 2:
                tokens = line.strip().split(' -> ')
                rules[tokens[0]] = tokens[1]
    return tmpl, rules

def p1(_tmpl, rules, steps):
    tmpl = _tmpl
    for step in range(steps):
        tmpl = do_insertion(tmpl, rules)
    counts = Counter(tmpl)
    max_elt = max(counts, key=counts.get)
    max_count = counts[max_elt]
    min_elt = min(counts, key=counts.get)
    min_count = counts[min_elt]
    diff = max_count - min_count
    print(f"Part 1: after {steps} steps, most common ({max_elt}, {max_count}) - least common ({min_elt}, {min_count}) = {diff}.")

def do_insertion(tmpl, rules):
    result = ""
    for idx in range(len(tmpl) - 1):
        cur_pair = tmpl[idx:idx+2]
        assert cur_pair in rules, f"Pair {cur_pair} not found in rules!"
        result += (cur_pair[0] + rules[cur_pair])
        if idx == len(tmpl) - 2: # last iteration, append last char
            result += cur_pair[1]
    return result

def p2(tmpl, rules, steps):
    # init count dicts
    char_counts = Counter(tmpl) # count chars in template string
    pair_counts = {pair:0 for pair in rules.keys()} # init all pairs to 0, then count pairs in template string
    for pair in [tmpl[idx] + tmpl[idx+1] for idx in range(len(tmpl) - 1)]:
        pair_counts[pair] += 1

    for step in range(steps):
        do_insertion_v2(tmpl, rules, char_counts, pair_counts)

    counts = Counter(char_counts)
    max_elt = max(counts, key=counts.get)
    max_count = char_counts[max_elt]
    min_elt = min(counts, key=counts.get)
    min_count = char_counts[min_elt]
    diff = max_count - min_count
    print(f"Part 2: After {steps} steps, most common ({max_elt}, {max_count}) - least common ({min_elt}, {min_count}) = {diff}.")

# Instead of rebuilding template string each step, track count of each character
# and each pair of characters.
def do_insertion_v2(tmpl, rules, char_counts, pair_counts):
    pair_deltas = {pair:0 for pair in pair_counts.keys()} # track change in pair counts
    for pair, count in pair_counts.items():
        if count == 0:
            continue
        # get the two new pairs i.e. AB -> C = AC, CB
        new_char = rules[pair]
        pair1 = pair[0] + new_char
        pair2 = new_char + pair[1]
        # increase counts of the new pairs
        pair_deltas[pair1] += count
        pair_deltas[pair2] += count
        # reduce count of the original pair
        pair_deltas[pair] -= count
        # increment char count of added char
        char_counts[new_char] += count
    for pair, delta in pair_deltas.items(): # apply deltas
        pair_counts[pair] += delta


if __name__ == "__main__":
    tmpl, rules = parse_input("inputs/d14.txt")
    p1(tmpl, rules, 10)
    p2(tmpl, rules, 40)