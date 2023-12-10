from math import lcm


USE_SAMPLE = False

sample = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


if USE_SAMPLE:
    lines = sample.split('\n')
else:
    with open('data/day_08.txt', 'r') as f:
        lines = [l.replace('\n','') for l in f.readlines()]


def cycle(start_key, move_count):
    key = start_key

    for char in moves:
        move_count +=1
        key = map.get(key).get(char)
        if key == "ZZZ":
            break

    return key, move_count


moves = lines[0]
map = {}

for line in lines[2:]:
    key = line.split(" ")[0]
    map[key] = {
        "L": line.split("=")[1][2:5],
        "R": line.split("=")[1][7:10]
    }

live_nodes = [k for (k, v) in map.items() if k.endswith('A')]


live_nodes_count = []

for node in live_nodes:
    key = node
    move_count = 0
    while not key.endswith("Z"):
        key, move_count = cycle(key, move_count)
    live_nodes_count.append(move_count)


result = lcm(*live_nodes_count)
