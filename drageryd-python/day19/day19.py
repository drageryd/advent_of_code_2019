from intcode import run
import sys

data = [int(n) for n in sys.stdin.read().strip().split(',')]

scan_area = {}

def scan(x, y):
    if x < 0 or y < 0:
        return 0
    i = [x,y]
    m = list(data)
    o = []
    # Test run once
    p,r = run(i,m,o)
    return o[0]

# Part 1
for y in range(50):
    for x in range(50):
        scan_area[(x,y)] = scan(x,y)

print("Part 1: {}".format(sum(v for p,v in scan_area.items())))

# Part 2
# Start at the end of the already scanned area and find the first x value 1
y = 49
for x in range(50):
    if scan_area[(x,y)]:
        break
# x and y now contain the star of the search
# If a square of size 100 fits in the beam (x,y) and (x+99, y-99) should contain 1s
# And the desired coordinate is located at (x, y-99)
size = 100
while (scan(x,y), scan(x+(size-1),y-(size-1))) != (1,1):
    # Increment y
    y += 1
    # Increment x until beam is found
    while scan(x,y) != 1:
        x += 1

print("Part 2: {}".format(10000 * x + (y - (size-1))))
