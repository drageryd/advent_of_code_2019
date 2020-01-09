import sys
import time

def multipliers(output_position, length):
    base = [0,1,0,-1]
    p = output_position
    while p < length:
        m = base[int((p + 1) / (output_position + 1)) % 4]
        if m != 0:
            yield (p,m)
        p += 1

def run(data, phases=100, multiplier=1, relative_offset=False):
    # Offset of which digits to return from last phase
    offset = int(data[:7]) if relative_offset else 0
    # Convert data
    data = [int(i) for i in data] * multiplier
    data_length = len(data)
    half_length = int(data_length / 2)
    # Calculate next phase
    for phase in range(phases):
        #print('phase', phase)
        #print(data)
        next_data = []
        # For data between offset and half length
        for i in range(offset,half_length):
            digit = 0
            for p,m in multipliers(i, data_length):
                #print(p,m)
                digit += data[p] * m
            data[i] = abs(digit) % 10
            #print('hard', i, data[i])
        # Last half of next phase is the sum of all digits to the right in current phase
        sum = 0
        for i in range(data_length-1, half_length-1, -1):
            sum = abs(sum + data[i]) % 10
            data[i] = sum
            #print('simple', i, data[i])
        #print('')   
    return ''.join([str(d) for d in data[offset:offset+8]])

tests = [(00,'12345678','01029498',4,1,False),
         (11,'80871224585914546619083218645595','24176176',100,1,False),
         (12,'19617804207202209144916044189917','73745418',100,1,False),
         (13,'69317163492948606335995924319873','52432133',100,1,False),
         (21,'03036732577212944063491565474664','84462026',100,10000,True),
         (22,'02935109699940807407585447034323','78725270',100,10000,True),
         (23,'03081770884921959731165446850517','53553731',100,10000,True)]

for t,i,o,p,m,r in tests:
    t1 = time.time()
    r = run(i,p,m,r)
    t2 = time.time()
    print('Test {0:2d} took {1:5.3f}s{2:>12s}... becomes {3:8s} ---> {4:>4s} ({5:8s})'.format(
        t,
        t2-t1,
        i[:10],
        o,
        'ok' if r == o else 'fail',
        r))

data = sys.stdin.read().strip()
print('Part 1: {}'.format(run(data,100,1,False)))
print('Part 2: {}'.format(run(data,100,10000,True)))
