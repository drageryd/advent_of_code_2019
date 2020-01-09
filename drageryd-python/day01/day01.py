import sys

input = [int(i) for i in sys.stdin.read().strip().split('\n')]
fuel = sum([int(mass/3) - 2 for mass in input])
print('Part 1: {}'.format(fuel))

fuel = 0
for mass in input:
    f = int(mass/3) - 2
    while f > 0:
        fuel += f
        f = int(f/3) - 2
print('Part 2: {}'.format(fuel))
