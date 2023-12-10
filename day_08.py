USE_SAMPLE = False

sample = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


if USE_SAMPLE:
    lines = sample.split('\n')
else:
    with open('data/day_08.txt', 'r') as f:
        lines = [l.replace('\n','') for l in f.readlines()]

moves = lines[0]

map = {}

for line in lines[2:]:
    key = line.split(" ")[0]
    map[key] = {
        "L": line.split("=")[1][2:5],
        "R": line.split("=")[1][7:10]
    }

def cycle(start_key, move_count):
    key = start_key

    for char in moves:
        print(key)
        print(char)
        move_count +=1
        key = map.get(key).get(char)
        if key == "ZZZ":
            break

    return key, move_count

key = "AAA"
move_count = 0
while key != "ZZZ":
    key, move_count = cycle(key, move_count)