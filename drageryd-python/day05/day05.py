import sys

def run(input, memory):
    output = []
    ptr = 0
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
            memory[a1] = input.pop(0)
            ptr += 2
            continue
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

    return output

'''
#Tests
tests = [([3,9,8,9,10,9,4,9,99,-1,8],[8],'==8 -> 1'),
         ([3,9,8,9,10,9,4,9,99,-1,8],[1],'==8 -> 0'),
         ([3,9,7,9,10,9,4,9,99,-1,8],[4],'<8 -> 1'),
         ([3,9,7,9,10,9,4,9,99,-1,8],[10],'<8 -> 0'),
         ([3,9,7,9,10,9,4,9,99,-1,8],[8],'<8 -> 0'),
         ([3,3,1108,-1,8,3,4,3,99],[8],'==8 -> 1'),
         ([3,3,1108,-1,8,3,4,3,99],[1],'==8 -> 0'),
         ([3,3,1107,-1,8,3,4,3,99],[4],'<8 -> 1'),
         ([3,3,1107,-1,8,3,4,3,99],[10],'<8 -> 0'),
         ([3,3,1107,-1,8,3,4,3,99],[8],'<8 -> 0'),
         ([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],[1],'==1 jump -> 1'),
         ([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],[0],'==1 jump -> 0'),
         ([3,3,1105,-1,9,1101,0,0,12,4,12,99,1],[1],'==1 jump -> 1'),
         ([3,3,1105,-1,9,1101,0,0,12,4,12,99,1],[0],'==1 jump -> 0'),
         ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],[7],'<8 -> 999'),
         ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],[8],'==8 -> 1000'),
         ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],[9],'>8 -> 10001')]

for m,i,s in tests:
    print('Test ({}): {}'.format(s,run(i, m)))
'''

memory = [int(i) for i in sys.stdin.read().split(',')]
print('Part 1: {}'.format(run([1], list(memory))[-1]))
print('Part 2: {}'.format(run([5], list(memory))[-1]))
