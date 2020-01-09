import sys

# Create a set of positions where there are bugs
def parse(data):
    state = set()
    rows = data.split("\n")
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c == "#":
                # Offset so that 0, 0 is in the middle
                state.add((x - int(len(row) / 2), y - int(len(rows) / 2), 0))
    return state

def get_adjacent(tile, recursive):
    x, y, z = tile
    steps = ((1, 0), (-1, 0), (0, 1), (0, -1))
    adjacent = []
    for dx, dy in steps:
        if recursive and (x + dx, y + dy) == (0, 0):
            # If the adjacent tile is in the middle, add one recusion level
            # Also the adjacent becomes the 5 tiles on the edge of that level
            # Add level
            dz = 1
            # Current tile is either (-1, 0), (1, 0), (0, -1) or (0, 1)
            # If the tile is (1, 0) the column on (2, y) should be added from deeper level
            if y == 0:
                # x_col is -2 or 2
                x_col = 2 * x
                adjacent += [(x_col, y_row, z + dz) for y_row in range(-2, 3)]
            else:
                # y_row is -2 or 2
                y_row = 2 * y
                adjacent += [(x_col, y_row, z + dz) for x_col in range(-2, 3)]
        elif abs(x + dx) <= 2 and abs(y + dy) <= 2:
            # Add if not outside grid
            adjacent.append((x + dx, y + dy, z))
        elif recursive:
            # If the adjacent tile is outside the edge, subtract one level
            # Also add the opposite tile on that level (e.g (0,-1,0)->(0,1,-1))
            # Subtract level
            dz = -1
            # dx and dy will point to the tile in the higher level
            # If the tile is (2, 0) [rightmost in middle row]
            # and the step is (1, 0) the tile will point to (1,0) in z-1
            adjacent.append((dx, dy, z + dz))
    return adjacent

# Calculate next state based on current
# If a space contains a bug it will die unless there is exactly 1 bug next to it
# If a space is empty it will spawn a bug if there is exactly 1 or 2 bugs next to it
def get_next(state, recursive):
    # Start with a new state
    next_state = set()
    # Since state only contains infested spaces and an empty space
    # only spawns if there are infested tiles next to it we can count
    # the infested adjacent tiles for an empty tile at the same time
    empty = {}
    # Loop through infested
    for tile in state:
        # Count infested adjacent tiles
        adjacent = 0
        # Get list of adjacent tiles
        for atile in get_adjacent(tile, recursive):
            if atile in state:
                # Tile infested
                adjacent += 1
            else:
                # Increment the infested count for this empty tile
                empty[atile] = empty.get(atile, 0) + 1
        # Check if tile should survive
        if adjacent == 1:
            next_state.add(tile)
    # Loop through empty tiles (that we know are adjacent to at least one infested tile)
    for tile, adjacent in empty.items():
        # Check if it should spawn
        if adjacent <= 2:
            next_state.add(tile)
    return next_state

def pretty(state):
    for z in range(-5, 6):
        print("Depth {}:".format(z))
        for y in range(-2, 3):
            for x in range(-2, 3):
                if (x, y) == (0, 0):
                    print("?", end="")
                elif (x, y, z) in state:
                    print("#", end="")
                else:
                    print(".", end="")
            print("")
        print("")

# Represent state as binary number where top left is lsb
def biodiversity_rating(state):
    bits = ''
    for y in range(-2, 3):
        for x in range(-2, 3):
            if (x, y, 0) in state:
                bits = '1' + bits
            else:
                bits = '0' + bits
    return int(bits, 2)


# Part 1
data = sys.stdin.read().strip()
state = parse(data)
rating = biodiversity_rating(state)
seen = set()
# Loop until first repeating
while rating not in seen:
    # Add to seen
    seen.add(rating)
    state = get_next(state, False)
    rating = biodiversity_rating(state)

print("Part 1: {}".format(rating))

state = parse(data)
for i in range(200):
    state = get_next(state, True)

print("Part 2: {}".format(len(state)))
