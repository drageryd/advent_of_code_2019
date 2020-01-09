import sys

# State based shuffling
def shuffle_state(length, instructions):
    i, l, z = (1, length, 0)
    for row in instructions.split("\n"):
        #print(i, d, l)
        if "deal into new stack" in row:
            # Same as deal with increment lenght - 1 followed by cut 1
            i = (i * (l - 1)) % l
            z = (z * (l - 1)) % l
            z = (z - 1) % l
            #print("deal into new stack")
            pass
        elif "cut" in row:
            cut = int(row.split(" ")[-1])
            z = (z - cut) % l
            #print("cut", cut)
        else:
            increment = int(row.split(" ")[-1])
            #print("deal with increment", increment)
            i = (i * increment) % l
            z = (z * increment) % l
    return (i, l, z)

# Repeat state multiple times
def combine_state(s1, s2):
    i1, l1, z1 = s1
    i2, l2, z2 = s2
    return ((i1 * i2) % l1, l1, (z1 * i2 + z2) % l1)

def repeat_state(state, repeat):
    rbin = list(bin(repeat)[2:])
    final_state = (1, state[1], 0)
    while rbin:
        bit = rbin.pop()
        if bit == "1":
            # Add bit state to final state
            final_state = combine_state(final_state, state)
        # Double the state
        state = combine_state(state, state)
    return final_state

def binary_exponentiation(a, n, m):
    # Binary representation without 0b
    nbits = list(bin(n)[2:])
    result = 1
    while nbits:
        bit = nbits.pop()
        if bit == "1":
            result = (result * a) % m 
        a = (a * a) % m
    return result

# Based on the deck state, find value at position
def deal(state, p):
    i, l, z = state
    i = i % l
    p = (p - z) % l
    # Since the deck length is prime in the real cases
    # we can safely use eulers theorem for modular multiplicative inverse
    # Calculating a^-1 = a^m-2 when m is prime, but becomes very large
    # Use Binary exponentiation to iterate the solution
    i_inv = binary_exponentiation(i, l - 2, l)
    return (p * i_inv) % l

data = sys.stdin.read().strip()

# Part 1
# Deck length
length = 10007
# Shuffle once
state = shuffle_state(length, data)
# Search for value 2019
for c in range(length):
    if deal(state, c) == 2019:
        print("Part 1: {}".format(c))

# Part 2
# New deck length
length = 119315717514047
# Shuffle once
state = shuffle_state(length, data)
# Number of times to repeat shuffle
repeat = 101741582076661
# Once again use a version of binary exponentiation to combine the states
state = repeat_state(state, repeat)
print("Part 2: {}".format(deal(state, 2020)))
