def parse_input(inputfile):
    with open(inputfile) as f:
        for l in f.readlines():
            hex = l.strip()
            break
    return hex

def hex_to_bin(hexstr):
    binstr = ""
    for c in hexstr:
        binstr += bin(int(c,16))[2:].zfill(4) # add leading 0s until len == 4
    return binstr

version_sum = 0
stack = []
# blob (BlobReader): binary blob to parse
# level (int): indentation of log statements.
def parse(blob, level):
    global version_sum, stack

    vers = blob.version()
    version_sum += vers
    ti = blob.type_id()
    print(f"{'  '*level} version {vers} type {ti}", end='')
    if ti == 4:
        litval = blob.literal_value()
        print(f" literal value = {litval}")
        stack.append(litval)
    else:
        subpacket_count = 0
        lti = blob.len_type_id()
        if lti == 0:
            sl = blob.sub_length()
            print(f" LTI 0, reading {sl} bits")
            total_read = 0
            while total_read < sl:
                old_pos = blob.getpos()
                parse(blob, level+1)
                total_read += blob.getpos() - old_pos
                subpacket_count += 1
        elif lti == 1:
            sc = blob.sub_count()
            print(f" LTI 1, reading {sc} subpackets")
            for sub in range(sc):
                parse(blob, level+1)
            subpacket_count = sc
        process(ti, stack, subpacket_count, level)

# Pop last subpacket_count elements of stack, perform operation specified by ti
# on those elts, then push the result onto stack.
def process(ti, stack, subpacket_count, level):
    result = None
    if ti == 0: # sum
        vals = [stack.pop() for _ in range(subpacket_count)]
        result = sum(vals)
        print(f"{'  '*level} Got {result} from summing {vals}")
    elif ti == 1: # product
        result = 1
        vals = [stack.pop() for _ in range(subpacket_count)]
        for v in vals:
            result *= v
        print(f"{'  '*level} Got {result} from product of {vals}")
    elif ti == 2: # min
        vals = [stack.pop() for _ in range(subpacket_count)]
        result = min(vals)
        print(f"{'  '*level} {result} is min of {vals}")
    elif ti == 3: # max
        vals = [stack.pop() for _ in range(subpacket_count)]
        result = max(vals)
        print(f"{'  '*level} {result} is max of {vals}")
    elif ti in [5,6,7]: # >, <, ==
        assert subpacket_count == 2
        # Order matters for greater than and less than comparisons.
        # Top of stack is right side of comparison, second-to-top is left.
        cmp_r = stack.pop()
        cmp_l = stack.pop()
        if ti == 5: # >
            result = 1 if cmp_l > cmp_r else 0
            print(f"{'  '*level} {cmp_l} > {cmp_r}: {bool(result)}")
        elif ti == 6: # <
            result = 1 if cmp_l < cmp_r else 0
            print(f"{'  '*level} {cmp_l} < {cmp_r}: {bool(result)}")
        elif ti == 7: # ==
            result = 1 if cmp_l == cmp_r else 0
            print(f"{'  '*level} {cmp_l} == {cmp_r}: {bool(result)}")
    else:
        assert False, f"Unexpected packet type {ti}"
    stack.append(result)

# Convenience class to grab bits and track current position in binary blob
class BlobReader:
    def __init__(self, binary_blob):
        self.bb = binary_blob
        self.pos = 0
        self.last_read = '' # result of last getbits() call, useful for debugging

    def getpos(self): # get current position
        return self.pos

    def getbits(self, bitlen): # return bitlen bits, advance pos by bitlen
        bits = self.bb[self.pos:self.pos+bitlen]
        self.pos += bitlen
        self.last_read = bits
        return bits

    def version(self): # packet version
        return int(self.getbits(3), 2)

    def type_id(self): # packet type ID
        return int(self.getbits(3), 2)

    def len_type_id(self): # length type ID for operator packets
        return int(self.getbits(1), 2)

    def sub_length(self): # read 15 bits, length of subpackets
        return int(self.getbits(15), 2)

    def sub_count(self): # read 11 bits, subpacket count
        return int(self.getbits(11), 2)

    def literal_value(self):
        groups = []
        while True:
            next = self.getbits(5)
            groups.append(next)
            if next[0] != '1':
                break
        # print(f"Read {len(groups)} groups: {groups}")
        value = ""
        for g in groups:
            value += g[1:]
        return int(value, 2)
    

if __name__ == "__main__":
    hexstr = parse_input("inputs/d16.txt")
    for hex, expected in [(hexstr, "[Part 2 answer]")]:
    # for hex, expected in [("04005AC33890", 54), ("880086C3E88112", 7), ("CE00C43D881120", 9), ("D8005AC2A8F0", 1), ("F600BC2D8F", 0), ("9C005AC2F8F0", 0), ("9C0141080250320F1802104A08", 1)]:
        print(hex)
        parse(BlobReader(hex_to_bin(hex)), level=0)
        print(f"Part 1: Sum = {version_sum}")
        result = stack.pop(0)
        assert len(stack) == 0, "Stack nonempty after parsing."
        print(f"Part 2: Result = {result}, expected = {expected}\n")
        version_sum = 0 # reset for next loop cycle