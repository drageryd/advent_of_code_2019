import sys

def parse_data(data):
    # Parse input
    data = [i.split(' => ') for i in data.split('\n')]
    recepies = {}
    for inputs, output in data:
        # Get count and type of output
        output_amount, output_type = output.split(' ')
        recepies[output_type] = {'children':set(), 'amount':int(output_amount), 'components':{}}
        # Get counts and types of input components
        for i in inputs.split(', '):
            input_amount, input_type = i.split(' ')
            recepies[output_type]['components'][input_type] = int(input_amount)
            recepies[output_type]['children'].add(input_type)
    # Propagate children
    did_something = True
    while did_something:
        did_something = False
        for root in recepies:
            # Get childrens children
            children = recepies[root]['children']
            #print(root, children)
            for c in list(children):
                #print('',c)
                if c not in recepies:
                    continue
                childs_children = recepies[c]['children']
                #print('',childs_children)
                for cc in list(childs_children):
                    #print(' ',cc)
                    if cc not in children:
                        #print('   Adding',cc,'to',root)
                        did_something = True
                        recepies[root]['children'].add(cc)
    return recepies



def loop(inventory, recepies):
    queue = ['FUEL']
    # Loop until done
    while queue:
        #print(queue)
        # Get type at front of queue
        current_type = queue.pop(0)
        # Skip ORE
        if current_type == 'ORE':
            continue

        #print('unreacting',current_type)
        # Get current inventory
        #current_inventory = inventory[current_type]
        # Get recepie for that item
        needed_amount = recepies[current_type]['amount']

        # React all possible of this type
        total_reactions, amount_left = divmod(inventory[current_type], needed_amount)

        # Save inventory left
        inventory[current_type] = amount_left

        # Get parts of recepie
        parts = recepies[current_type]['components']
        #print(' parts',recepies[current_type]['components'])

        # Add parts to inventory and queue
        for part_type, part_amount in parts.items():
            inventory[part_type] += total_reactions * part_amount
            # Add to queue
            if part_type not in queue and part_type != 'ORE':
                queue.append(part_type)
        
        '''
        # While enough to perform reaction
        while inventory[current_type] >= needed_amount:
            # Remove amount
            inventory[current_type] -= needed_amount
        
            # Get parts of recepie
            parts = recepies[current_type]['components']
            print(' parts',recepies[current_type]['components'])

            # Add parts to inventory and queue
            for part_type, part_amount in parts.items():
                inventory[part_type] += part_amount
                # Add to queue
                if part_type not in queue and part_type != 'ORE':
                    queue.append(part_type)
        '''
        # If there is anything left in current amount check queue if any
        # remaining reaction will produce current type (which will add it to queue)
        if inventory[current_type] > 0:
            future = False
            for peek_type in queue:
                # If queued item produce current_type
                if current_type in recepies[peek_type]['children']:
                    future = True
                    break
            # Else add missing amount and queue type
            if not future:
                inventory[current_type] = needed_amount
                queue.append(current_type)
        
        #print('',inventory)
    return inventory['ORE']

def set_inventory(fuel_amount, recepies):
    # Go from FUEL to ORE and add components
    types = set([x for t in recepies for x in [t]+list(recepies[t]['components'].keys())])
    inventory = {t:0 for t in types}
    inventory['FUEL'] = fuel_amount
    return inventory

def solve(data, guess=0):
    recepies = parse_data(data)
    
    # Go from FUEL to ORE and add components
    if guess == 0:
        inventory = set_inventory(1, recepies)
        return loop(inventory, recepies)

    # Binary search until biggest guess resulting in ore < 1000000000000
    ore = 0
    committed = 0
    step_size = guess
    while True:
        # Set guess
        guess = committed + step_size
        # Calculate amount of ore
        inventory = set_inventory(guess, recepies)
        ore = loop(inventory, recepies)

        # If we overshoot, dont commit step_size
        if ore <= 1000000000000:
            committed += step_size
        # Test half step size
        print(step_size, guess, ore)
        if step_size == 0:
            break
        step_size = int(step_size / 2)
    return guess



    

a1 = 31
d1 = '''10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL'''

a2 = 165
d2 = '''9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL'''

a3 = 13312
b3 = 82892753
d3 = '''157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT'''

a4 = 180697
b4 = 5586022
d4 = '''2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF'''

a5 = 2210736
b5 = 460664
d5 = '''171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX'''


tests = [(1,d1,a1,None),(2,d2,a2,None),(3,d3,a3,b3),(4,d4,a4,b4),(5,d5,a5,b5)]
for t,d,a,b in tests:
    s1 = solve(d)
    print('Test',t,'Part 1 - should be',a,'--->','passed' if s1 == a else 'failed', s1)
    s2 = solve(d, int(1000000000000/s1))
    print('Test',t,'Part 2 - should be',b,'--->','passed' if s2 == b else 'failed', s2)

data = sys.stdin.read().strip()
s1 = solve(data)
print('Part 1: {}'.format(s1))
s2 = solve(data, int(1000000000000/s1))
print('Part 2: {}'.format(s2))
