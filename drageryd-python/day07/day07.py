import sys
from itertools import permutations

def run(input, memory, ptr, output):
    while True:
        # Extract opcode and parameters
        A,B,C,D,E = list(format(memory[ptr], '05d'))
        opcode = D + E
        #print('instruction {}: {}{}{}{}{} ({})'.format(ptr,A,B,C,D,E,memory[ptr:ptr+4]))

        # Break
        if opcode == '99':
            break
        
        # 1st parameter
        a1 = memory[ptr + 1]
        if C == '0':
            d1 = memory[a1]
        else:
            d1 = a1
        #print(' a1:{} d1:{}'.format(a1,d1))

        # Read
        if opcode == '03':
            # If no input return current position in memory
            if input:
                memory[a1] = input.pop(0)
                ptr += 2
                continue
            else:
                return ptr
        # Write
        elif opcode == '04':
            output.append(d1)
            ptr += 2
            continue

        # 2nd parameter
        a2 = memory[ptr + 2]
        if B == '0':
            d2 = memory[a2]
        else:
            d2 = a2
        #print(' a2:{} d2:{}'.format(a2,d2))

        # Jump if true
        if opcode == '05':
            if d1 != 0:
                ptr = d2
            else:
                ptr += 3
            continue
        # Jump if false
        elif opcode == '06':
            if d1 == 0:
                ptr = d2
            else:
                ptr += 3
            continue

        # 3rd parameter
        a3 = memory[ptr + 3]
        if A == '0':
            d3 = memory[a3]
        else:
            d3 = a3
        #print(' a3:{} d3:{}'.format(a3,d3))

        # Add
        if opcode == '01':
            memory[a3] = d1 + d2
            ptr += 4
            continue
        # Multiply
        elif opcode == '02':
            memory[a3] = d1 * d2
            ptr += 4
            continue
        # Less than
        elif opcode == '07':
            if d1 < d2:
                memory[a3] = 1
            else:
                memory[a3] = 0
            ptr += 4
            continue
        # Equals
        elif opcode == '08':
            if d1 == d2:
                memory[a3] = 1
            else:
                memory[a3] = 0
            ptr += 4
            continue
    return -1

# Set up the instances of incomputers
def run_sequence(setting, memory):
    s1, s2, s3, s4, s5 = setting
    o1, o2, o3, o4, o5 = [s1], [s2], [s3], [s4], [s5,0]
    p1, p2, p3, p4, p5 = 0, 0, 0, 0, 0
    m1, m2, m3, m4, m5 = list(memory), list(memory), list(memory), list(memory), list(memory)
    while True:
        # Stage 1
        #print('Run stage 1')
        p1 = run(o5, m1, p1, o1)
        #print('Returned', p1)
        # Stage 2
        #print('Run stage 2')
        p2 = run(o1, m2, p2, o2)
        #print('Returned', p2)
        # Stage 3
        #print('Run stage 3')
        p3 = run(o2, m3, p3, o3)
        #print('Returned', p3)
        # Stage 4
        #print('Run stage 4')
        p4 = run(o3, m4, p4, o4)
        #print('Returned', p4)
        # Stage 5
        #print('Run stage 5')
        p5 = run(o4, m5, p5, o5)
        #print('Returned', p5)
        if p5 == -1:
            break
    #print('Sequence result', o5)
    return o5[0]

memory = [int(i) for i in sys.stdin.read().split(',')]

# Part 1
best = 0
for p in permutations(range(5)):
    o = run_sequence(p, memory)
    best = max(best, o)
print('Part 1: {}'.format(best))

# Part 2
best = 0
for p in permutations(range(5,10)):
    o = run_sequence(p, memory)
    best = max(best, o)
print('Part 2: {}'.format(best))










