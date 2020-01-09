from intcode import run
import sys

data = [int(n) for n in sys.stdin.read().strip().split(',')]

def execute(code):
    program = [[ord(c) for c in line + "\n"] for line in code.split("\n")]
    i = []
    m = list(data)
    o = []
    # Test run once
    p,r = run(i,m,o)
    for i in program:
        p,r = run(i,m,o,p,r)
    #print(''.join(chr(x) for x in o if x < 256))
    return o[-1]

# If any of tiles A, B and C are a hole and D is floor -> jump
part1 = """NOT J J
AND A J
AND B J
AND C J
NOT J J
AND D J
WALK"""

print("Part 1:", execute(part1))

# Extend part 1 to only jump eary if H is clear, this forces us to sometimes always jump at A
part2 = """NOT J J
AND A J
AND B J
AND C J
NOT J J
AND D J
AND H J
NOT A T
OR T J
RUN"""

print("Part 2:", execute(part2))
