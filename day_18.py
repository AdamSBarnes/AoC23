import shapely


sample = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

USE_SAMPLE = False

if USE_SAMPLE:
    lines = [ll.split(" ") for ll in sample.split("\n") if ll]
else:
    with open('data/day_18.txt', 'r') as f:
        lines = [l.replace('\n', '').split(" ") for l in f.readlines() if l]

inputs = []
for l in lines:
    inputs.append((
        l[0],
        int(l[1]),
        l[2].replace("(","").replace(")", "")
    ))

start = (0,0)
visited = [start, ]

def move(dir, num):
    row, col = visited[-1]
    for i in range(1, num + 1):
        if dir == "R":
            visited.append((row, col + i))
        elif dir == "L":
            visited.append((row, col - i))
        elif dir == "U":
            visited.append((row - i, col))
        else:
            visited.append((row + i, col))


for i in inputs:
    move(i[0], i[1])

poly = shapely.Polygon(visited)
# 53300
poly.area + (poly.length / 2) + 1

### p2
inputs_two = []
for input in inputs:
    pass
    inputs_two.append((
        ["R", "D", "L", "U"][int(input[2][-1])],
        int(input[2][1:6], 16)
    ))

# much more efficient, should have done first
def move_two(dir, num):
    row, col = visited[-1]
    if dir == "R":
        visited.append((row, col + num))
    elif dir == "L":
        visited.append((row, col - num))
    elif dir == "U":
        visited.append((row - num, col))
    else:
        visited.append((row + num, col))


start = (0, 0)
visited = [start, ]

for i in inputs_two:
    move_two(i[0], i[1])

poly = shapely.Polygon(visited)
p2 = poly.area + (poly.length / 2) + 1

