def add_key(key, val, dict):
    if key in dict:
        dict[key].append(val)
    else:
        dict[key] = [val]

def parse_input(inputfile):
    paths = {} # key: source node str, value: list of adacent node strs
    with open(inputfile) as f:
        for line in f.readlines():
            l = line.strip()
            src_node, dest_node = l.split('-')
            # add paths from src to dest, and dest to src
            add_key(src_node, dest_node, paths)
            if src_node != 'start': # can't return to 'start', don't add to destinations
                add_key(dest_node, src_node, paths) # reverse path
    return paths

def p1(paths):
    cur_path = []
    completed = []
    explore('start', paths, cur_path, completed)
    return len(completed)

def p2(paths):
    all_completed = []
    small_caves = [c for c in paths.keys() if c[0].islower() and c != 'start' and c != 'end']
    for small_cave in small_caves:
        cur_path = []
        completed = []
        explore('start', paths, cur_path, completed, cave_2x=small_cave)
        all_completed += completed
    return len(all_completed)

# Traverse nodes, capturing valid paths from start to end.
# node: current node str
# paths: node adjacency dict
# cur_path: list of nodes in current path
# completed: list of completed paths
# cave_2x: str of small cave node that can be visited twice, or None if no cave can be visited twice.
# If cave_2x is not None, only paths that visit cave_2x twice are considered valid.
# Without this logic, given three small caves 'a','b','c', both explore(cave_2x='a')
# and explore(cave_2x='b') would capture the routes that visit cave 'c' only once,
# leading to duplicate paths that must be culled.
def explore(node, paths, cur_path, completed, cave_2x=None):
    cur_path.append(node)
    for dest_node in paths[node]:
        if dest_node == 'end':
            if cave_2x is None or (cave_2x is not None and len([n for n in cur_path if n == cave_2x]) == 2):
                valid_path = cur_path + ['end']
                completed.append(valid_path)
            continue
        elif dest_node[0].islower():
            if cave_2x is not None and dest_node == cave_2x:
                if len([n for n in cur_path if n == dest_node]) >= 2:
                    continue
            elif dest_node in cur_path:
                continue
        explore(dest_node, paths, cur_path, completed, cave_2x)
    cur_path.pop()

if __name__ == "__main__":
    paths = parse_input("inputs/d12.txt")
    p1_count = p1(paths)
    print(f"Part 1: Found {p1_count} paths that visit small caves 0-1x.")
    p2_count = p2(paths)
    print(f"Part 2: Found {p2_count} paths that visit one small cave exactly 2x.")
    print(f"Part 2 answer = P1 + P2 = {p1_count + p2_count}.")