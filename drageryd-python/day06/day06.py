import sys

input = sys.stdin.read().strip()

# Dictionary where key is an object that orbits the value
orbit_map = {object:orbit for orbit,object in [i.split(')') for i in input.split('\n')]}

# Calculate total number of direct and indirect orbits
n = 0
for object in orbit_map:
    o = object
    while o != 'COM':
        n += 1
        o = orbit_map[o]
print('Part 1: {}'.format(n))

# Assemble the closest path from COM to YOU and COM to SAN
com_you = ['YOU']
while com_you[0] != 'COM':
    com_you.insert(0,orbit_map[com_you[0]])
com_san = ['SAN']
while com_san[0] != 'COM':
    com_san.insert(0,orbit_map[com_san[0]])

# Remove the common indirect orbits
while com_san[0] == com_you[0]:
    com_san.pop(0)
    com_you.pop(0)

# Calculate the number of transfers required
print('Part 2: {}'.format(len(com_san)-1+len(com_you)-1))
