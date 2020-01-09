import sys

input = [int(i) for i in sys.stdin.read().split(',')]

def run(memory, p1, p2):
    m = list(memory)
    i = 0
    m[1] = p1
    m[2] = p2
    while True:
        opcode = m[i]
        if opcode == 1:
            m[input[i + 3]] = m[input[i + 1]] + m[input[i + 2]]
        elif opcode == 2:
            m[input[i + 3]] = m[input[i + 1]] * m[input[i + 2]]
        else:
            break
        i += 4
    return m[0]

print('Part 1: {}'.format(run(input, 12, 2)))

goal = 19690720

max = 1000

for noun in range(max):
    for verb in range(max):
        output = run(input, noun, verb)
        if output == goal:
            break
    if output == goal:
        break

print('Part 2: {}'.format(100 * noun + verb))
