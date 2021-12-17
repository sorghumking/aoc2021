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

vers_sum = 0
def parse(blob, level):
    vers = blob.version()
    global vers_sum
    vers_sum += vers
    ti = blob.type_id()
    print(f"{'  '*level} version {vers} type {ti}", end='')
    if ti == 4:
        litval = blob.literal_value()
        print(f" literal value = {litval}")
    else:
        lti = blob.len_type_id()
        if lti == 0:
            sl = blob.sub_length()
            print(f" LTI 0, reading {sl} bits")
            total_read = 0
            while total_read < sl:
                old_pos = blob.getpos()
                parse(blob, level+1)
                total_read += blob.getpos() - old_pos
        elif lti == 1:
            sc = blob.sub_count()
            print(f" LTI 1, reading {sc} subpackets")
            for sub in range(sc):
                parse(blob, level+1)

class Blob:
    def __init__(self, binary_blob):
        self.bb = binary_blob
        self.bloblen = len(binary_blob)
        self.pos = 0
        self.read_count = 0 # bits read since last reset
        self.last_read = ''

    def _incrpos(self, amt):
        self.pos += amt
        self.read_count += amt

    def reset(self):
        self.read_count = 0
    
    def getpos(self):
        return self.pos

    def setpos(self, pos):
        self.pos = pos

    def getbits(self, bitlen):
        bits = self.bb[self.pos:self.pos+bitlen]
        self._incrpos(bitlen)
        self.last_read = bits
        return bits

    def peekbits(self, bitlen):
        return self.bb[self.pos:self.pos+bitlen]

    def version(self):
        return int(self.getbits(3), 2)

    def type_id(self):
        return int(self.getbits(3), 2)

    def len_type_id(self): # length type ID for operator packets
        return int(self.getbits(1), 2)

    def sub_length(self): # read 15 bits, length of subpackets
        return int(self.getbits(15), 2)

    def sub_count(self): # read 11 bits, subpacket count
        return int(self.getbits(11), 2)

    def get_subs_by_length(self, length):
        return self.getbits(length)

    def get_subs_by_count(self, count):
        sublen = 11
        subs = [self.getbits(sublen) for c in range(count)]
        return subs        

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
    # hex = parse_input("inputs/d16.txt")
    for hex in ["C200B40A82"]:
        parse(Blob(hex_to_bin(hex)), 0)
        print(f"Sum = {vers_sum}")
        vers_sum = 0