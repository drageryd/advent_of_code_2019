import sys
from bisect import insort

data = sys.stdin.read().strip()

def is_door(item):
    return item.isupper()

def is_key(item):
    return item.islower()

def is_item(item):
    return is_door(item) or is_key(item)

def is_wall(item):
    return item == "#"

def is_entrance(item):
    return item == "@"

def entrance():
    return "@"

def wall():
    return "#"

def space():
    return "."

# Find all items from a start position returns a dictionary with distances and doors passed on the way
def distances_to_items(grid, start):
    # Stored distances from start to item
    distances = {}
    # Start at start position
    queue = [(start, 0, frozenset())]
    # Save visited position to not revisit
    visited = set([start])
    # Possible steps from a position
    steps = (1, 1j, -1, -1j)
    while queue:
        position, distance, items = queue.pop(0)
        # If position contains an item, store it
        item = grid[position]
        if is_key(item) and position != start:
            distances[position] = (item, distance, items)
        if is_item(item) and position != start:
            items = items.union(item)
        # Get possible steps from current position
        next_positions = [position + step for step in steps if not is_wall(grid[position + step]) and position + step not in visited]
        # Add to queue with one more step
        queue += [(np, distance + 1, items) for np in next_positions]
        # Add to visisted
        visited.update(next_positions)
    return distances

# Takes a list of items and returns the keys needed
def get_needed_keys(doors):
    return frozenset(i.lower() for i in doors if is_door(i))

def get_unlocked_doors(keys):
    return frozenset(i.upper() for i in keys if is_key(i))

def get_dependency_table(table):
    dependency_table = {}
    keys = {i: d for i, d in table.items() if is_key(i)}
    for key in keys:
        distance, passing = keys[key]
        dependency_table[key] = get_needed_keys(passing)
    return dependency_table

def convert_to_multiple(grid):
    # Get entrance position
    ep = [p for p, i in grid.items() if is_entrance(i)].pop()
    # If surrounding grids are empty
    surrounding = (-1-1j, -1j, 1-1j, -1, 1, -1+1j, 1j, 1+1j)
    if [grid[ep+p] for p in surrounding].count(space()) == len(surrounding):
        grid[ep] = wall()
        for p in surrounding:
            if abs(p) == 1:
                grid[ep+p] = wall()
            else:
                grid[ep+p] = entrance()

# Lets bfs/A* (again) our way through the options, starting from the start
def solve(data, multiple=False):
    # Create a grid to be able to parse testing imaginary number for coordinate
    grid = {x + y * 1j: v for y,row in enumerate(data.split("\n")) for x,v in enumerate(row)}

    # Convert entrance to multi entrance if input argument is set and grid supports it
    if multiple:
        convert_to_multiple(grid)

    # Construct a table of the shortest distance from all keys to all other keys
    table = {position: distances_to_items(grid, position) for position, item in grid.items() if is_key(item) or is_entrance(item)}
    keys_set = frozenset(grid[p] for p in table if is_key(grid[p]))

    # Start at entrances with 0 steps
    queue = [(0, frozenset(p for p in table if is_entrance(grid[p])), frozenset())]
    visited = {}
    largest_queue = 0
    depth = 0

    while queue:
        total_distance, current_positions, passed_keys = queue.pop(0)
        # If all keys are found, print solution and distance
        if not keys_set.difference(passed_keys):
            return total_distance

        for position in current_positions:
            old_positions = current_positions.difference([position])
            # Loop over possible keys from current item
            for new_position, value in table[position].items():
                # Get distance and blocking items
                key, distance, blocking = value
                # If key already visited
                if key in passed_keys:
                    continue
                # Remove visited keys from blocking
                blocking = blocking.difference(passed_keys)
                # Remove unlocked doors from blocking
                blocking = blocking.difference(get_unlocked_doors(passed_keys))
                # If no blocking, add to queue
                if not blocking:
                    new_passed_keys = passed_keys.union(key)
                    new_distance = total_distance + distance
                    new_positions = old_positions.union([new_position])
                    # Insert only if it is shorder than element already in visited
                    if (new_positions, new_passed_keys) in visited and visited[(new_positions, new_passed_keys)] <= new_distance:
                        pass
                    else:
                        # Add to visited and queue
                        insort(queue, (new_distance, new_positions, new_passed_keys))
                        visited[(new_positions, new_passed_keys)] = new_distance

test1 = """#########
#b.A.@.a#
#########"""

test2 = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

test3 = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""

test4 = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""

test5 = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""

test6 = """#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######"""

test7 = """###############
#d.ABC.#.....a#
######...######
######.@.######
######...######
#b.....#.....c#
###############"""

test8 = """#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############"""

test9 = """#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############"""

print("Test 1:", solve(test1), "should be", 8)
print("Test 2:", solve(test2), "should be", 86)
print("Test 3:", solve(test3), "should be", 132)
print("Test 4:", solve(test4), "should be", 136)
print("Test 5:", solve(test5), "should be", 81)

# Solve part 1
print("Part 1: {}".format(solve(data)))

print("Test 6:", solve(test6, True), "should be", 8)
print("Test 7:", solve(test7, True), "should be", 24)
print("Test 8:", solve(test8, True), "should be", 32)
print("Test 9:", solve(test9, True), "should be", 72)

# Solve part 2
print("Part 2: {}".format(solve(data, True)))
