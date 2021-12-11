def parse_input(inputfile):
    lines = []
    with open(inputfile) as f:
        lines = [l.strip() for l in f.readlines()]
    return lines

def p1(lines):
    pairs = {'(':')', '[':']', '<':'>', '{':'}'}
    illegals = {')':0, ']':0, '>':0, '}':0}
    good_lines = []
    for line in lines:
        stack = []
        corrupt = False
        for c in line:
            if c in ['(', '[', '<', '{']:
                stack.append(c)
            elif c in [')', ']', '>', '}']:
                assert len(stack) > 0
                if pairs[stack[-1]] == c:
                    stack.pop()
                else:
                    print(f"Corruption: found {c}, expected {pairs[stack[-1]]}")
                    illegals[c] += 1
                    corrupt = True
                    break
        if not corrupt:
            good_lines.append(line)

    score = illegals[')'] * 3 + illegals[']'] * 57 + illegals['}'] * 1197 + illegals['>'] * 25137
    print(f"Total syntax error score = {score}")
    return good_lines

def p2(lines):
    pairs = {'(':')', '[':']', '<':'>', '{':'}'}
    scores = []
    for line in lines:
        stack = []
        for c in line:
            if c in ['(', '[', '<', '{']:
                stack.append(c)
            elif c in [')', ']', '>', '}']:
                assert len(stack) > 0
                if pairs[stack[-1]] == c:
                    stack.pop()
                else:
                    assert False, f"Part 2 unexpected corruption: found {c}, expected {pairs[stack[-1]]}"
        if len(stack) > 0:
            completion = [pairs[c] for c in reversed(stack)]
            scores.append(get_score(completion))
            # print(f"Completion = {''.join(completion)}")
    mid_idx = int((len(scores) - 1) / 2)
    mid_score = sorted(scores)[mid_idx]
    print(f"Middle score = {mid_score}")

def get_score(completion):
    vals = {')':1, ']':2, '}':3, '>':4}
    score = 0
    for c in completion:
        score *= 5
        score += vals[c]
    return score


if __name__ == "__main__":
    lines = parse_input("inputs/d10.txt")
    good_lines = p1(lines)
    p2(good_lines)