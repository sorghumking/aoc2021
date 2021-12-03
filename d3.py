def parse_input(inputfile):
    numbers = []
    with open(inputfile) as f:
        for line in f.readlines():
            numbers.append(line.strip())
    return numbers

def p1(numbers):
    gamma = []
    epsilon = []
    for idx in range(len(numbers[0])):
        ones = len([n[idx] for n in numbers if n[idx] == '1'])
        zeroes = len(numbers) - ones
        gamma.append('1' if ones > zeroes else '0')
        epsilon.append('0' if ones > zeroes else '1')
    g_str = ''.join(gamma)
    e_str = ''.join(epsilon)
    print(f"Part 1:\ngamma = {g_str}, epsilon = {e_str}")
    print(f"Product is {int(g_str,2) * int(e_str,2)}\n")

def p2(numbers):
    print("Part 2:")
    oxy = get_rating(numbers, 'oxygen', '1', lambda x,y: x if len(x) > len(y) else y)
    co2 = get_rating(numbers, 'co2', '0', lambda x,y: x if len(x) < len(y) else y)
    print(f"Product of {oxy} and {co2} = {oxy*co2}")

def get_rating(_numbers, name, default, test):
    numbers = _numbers.copy()
    for idx in range(len(numbers[0])):
        zeroes = [n for n in numbers if n[idx] == '0']
        ones = [n for n in numbers if n[idx] == '1']
        if len(zeroes) == len(ones):
            numbers = zeroes if default == '0' else ones
        else:
            numbers = test(zeroes, ones)
        if len(numbers) == 1:
            decimal = int(''.join(numbers[0]), 2)
            print(f"{name} rating = {numbers[0]} = {decimal}")
            return decimal


if __name__ == "__main__":
    numbers = parse_input("inputs/d3.txt")
    p1(numbers)
    p2(numbers)