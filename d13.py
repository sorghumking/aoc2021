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
    wid = 0
    hit = 0
    dots = _dots.copy()
    for axis, val in folds:
        new_dots = []
        if axis == 'y':
            unmoved_dots = [dot for dot in dots if dot[1] < val]
            for d in [dot for dot in dots if dot[1] > val]:
                diff = abs(d[1] - val) * 2
                folded_dot = (d[0], d[1] - diff)
                new_dots.append(folded_dot)
            hit = val
        else: # y-axis
            unmoved_dots = [dot for dot in dots if dot[0] < val]
            for d in [dot for dot in dots if dot[0] > val]:
                diff = abs(d[0] - val) * 2
                folded_dot = (d[0] - diff, d[1])
                new_dots.append(folded_dot)
            wid = val
        dots = new_dots + unmoved_dots
        dots = list(set(dots)) # cull dups
    return dots, wid, hit

def print_paper(dots, wid, hit):
    for y in range(0, hit):
        for x in range(0, wid):
            print('#', end='') if (x,y) in dots else print(' ', end='')
        print('\n')

if __name__ == "__main__":
    dots, folds = parse_input("inputs/d13.txt")
    folded_dots, wid, hit = do_folds(dots, folds)
    print_paper(folded_dots, wid, hit)
