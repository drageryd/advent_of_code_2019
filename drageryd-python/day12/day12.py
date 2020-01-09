import sys
import re
import numpy as np

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def guess_seq_len(seq):
    #guess = -1
    #max_len = int(len(seq)/2)
    #for x in range(2, max_len):
    #    if seq[-x:] == seq[-2*x:-x] :
    #        return x
    #return guess
    last = seq[-1]
    length = len(seq)
    candidate = []
    # Find all indexes of last (from half length)
    values = np.array(seq[int(length/2):-3])
    ii = np.where(values == last)[0] + int(length/2)
    #print(last, ii)
    #print(seq)
    # Test if sequence from last to match repeats
    #print(list(reversed(ii)))
    for i in reversed(ii):
        # sequence length
        sl = length - i - 1
        # Check if match
        #print(seq[-sl:],seq[-2*sl:-sl])
        if seq[-sl:] == seq[-2*sl:-sl]:
            return sl
    return -1
        

def simulate(input, n):
    moons = [[int(n) for n in re.findall('-?\d+',row)] for row in input.split('\n')]
    moons = list(zip(moons, [[0,0,0] for m in moons]))

    # Period fitting per position/velocity axis
    #states = [{'done':False, 'period':0} for mvp in moons for axis in mvp]
    states = [[0] for mvp in moons for pair in mvp for e in pair]
    candidate = []
    
    t = 0
    while n == 0 or t < n:
        # Apply gravity
        for moon, velocity in moons:
            # Compare to all other moons
            for m, v in moons:
                for axis, mm_pair in enumerate(zip(moon, m)):
                    m1, m2 = mm_pair
                    if m1 < m2:
                        velocity[axis] += 1
                    elif m1 > m2:
                        velocity[axis] -= 1

        # Update positions
        for moon, velocity in moons:
            for axis, mv_pair in enumerate(zip(moon, velocity)):
                moon[axis] = sum(mv_pair)

        # Calculate energy
        energy = sum([sum(abs(a) for a in moon) * sum(abs(b) for b in velocity) for moon, velocity in moons])

        '''
        # Check states to find periods
        if n == 0:
            state = [tuple(axis) for mvp in moons for axis in mvp]
            for s,ss in zip(state,states):
                # If this axis is done
                if ss['done']:
                    continue
                # Check if this axis state has been before
                if s in ss:
                    ss['period'] = t - ss[s]
                    ss['done'] = True
                else:
                    ss[s] = t
            # Check if all axis periods are found
            if [ss['done'] for ss in states].count(False) == 0:
                periods = [ss['period'] for ss in states]
                print(periods)
                pfs = [prime_factors(p) for p in periods]
                pftot = set()
                for pfl in pfs:
                    for pf in set(pfl):
                        for c in range(pfl.count(pf)):
                            pftot.add((pf,c))
                print(pftot)
                product = 1
                for pf,c in pftot:
                    product *= pf
                return product
        '''
        if n == 0:
            state = [e for mvp in moons for pair in mvp for e in pair]
            # Add current state to states
            for s,ss in zip(state, states):
                ss.append(s)
            # Find repeating patterns in every axis
            #print(periods)
            #print(periods)
            if t % 100000 == 0:
                periods = [guess_seq_len(ss) for ss in states]
                print(periods)
            
                if periods.count(-1) == 0:
                    print(candidate, periods, candidate == periods)
                    if candidate and periods == candidate:
                        #return l
                        pfs = [prime_factors(p) for p in periods]
                        pftot = set()
                        for pfl in pfs:
                            for pf in set(pfl):
                                for c in range(pfl.count(pf)):
                                    pftot.add((pf,c))
                        #print(pftot)
                        product = 1
                        for pf,c in pftot:
                            product *= pf
                        print(periods)
                        print(product)
                        return product
                    else:
                        candidate = periods
                        
        t += 1
    return energy

input = sys.stdin.read().strip()

test1 = '''<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>'''

test2 = '''<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>'''

tests = [(1,test1,10,179,2772),(2,test2,100,1940,4686774924)]

for t,i,n,a1,a2 in tests:
    print('Test',t,'Part 1 - should be',a1,'-->','passed' if simulate(i,n) == a1 else 'failed')
    print('Test',t,'Part 2 - should be',a2,'-->','passed' if simulate(i,0) == a2 else 'failed')

print('Part 1: {}'.format(simulate(input, 1000)))
print('Part 2: {}'.format(simulate(input, 0)))

#periods = simulate(input, 500, True)
#print('Part 2: {}'.format(periods))

