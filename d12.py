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
    print(f"Part 1: Found {len(completed)} paths")

def p2(paths):
    all_completed = []
    small_caves = [c for c in paths.keys() if c[0].islower() and c != 'start' and c != 'end']
    for small_cave in small_caves:
        cur_path = []
        completed = []
        explore('start', paths, cur_path, completed, cave_2x=small_cave)
        all_completed += completed
    # remove duplicate paths with set()
    print(f"Part 2: Found {len(all_completed)} paths, {len(set(all_completed))} are unique.")

# Traverse nodes, capturing valid paths from start to end.
# node: current node str
# paths: node adjacency dict
# cur_path: list of nodes in current path
# completed: list of completed paths
# cave_2x: str of small cave node that can be visited twice, or None if no cave can be visited twice
def explore(node, paths, cur_path, completed, cave_2x=None):
    cur_path.append(node)
    for dest_node in paths[node]:
        if dest_node == 'end':
            # add path as tuple for eventual set() call; lists aren't hashable
            valid_path = tuple(cur_path + ['end'])
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
    p1(paths)
    p2(paths)