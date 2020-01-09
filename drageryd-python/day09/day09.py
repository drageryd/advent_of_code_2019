import sys
from itertools import permutations

def read_memory(memory, address):
    # If memory is too small
    while address >= len(memory):
        memory.append(0)
        #print('Extending memory', len(memory))
    #print('Reading', address)
    return memory[address]

def write_memory(memory, address, value):
    # If memory is too small
    while address >= len(memory):
        memory.append(0)
    memory[address] = value
    return value

def read_parameter(memory, ptr, mode, relative_base=0):
    a = read_memory(memory, ptr)
    if mode == '0':
        d = read_memory(memory, a)
    elif mode == '1':
        d = a
    elif mode == '2':
        d = read_memory(memory,relative_base + a)
        a += relative_base
    return(a,d)

def run(input, memory, output, ptr=0, relative_base=0):
    while True:
        # Extract opcode and parameters
        A,B,C,D,E = list(format(read_memory(memory, ptr), '05d'))
        opcode = D + E
        #print('instruction {}: {}{}{}{}{} ({})'.format(ptr,A,B,C,D,E,memory[ptr:ptr+4]))

        # Break
        if opcode == '99':
            break
        
        # 1st parameter
        a1, d1 = read_parameter(memory, ptr+1, C, relative_base)
        #print(' a1:{} d1:{} rb:{}'.format(a1,d1,relative_base))

        # Read
        if opcode == '03':
            # If no input return current position in memory
            if input:
                write_memory(memory, a1, input.pop(0))
                ptr += 2
                continue
            else:
                return (ptr,relative_base)
        # Write
        elif opcode == '04':
            output.append(d1)
            ptr += 2
            continue
        # Adjust relative base
        elif opcode == '09':
            relative_base += d1
            ptr += 2
            continue

        # 2nd parameter
        a2, d2 = read_parameter(memory, ptr+2, B, relative_base)
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
        a3, d3 = read_parameter(memory, ptr+3, A, relative_base)
        #print(' a3:{} d3:{}'.format(a3,d3))

        # Add
        if opcode == '01':
            write_memory(memory, a3, d1 + d2)
            ptr += 4
            continue
        # Multiply
        elif opcode == '02':
            write_memory(memory, a3, d1 * d2)
            ptr += 4
            continue
        # Less than
        elif opcode == '07':
            if d1 < d2:
                write_memory(memory, a3, 1)
            else:
                write_memory(memory, a3, 0)
            ptr += 4
            continue
        # Equals
        elif opcode == '08':
            if d1 == d2:
                write_memory(memory, a3, 1)
            else:
                write_memory(memory, a3, 0)
            ptr += 4
            continue
    return (-1,relative_base)

# Part 1
input = [1]
memory = [int(i) for i in sys.stdin.read().split(',')]
output = []
run(input,list(memory),output)
print('Part 1: {}'.format(output[0]))

# Part 2
input = [2]
output = []
run(input,list(memory),output)
print('Part 2: {}'.format(output[0]))

