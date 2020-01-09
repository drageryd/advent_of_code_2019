import sys
from itertools import combinations_with_replacement

lower, upper = [int(i) for i in sys.stdin.read().split('-')]
input = range(lower, upper+1)

# Generate 6 digit candidates with increasing digits
candidates = combinations_with_replacement('0123456789', 6)

# Filter based on input range
candidates = [''.join(c) for c in candidates if int(''.join(c)) in input]

# Return if candidate has repeated digits
def has_repeating(candidate, allow_group = True):
    digits = '0123456789'
    counts = [candidate.count(d) for d in digits]
    if allow_group:
        return [c for c in counts if c > 1]
    else:
        return [c for c in counts if c == 2]
    
# Filter based on repeating digits
print('Part 1: {}'.format(len([c for c in candidates if has_repeating(c)])))
print('Part 2: {}'.format(len([c for c in candidates if has_repeating(c, False)])))
