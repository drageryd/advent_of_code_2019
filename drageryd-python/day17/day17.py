from intcode import run
import sys
from functools import reduce

data = [int(n) for n in sys.stdin.read().strip().split(',')]

i = []
m = list(data)
o = []

# Test run once
p,r = run(i,m,o)

# Create a grid
os = ''.join([chr(i) for i in o]).strip()
"""
os = '''#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......'''
"""
grid = [list(line) for line in os.split('\n')]
grid = {(x,y):e for y,line in enumerate(grid) for x,e in enumerate(line) if e != '.'}

# Check if point in grid is a intersection, corner or dead end
def is_intersection(grid, point):
    if grid.get(point, '.') == '.':
        return False
    x, y = point
    # Adjacent points
    n = 1 if grid.get((x, y+1), '.') != '.' else 0
    s = 1 if grid.get((x, y-1), '.') != '.' else 0
    e = 1 if grid.get((x+1, y), '.') != '.' else 0
    w = 1 if grid.get((x-1, y), '.') != '.' else 0
    # Is dead end
    if sum((n, s, e, w)) == 1:
        return 1
    # Is intersection
    if sum((n, s, e, w)) == 4:
        return 4
    # Is corner or intersection
    for p in [(e, n), (e, s), (w, n), (w, s)]:
        if sum(p) == 2:
            return 2
    return 0

# Check every location in grid
s = 0
for point in grid:
    if is_intersection(grid, point) == 4:
        s += reduce(lambda x, y: x * y, point)
print('Part 1: {}'.format(s))

directions = ('^', '>', 'v', '<')
step_direction = ((0,-1), (1,0), (0,1), (-1,0))
visited = set()

def pretty_print(position, grid):
    size_x = max(x for x,y in grid) + 1
    size_y = max(y for x,y in grid) + 1
    for y in range(size_y):
        for x in range(size_x):
            if (x, y) == position[:2]:
                print(directions[position[2] % 4], end = '')
            elif (x, y) in grid:
                print('#', end = '')
            else:
                print('.', end = '')
        print('')


def step(position):
    x, y, d = position
    dx, dy = step_direction[d % 4]
    new_x = x + dx
    new_y = y + dy
    return (new_x, new_y)

# Try to move forward, else rotate to existing scaffolding
def find_next_step(position):
    x, y, d = position
    # Step forward
    if step(position) in grid:
        new_x, new_y = step(position)
        return ('F', (new_x, new_y, d))
    # Try to rotate right
    new_d = (d + 1) % 4
    if step((x, y, new_d)) in grid:
        return ('R', (x, y, new_d))
    # Try to rotate left
    new_d = (d - 1) % 4
    if step((x, y, new_d)) in grid:
        return ('L', (x, y, new_d))

# Go once through graph and visit every node
# Start is at one of the dead ends
position = ()
for point in grid:
    if grid[point] in directions:
        position = point + (directions.index(grid[point]),)
#pretty_print(position, grid)

steps = []
while len(visited) < len(grid):
    # Try to step forward
    action, position = find_next_step(position)
    # Add action to steps taken
    if action == 'F':
        if len(steps) > 0 and isinstance(steps[-1], int):
            steps[-1] += 1
        else:
            steps.append(1)
    else:
        steps.append(action)
    #print(steps)
    #pretty_print(position, grid)
    # Add position to visited points
    visited.add(position[:2])
    # Compare to grid to see if done
    #print(len(visited), len(grid))
#pretty_print(position, grid)
#print(steps)

# Check if list match
def matching_sublist(shorter, longer):
    length = min(len(shorter), len(longer))
    return shorter[:length] == longer[:length]

def function_to_ascii(f):
    # Convert to list of ascii
    return ','.join(str(i) for i in f)

def test_functions(A, B, C):
    options = [((), 0)]
    while options:
        main, index = options.pop(0)
        if matching_sublist(A, steps[index:]):
            new_main = main + ('A',)
            new_index = index + len(A)
            if new_index < len(steps):
                options.append((new_main, new_index))
            elif len(function_to_ascii(new_main)) < 20:
                break
        if matching_sublist(B, steps[index:]):
            new_main = main + ('B',)
            new_index = index + len(B)
            if new_index < len(steps):
                options.append((new_main, new_index))
            elif len(function_to_ascii(new_main)) < 20:
                break
        if matching_sublist(C, steps[index:]):
            new_main = main + ('C',)
            new_index = index + len(C)
            if new_index < len(steps):
                options.append((new_main, new_index))
            elif len(function_to_ascii(new_main)) < 20:
                break
    if new_index == len(steps) and len(function_to_ascii(new_main)) < 20:
        #print('     ', new_main, len(function_to_ascii(new_main)))
        return new_main
    else:
        #print('      ', new_main)
        return []

# Now steps contain the necessary steps to visit all parts of the scaffold
# Find repeating parts of the steps to turn into instructions
# Exhaustive test functions
a_len = 0
while True:
    a_len += 1
    A = steps[0:a_len]
    if len(function_to_ascii(A)) > 20:
        break
    b_start = a_len
    # Skip as long as A is repeating
    while matching_sublist(A, steps[b_start:]):
        b_start += len(A)
    b_len = 0
    while True:
        b_len += 1
        B = steps[b_start:b_start + b_len]
        if len(function_to_ascii(B)) > 20:
            break
        c_start = b_start + b_len
        # Skip as long as A or B is repeating
        while matching_sublist(A, steps[c_start:]) or matching_sublist(B, steps[c_start:]):
            if matching_sublist(A, steps[c_start:]):
                c_start += len(A)
            else:
                c_start += len(B)
        c_len = 0
        while True:
            c_len += 1
            C = steps[c_start:c_start + c_len]
            if len(function_to_ascii(C)) > 20:
                break
            """
            print("Testing functions {} ({}), {} ({}), {} ({})". format(
                function_to_ascii(A),
                len(function_to_ascii(A)),
                function_to_ascii(B),
                len(function_to_ascii(B)),
                function_to_ascii(C),
                len(function_to_ascii(C))))
            """
            main = test_functions(A, B, C)
            if main:
                break
        if main:
            break
    if main:
        break

# Wake robot
m = list(data)
m[0] = 2
i = []
o = []
p,r = run(i,m,o)

# Supply routines
routine = function_to_ascii(main) + '\n' + \
    function_to_ascii(A) + '\n' + \
    function_to_ascii(B) + '\n' + \
    function_to_ascii(C) + '\n' + \
    'n\n'
i = [ord(c) for c in routine]
o = []
p,r = run(i,m,o,p,r)
print('Part 2: {}'.format(o[-1]))
