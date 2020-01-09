import sys

input = sys.stdin.read().strip()
width = 25
height = 6
layer_size = width * height

layers = [input[chunk:chunk+layer_size] for chunk in range(0,len(input),layer_size)]

# Find layer with fewest 0 digits
fewest_0 = sorted(layers, key = lambda l: l.count('0'))[0]

print('Part 1: {}'.format(fewest_0.count('1') * fewest_0.count('2')))

# Create pixel priority
pixel_stack = list(zip(*layers))

# Remove transparent pixels (and only keep prio 1)
pixels = [list(filter(lambda p: p != '2', ps))[0] for ps in pixel_stack]

# Pretty print image
pixels = [pixels[i:i+width] for i in range(0,layer_size,width)]

print('Part 2:')
for row in pixels:
    print(''.join(row).replace('0',' ').replace('1','#'))

