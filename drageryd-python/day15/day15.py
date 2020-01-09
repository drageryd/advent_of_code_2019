import sys
from intcode import run

data = [int(i) for i in sys.stdin.read().split(',')]

def pretty_print(map, path=None):
    if  path:
        map = dict(map)
        x,y = 0,0
        map[(x,y)] = 'X'
        for s in path:
            if s == 1:
                y += 1
            elif s == 2:
                y -= 1
            elif s == 3:
                x -= 1
            elif s == 4:
                x += 1
            map[(x,y)] = 'X'
    
    xs = list(zip(*map.keys()))[0]
    ys = list(zip(*map.keys()))[1]
    for y in reversed(range(min(ys),max(ys)+1)):
        for x in range(min(xs),max(xs)+1):
            if (x,y) in map:
                print(map[(x,y)],end='')
            else:
                print(' ',end='')
        print('')

# Starting position is ok
map = {(0,0):'D'}

# queue containing memory and variables for every path, position and steps there
queue = [(list(data),0,0,0,0,[])]
loops = 0
part1_len = 0
while queue:
    # Get queue item
    memory, pointer, relbase, position_x, position_y, path = queue.pop(0)

    # Check done
    if map.get((position_x,position_y),0) == 'T':
        part1_len = len(path)
    
    # Generate steps
    steps = [1,2,3,4]
    # For every step
    for s in steps:
        # Generate a queue candidate
        m = list(memory)
        p = pointer
        r = relbase
        
        # Possible new position
        x = position_x
        y = position_y
        if s == 1:
            y += 1
        elif s == 2:
            y -= 1
        elif s == 3:
            x -= 1
        elif s == 4:
            x += 1

        # Path there
        np = path + [s]
            
        # Run bot once
        i = [s]
        o = []
        p,r = run(i,m,o)

        # Evaluate output
        o = o.pop()
        if o == 0:
            # Hit wall
            # Dont add to queue
            # Add wall to map
            map[(x,y)] = '#'
        elif o == 1:
            # Moved
            # Add to queue if tile isnt already visited
            if (x,y) not in map:
                # Add to queue
                queue.append((m,p,r,x,y,np))
                # Add ok to map
                map[(x,y)] = '.'
        elif o == 2:
            # Add to queue
            queue.append((m,p,r,x,y,np))
            # Add oxygen to map
            map[(x,y)] = 'T'

    loops += 1
    #if loops > 1000:
    #    break

pretty_print(map, path)
print('Part 1: {}'.format(part1_len))

# Part 2
startx,starty = max(map, key=lambda k: 1 if map[k] == 'T' else 0)

# Search back to all positions
queue = [(startx,starty,0)]

while queue:
    x,y,t = queue.pop(0)
    # fill with oxygen
    map[(x,y)] = 'O'
    # steps
    for sx,sy in [(1,0),(-1,0),(0,1),(0,-1)]:
        if map[(x+sx,y+sy)] == '#':
            # if step is a wall dont queue
            pass
        elif map[(x+sx,y+sy)] == 'O':
            # if already filled with oxygen dont queue
            pass
        else:
            # else queue
            queue.append((x+sx,y+sy,t+1))
        
pretty_print(map)
print('Part 2: {}'.format(t))
