import sys
import math

input = sys.stdin.read().strip()
"""
input = '''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##'''
"""
def get_visible_asteroids(coordinates, chosen=None):
    #print(coordinates)

    # For every asteroid check relative distance to all others sorted by total distance (3rd element)
    # If we've already chosen one, only get its visible
    if chosen is None:
        distances = {c:sorted([(x-c[0],c[1]-y) for x,y in coordinates if (x,y) != c], key=lambda k: abs(k[0])+abs(k[1])) for c in coordinates}
    else:
        c = chosen
        distances = {c:sorted([(x-c[0],c[1]-y) for x,y in coordinates if (x,y) != c], key=lambda k: abs(k[0])+abs(k[1]))}
    max_distance = sum(max(coordinates, key=lambda k:sum(k)))
    #print(distances)
    #print(max_distance)

    # For every neighbor, remove k*(relative coordinate) neighbors (blocked by current neighbor)
    filtered = {}
    for asteroid,neighbors in distances.items():
        #print('Asteroid',asteroid)
        filtered[asteroid] = []
        while neighbors:
            # Add closest neighbor to filtered
            x,y = neighbors.pop(0)
            #print(' testing',x,y)
            filtered[asteroid].append((x,y))
            #print(filtered[asteroid])
            # Remove blocked
            #k = y/x or x/y
            for d in range(1,max_distance):
                if abs(x) <= abs(y):
                    x2 = d*x/abs(y)
                    y2 = d*y/abs(y)
                else:
                    x2 = d*x/abs(x)
                    y2 = d*y/abs(x)
                if (x2,y2,) in neighbors:
                    #print('  found',x2,y2)
                    neighbors.remove((x2,y2))
    #lengths = {k:len(v) for k,v in filtered.items()}
    return filtered

# Part 1
# Create list of coordinates
coordinates = [(x,y) for y,row in enumerate(input.split('\n')) for x,c in enumerate(row) if c == '#']
# Get best asteroid
lengths = get_visible_asteroids(coordinates)
best_coordinate,best_visible = max(lengths.items(), key=lambda i: len(i[1]))
print('Part 1: {}'.format(len(best_visible)))


def angle(x,y):
    a = math.atan2(x,y)
    if a < 0:
        a = 2*math.pi + a
    return a

def get_vaporized_order(coordinates, chosen, n):
    # Local copy
    vapor_order = []
    while len(vapor_order) < n and coordinates:
        # Get visible from chosen
        lengths = get_visible_asteroids(coordinates,chosen)
         # Only one element sorted based on angle
        visible = sorted(lengths[chosen],key=lambda k: angle(k[0],k[1]))
        # Project back to global coordinates
        new_vapor_order = [(chosen[0]+x,chosen[1]-y) for x,y in visible]
        #new_vapor_order = [(x,y,angle(x,y)) for x,y in sorted(visible, key=lambda c: angle(c[0],c[1]))]
        #print(new_vapor_order)
        # Add new to vapor_order
        vapor_order += new_vapor_order
        # Remove from coordinates
        coordinates = [c for c in coordinates if c not in new_vapor_order]
    return vapor_order[:n]




# Part 2
#lengths = get_visible_asteroids(coordinates,(8,3))
#best_coordinate,best_visible = max(lengths.items(), key=lambda i: len(i[1]))
#print(len(best_visible))
# Sort visible based on angle (back to global coordinates)
#best_visible = [(x+best_coordinate[0],y+best_coordinate[1]) for x,y in sorted(best_visible, key=lambda c: angle(c[0],c[1]), reverse=True)]
#print(best_visible)

"""
input = '''.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##'''
coordinates = [(x,y) for y,row in enumerate(input.split('\n')) for x,c in enumerate(row) if c == '#']
best_coordinate = (8,3)
print(get_visible_asteroids(coordinates,(8,3)))
print('')
"""

#coordinates = [(x,y) for y,row in enumerate(input.split('\n')) for x,c in enumerate(row) if c == '#']
#best_coordinate = (8,3)
#best_projected = [(8+x,3-y) for x,y in sorted(get_visible_asteroids(coordinates,(8,3))[(8,3)],key=lambda k:angle(k[0],k[1]))]
#print(best_projected)

#print(best_coordinate)
vapor_order = get_vaporized_order(coordinates, best_coordinate, 200)
#print('chosen',best_coordinate)
#print(vapor_order)
#for i in [0,1,2,9,19,49,99,198,199,200,298]:
#    print(vapor_order[i])

x,y = vapor_order[-1]
print('Part 2: {}'.format(100*x+y))
