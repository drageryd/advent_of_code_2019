import sys

input = sys.stdin.read().strip()
input = [row.split(',') for row in input.split('\n')]

# List coordinates from point in direction (Unn, Dnn, Rnn, Lnn)
def list_coordinates(start, steps, coordinates):
    d = steps[0]
    cx = {'R':1, 'L':-1, 'U':0, 'D':0}
    cy = {'R':0, 'L':0, 'U':1, 'D':-1}
    s = int(steps[1:])
    x,y = start
    for i in range(1,s+1):
        # Add coordinate and number of steps there
        if (cx[d]*i+x, cy[d]*i+y) not in coordinates:
            coordinates[(cx[d]*i+x, cy[d]*i+y)] = coordinates.get(start,0) + i
    return (cx[d]*s+x, cy[d]*s+y)

# Add all coordinates that a wire occupies to a set
coordinates = []
for wire in input:
    # Dictionary with coordinates and number of steps so far
    c = {}
    p = (0,0)
    for w in wire:
        p = list_coordinates(p, w, c)
    coordinates.append(c)

# Convert coordinate dictionarys to sets and intersect sets
intersections = set.intersection(*[set(coordinates.keys()) for coordinates in coordinates])
print('Part 1: {}'.format(min(sum(abs(i) for i in intersection) for intersection in intersections)))

# Get sum of steps to intersections
distances = [sum(c.get(i,0) for c in coordinates) for i in intersections]
print('Part 2: {}'.format(min(distances)))
