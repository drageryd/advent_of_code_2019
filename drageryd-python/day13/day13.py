import sys
from intcode import run
import time

game = [int(i) for i in sys.stdin.read().split(',')]
#game = [int(i) for i in open('day13.in','r').read().split(',')]

grid = {}
score = 0
def pretty_print(tiles):
    sprite = {4:'O', 3:'T', 2:'#', 1:'X', 0:' '}
    print('-----------------')
    global score
    global grid
    while tiles:
        x = tiles.pop(0)
        y = tiles.pop(0)
        t = tiles.pop(0)
        if (x,y) == (-1,0):
            score = t
        else:
            grid[(x,y)] = t

    xs = list([x for x,y in grid.keys()])
    ys = list([y for x,y in grid.keys()])
    print('score:', score)
    for y in range(min(ys),max(ys)+1):
        for x in range(min(xs),max(xs)+1):
            if (x,y) in grid:
                print(sprite[grid[(x,y)]], end='')
            else:
                print(' ', end='')
        print('')

# Part 1
m = list(game)
i = []
o = []
p,r = run(i,m,o)

# Every 3 is a tile
s = sum([1 for t in o[2::3] if t == 2])
print('Part 1: {}'.format(s))

# Part 2
m = list(game)
# Hack coin slot
m[0] = 2
i = []
o = []
p = 0
r = 0
test = 0
while p != -1:
    # Tick game
    p,r = run(i,m,o,p,r)
    pretty_print(o)
    # Move joystic
    #j = int(input('move:'))

    # AI
    # Get ball position
    ball = max(grid, key = lambda k: 1 if grid[k] == 4 else 0)
    paddle = max(grid, key = lambda k: 1 if grid[k] == 3 else 0)
    # If paddle is to the left of ball, move it right
    if paddle[0] < ball[0]:
        j = 1
    elif paddle[0] > ball[0]:
        j = -1
    else:
        j = 0
    # Add move to input
    i.append(j)

    time.sleep(0.01)

