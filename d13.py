def parse_input(inputfile):
    dots = []
    folds = []
    with open(inputfile) as f:
        read_dots = True
        for line in f.readlines():
            l = line.strip()
            if l == "":
                read_dots = False
                continue
            if read_dots:
                x, y = line.split(',')
                dots.append((int(x), int(y)))
            else:
                axis, val = l.split('=')
                axis = axis[-1]
                val = int(val)
                folds.append((axis,val))
    return dots, folds

def do_folds(_dots, folds):
    dots = _dots.copy()
    for axis, val in folds:
        new_dots = []
        if axis == 'y':
            unmoved_dots = [dot for dot in dots if dot[1] < val]
            for d in [dot for dot in dots if dot[1] > val]:
                diff = abs(d[1] - val) * 2
                folded_dot = (d[0], d[1] - diff)
                new_dots.append(folded_dot)
        else: # x-axis
            unmoved_dots = [dot for dot in dots if dot[0] < val]
            for d in [dot for dot in dots if dot[0] > val]:
                diff = abs(d[0] - val) * 2
                folded_dot = (d[0] - diff, d[1])
                new_dots.append(folded_dot)
        dots = new_dots + unmoved_dots
        dots = list(set(dots)) # cull duplicates
    return dots

def print_paper(dots, width, height):
    for y in range(0, height):
        for x in range(0, width):
            print('#', end='') if (x,y) in dots else print(' ', end='')
        print('\n')

if __name__ == "__main__":
    dots, folds = parse_input("inputs/d13.txt")
    folded_dots = do_folds(dots, folds[:1])
    print(f"Part 1: {len(folded_dots)} dots after 1 fold.")
    folded_dots = do_folds(dots, folds)
    width = min([f[1] for f in folds if f[0] == 'x'])
    height = min([f[1] for f in folds if f[0] == 'y'])
    print (f"\nPart 2:")
    print_paper(folded_dots, width, height)
