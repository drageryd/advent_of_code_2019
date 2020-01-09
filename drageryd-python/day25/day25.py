from intcode import run
import sys
from functools import reduce

data = [int(n) for n in sys.stdin.read().strip().split(',')]

"""
Output:
== Location ==
Description

Doors here lead:
- north
- south
- east
- west

Items here:
- <name of item>

Command?

Possible commands (end with newline):
Movement: north, south, east, or west
Take: take <name of item>
Drop: drop <name of item>
Inventory: inv
"""

def get_doors(output):
    doors = []
    movement = ("north", "south", "east", "west")
    for row in output.split("\n"):
        if "- " in row:
            row = row.replace("- ", "")
            if row in movement:
                doors.append(row)
    return doors

def get_items(output):
    items = []
    movement = ("north", "south", "east", "west")
    for row in output.split("\n"):
        # If a row starts with "- " it is an movement or item
        if "- " in row:
            row = row.replace("- ", "")
            if row not in movement:
                items.append(row)
    return items

def get_name(output):
    rows = []
    for row in output.split("\n"):
        if "==" in row:
            rows.append(row[3:-3])
    #print(rows)
    return rows[-1]

m = list(data)
p = 0
r = 0
def execute(command):
    global m
    global p
    global r
    if command:
        command += "\n"
    i = [ord(c) for c in command]
    o = []
    p,r = run(i,m,o,p,r)
    return ''.join(chr(c) for c in o)

# Items to not take
dont_take = set(["escape pod", "photons", "molten lava", "infinite loop", "giant electromagnet"])

# Breach hull
output = execute("")
# Current position
position = get_name(output)
# Rooms should contain {"name": {"room name": "direction"}}
rooms = {}

# Find and execute path between explored rooms
def goto_position(room_name, unexplored=None):
    global output
    global position
    local_output = output
    # BFS
    queue = [(position, )]
    visited = {position}
    while queue:
        path = queue.pop(0)
        if path[-1] == room_name:
            break
        candidates = [room for room in rooms[path[-1]].keys() if room not in visited]
        for room in candidates:
            queue.append(path + (room,))
            visited.add(room)
    #print(path)
    # Execute path
    for next_position in path[1:]:
        local_output = execute(rooms[position][next_position])
        position = get_name(local_output)
    if unexplored:
        #print(unexplored)
        unexplored_output = execute(unexplored)
        unexplored_position = get_name(unexplored_output)
        # Add if not existing
        rooms[path[-1]] = rooms.get(path[-1], {})
        if unexplored_position == position:
            rooms[path[-1]]["-Blocked-"] = unexplored
        else:
            local_output = unexplored_output
            position = unexplored_position
            # Add path to now explored room
            rooms[path[-1]][position] = unexplored
    return local_output

# DFS to unexplored
queue = [(position, None)]
while queue:
    #for i in range(10):
    #print("-------")
    # LIFO queue, pop from back
    goal_position, unexplored = queue.pop()
    #print("Goal position", goal_position, unexplored if unexplored else "")
    # Go to the goal position
    output = goto_position(goal_position, unexplored)
    #print(output)
    # Get room name, doors and items in this room
    name = get_name(output)
    #print("Is at", name)
    # Check if name already explored
    if name not in rooms:
        doors = get_doors(output)
        #print(doors)
        items = get_items(output)
        #print(items)
        # Pick up all items found
        for item in items:
            if item not in dont_take:
                #print("take", item)
                execute("take {}".format(item))
        # Populate connecting rooms with empty entries in rooms and add to queue
        for door in doors:
            queue.append((name, door))
    #print(rooms)

# Now all rooms are explored and the pressure sensing platform is found, all pickable items are in the inventory
# Go to the blocked passage
for room, doors in rooms.items():
    if "-Blocked-" in doors:
        target_room = room
        target_door = doors["-Blocked-"]
        break
#print(target_room, target_door)

# Go to room with blocked passage (Security Checkpoint)
output = goto_position(target_room, None)

# Generate list of inventory
output = execute("inv")
inventory = [row[2:] for row in output.split("\n") if "- " in row]

# Binary test all combinations of items until one works
# e.g 8 items = 256 combinations and 10001000 = take first and fifth item
for combination in range(2 ** len(inventory)):
    # All items are in inventory here
    mask = list(bin(combination)[2:].zfill(len(inventory)))
    #print([item for item, condition in zip(inventory, mask) if condition == "1"])
    # Drop all items not in current combination
    for item, condition in zip(inventory, mask):
        if condition == "0":
            execute("drop {}".format(item))

    # Try to enter blocked room
    output = execute(target_door)
    position = get_name(output)
    #print(output)
    if get_name(output) != target_room:
        # Succeded to enter room
        break

    # Pick items back up
    for item, condition in zip(inventory, mask):
        if condition == "0":
            execute("take {}".format(item))

print(output)
