from intcode import run
import sys

NIC = [int(n) for n in sys.stdin.read().strip().split(',')]

# Loop over the computers and move the data from outputs to inputs
def communicate(part):
    # Create every computer with an address and copy of program
    network = {address: {"input": [address], "memory": list(NIC), "output": [], "pr": (0, 0)} for address in range(50)}
    NAT = {"value": [], "last value": []}
    # Loop until breakpoint
    while True:
        # Assume idle
        idle = True
        for address, data in network.items():
            # If input is empty
            if not data["input"]:
                # Set input to -1
                data["input"].append(-1)
            else:
                # Network not idle
                idle = False
            # Run computer
            data["pr"] = run(data["input"],
                             data["memory"],
                             data["output"],
                             *data["pr"])
            # If there is any output it will be multiple of three values (address, X, Y)
            while data["output"]:
                new_address = data["output"].pop(0)
                X = data["output"].pop(0)
                Y = data["output"].pop(0)
                # If a NAT packet
                if new_address == 255:
                    if part == 1:
                        # Part 1 return Y
                        return Y
                    elif part == 2:
                        # Part 2 store in NAT unit (overwrite)
                        NAT["value"] = [X, Y]
                else:
                    # Send packet
                    network[new_address]["input"] += [X, Y]
                # If data was sent network is not idle
                idle = False
        # If idle is true here no computer received or sent anything
        if idle:
            # Wake NAT unit and send its data to 0
            network[0]["input"] += NAT["value"]
            # If last Y value sent is the same as this, return
            if NAT["last value"] and NAT["value"][1] == NAT["last value"][1]:
                return NAT["value"][1]
            # Store last sent value
            NAT["last value"] = NAT["value"]

# Part 1
print("Part 1: {}".format(communicate(1)))

# Part 1
print("Part 2: {}".format(communicate(2)))
