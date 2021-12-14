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
        if axis == 'y':
            unmoved_dots = [(x,y) for x,y in dots if y < val]
            dots_to_fold = [(x,y) for x,y in dots if y > val]
        else:
            unmoved_dots = [(x,y) for x,y in dots if x < val]
            dots_to_fold = [(x,y) for x,y in dots if x > val]

        folded_dots = [fold_dot(d[0], d[1], axis, val) for d in dots_to_fold]
        dots = folded_dots + unmoved_dots
        dots = list(set(dots)) # cull duplicates
    return dots

def fold_dot(x, y, axis, val):
    coord_to_fold = x if axis == 'x' else y
    coord_to_fold -= abs(coord_to_fold - val) * 2
    return (coord_to_fold, y) if axis == 'x' else (x, coord_to_fold)

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
