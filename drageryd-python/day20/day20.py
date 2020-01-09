import sys

data = sys.stdin.read()

def is_label(x):
    return x not in "#. "

def create_grid(data):
    grid = {(x+y*1j):c for y,row in enumerate(data.split("\n")) for x,c in enumerate(row)}
    # Possible values to check for second part of label
    # Every tuple contains <direction to check>, <direction to pick from>, <front or back label>
    # e.g if a "." is found below (1j) a label, take the (-1j) letter and add it to the front (0)
    directions = ((1,-1,0), (-1,1,1), (1j,-1j,0), (-1j,1j,1))
    # Go through and parse labels
    for position, label in grid.items():
        # If part of a label
        if is_label(label):
            # Check directions
            for direction, pick, index in directions:
                # If the adjacent is traversable
                check = grid.get(position + direction, " ")
                choose = grid.get(position + pick, " ")
                if check == ".":
                    # Add the opposite value to the index in label
                    grid[position] = label[:index] + choose + label[index:]
                    grid[position + pick] = " "
    return grid

# Take a position, if it is a label, get where to teleport to
def get_label_teleported_position(grid, position):
    directions = (1,-1,1j,-1j)
    if is_label(grid[position]):
        for d in directions:
            if grid.get(position + d, " ") == ".":
                return position + d
    

def solve(data, recursive=False):
    # Generate grid
    grid = create_grid(data)

    # Get rows and columns for outer labels
    xs = set()
    ys = set()
    for p, v in grid.items():
        if is_label(v):
            xs.add(p.real)
            ys.add(p.imag)
    x_border = frozenset([min(xs), max(xs)])
    y_border = frozenset([min(ys), max(ys)])

    # Generate a list of portals with sets of positions
    portals = {}
    for p, v in grid.items():
        if is_label(v):
            s = portals.get(v, frozenset())
            portals[v] = s.union([p])


    # Remove and get start and end positions from portals
    start = get_label_teleported_position(grid, list(portals.pop("AA")).pop())
    end = get_label_teleported_position(grid, list(portals.pop("ZZ")).pop())

    # BFS the grid
    queue = [(start,0,0)]
    visited = set((start,0))
    count = 0
    while queue:
        position, distance, depth = queue.pop(0)
        # If at end return
        if position == end and depth == 0:
            return distance
        # Check adjacent
        directions = (1,-1,1j,-1j)
        for d in directions:
            new_position = position + d
            new_depth = depth
            floor = grid.get(new_position, " ")
            if floor in portals:
                # If recursive, increment or decrement depth
                if recursive:
                    # Check if border
                    if new_position.real in x_border or new_position.imag in y_border:
                        # Outer
                        if depth == 0:
                            continue
                        new_depth -= 1
                    else:
                        # Inner
                        new_depth += 1
                # Get corresponding portal
                new_position = list(portals[floor].difference([new_position])).pop()
                new_position = get_label_teleported_position(grid, new_position)
                floor = grid.get(new_position, " ")
            if (new_position, new_depth) in visited:
                continue
            # If traversable
            if floor == ".":
                queue.append((new_position, distance + 1, new_depth))
                visited.add((new_position, new_depth))

test1 = """         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z"""

test2 = """                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P        """

test3 = """             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                 """

print("Test {} is {}, should be {}".format(1, solve(test1), 23))
print("Test {} is {}, should be {}".format(2, solve(test2), 58))

print("Part 1: {}".format(solve(data)))

print("Test {} is {}, should be {}".format(1, solve(test1, True), 26))
print("Test {} is {}, should be {}".format(3, solve(test3, True), 396))

print("Part 2: {}".format(solve(data, True)))
