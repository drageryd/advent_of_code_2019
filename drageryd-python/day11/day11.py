import sys
from intcode import run

input = [int(i) for i in sys.stdin.read().split(',')]

# Clockwise starting at 'up' (0)
directions = {0:(0,1), 1:(1,0), 2:(0,-1), 3:(-1,0)}

def paint_one(m, cp, p, d, ptr, rb):
    # Capture camera (not painted = black)
    if cp in p:
        c = p[cp]
    else:
        c = 0

    # Run one loop of the intcode computer
    o = []
    ptr, rb = run([c], m, o, ptr, rb)
    #print(o,ptr,rb)
    nc = o.pop(0)
    t = o.pop(0)
    return ptr, rb, nc, t

def pretty_print(p,cp=(0,0),cd=0):
    directions = {0:'^', 1:'>', 2:'v', 3:'<'}
    print('-----',cp,directions[cd],'------')
    xs,ys = tuple(zip(*p.keys())) if p else ([],[])
    xs += (cp[0],)
    ys += (cp[1],)
    for y in reversed(range(min(ys),max(ys)+1)):
        for x in range(min(xs),max(xs)+1):
            if (x,y) == cp:
                print(directions[cd], end='')
            elif (x,y) in p:
                if p[(x,y)] == 1:
                    print('#', end='')
                else:
                    print(' ', end='')
            else:
                print(' ', end='')
        print('')

# Paint until done
def paint_all(n, start=0, show=True):
    direction = 0
    position = (0,0)
    memory_pointer = 0
    relative_base = 0
    memory = list(input)

    # Painted tiles
    painted = {position:start}
    if show == 1:
        pretty_print(painted,position,direction)
    
    while True:
    #for i in range(n):
        # Run once
        memory_pointer, relative_base, new_color, turn = paint_one(memory, position, painted, direction, memory_pointer, relative_base)
        #print('step:',i,position,direction,new_color,turn,memory_pointer,relative_base)

        # Paint position
        painted[position] = new_color

        # If ptr = -1 program halted
        if memory_pointer == -1:
            print('Program terminated')
            break
    
        # Make turn
        if turn == 1:
            direction = (direction + 1) % 4
        else:
            direction = (direction - 1) % 4

        # Step in direction
        position = (position[0] + directions[direction][0], position[1] + directions[direction][1])

        # Pretty print
        if show == 1:
            pretty_print(painted,position,direction)
    if show == 2:
        pretty_print(painted,position,direction)
    return len(painted)


print('Part 1: {}'.format(paint_all(10,0,0)))
print('Part 1: {}'.format(paint_all(10,1,2)))

