# Return list of numbers and list of boards.
# Each board is a list of its 25 numbers in left-to-right, top-to-bottom order.
def parse_input(inputfile):
    numbers = []
    boards = []
    with open(inputfile) as f:
        cur_board = []
        rows_read = 0
        for idx, line in enumerate(f.readlines()):
            if idx == 0:
                numbers = [int(x) for x in line.split(',')]
                print(f"numbers = {numbers}")
            elif line.strip() != "":
                cur_board += [int(x) for x in line.split()]
                rows_read += 1
                if rows_read == 5:
                    boards.append(cur_board)
                    cur_board = []
                    rows_read = 0
    return numbers, boards

# Part 1: Find score of first board to bingo
def p1(numbers, boards):
    for num in numbers:
        for b in boards:
            mark_board(b, num)
            if bingo(b):
                unmarked_sum = sum([v for v in b if v > 0])
                print(f"Score is {unmarked_sum} * last number {num} = {unmarked_sum * num}")
                return

# Part 2: Find score of last board to bingo
def p2(numbers, boards):
    bingoed_board_indices = [] # track indices of boards that have bingoed
    for num in numbers:
        for idx, b in enumerate(boards):
            if idx in bingoed_board_indices: # skip bingoed boards
                continue
            mark_board(b, num)
            if bingo(b):
                unmarked_sum = sum([v for v in b if v > 0])
                bingoed_board_indices.append(idx)
                if len(bingoed_board_indices) == len(boards): # if this is the last bingoed board, we're done
                    print(f"Score of worst board is {unmarked_sum} * last number {num} = {unmarked_sum * num}")
                    return

# For each board, "mark" the value matching number by making it negative.
def mark_board(board, number):
    for idx, val in enumerate(board):
        if val == number:
            # print(f"Marking {val}")
            board[idx] *= -1
            break # assume only one match per board

# Does this board have bingo?
def bingo(board):
    return bingo_col(board) or bingo_row(board)

# Does any column in this board have bingo?
def bingo_col(board):
    for col in range(5):
        vals = board[col::5]
        if len([v for v in vals if v < 0]) == 5:
            # print(f"Column {col+1} bingo in {board}")
            return True
    return False

# Does any row in this board having bingo?
def bingo_row(board):
    for row in range(5):
        vals = board[5*row : 5*row+5]
        if len([v for v in vals if v < 0]) == 5:
            # print(f"Row {row} bingo in {board}")
            return True
    return False

if __name__ == "__main__":
    numbers, boards = parse_input("inputs/d4.txt")
    p1(numbers, boards)
    p2(numbers, boards)