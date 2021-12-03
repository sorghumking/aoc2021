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
    print(f"gamma = {g_str}, epsilon = {e_str}")
    print(f"Product is {int(g_str,2) * int(e_str,2)}")

def p2(numbers):
    oxy = get_rating(numbers, '1', '0', 'oxygen')
    co2 = get_rating(numbers, '0', '1', 'co2')
    print(f"Product of {oxy} and {co2} = {oxy*co2}")

def get_rating(_numbers, keep_bit, dump_bit, name):
    numbers = _numbers.copy()
    new_numbers = []
    for idx in range(len(numbers[0])):
        ones = len([n[idx] for n in numbers if n[idx] == '1'])
        zeroes = len(numbers) - ones
        if ones >= zeroes:
            new_numbers = [n for n in numbers if n[idx] == keep_bit]
        else: # zeroes > ones
            new_numbers = [n for n in numbers if n[idx] == dump_bit]
        numbers = new_numbers
        if len(numbers) == 1:
            decimal = int(''.join(numbers[0]), 2)
            print(f"{name} rating = {numbers[0]} = {decimal}")
            return decimal


if __name__ == "__main__":
    numbers = parse_input("inputs/d3.txt")
    p1(numbers)
    p2(numbers)