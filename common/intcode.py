
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
