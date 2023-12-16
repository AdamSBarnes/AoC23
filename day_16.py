sample = R"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""

USE_SAMPLE = False

if USE_SAMPLE:
    lines = [l for l in sample.split('\n') if l]
else:
    with open('data/day_16.txt', 'r') as f:
        lines = [l.replace('\n', '') for l in f.readlines()]

headings = ["L", "R", "U", "D"]


def move(cur_pos):
    row, col, heading = cur_pos
    if row < 0 or col < 0:
        return []
    try:
        current_char = lines[row][col]
        #print(current_char)
    except IndexError:
        return []

    if current_char == ".":
        if heading == "R":
            col += 1
        elif heading == "L":
            col -= 1
        elif heading == "U":
            row -= 1
        elif heading == "D":
            row += 1
        return [(row, col, heading)]
    if current_char == "/":
        if heading == "R":
            row -= 1
            heading = "U"
        elif heading == "L":
            row += 1
            heading = "D"
        elif heading == "U":
            col += 1
            heading = "R"
        elif heading == "D":
            col -= 1
            heading = "L"
        return [(row, col, heading)]
    if current_char == "\\":
        if heading == "R":
            row += 1
            heading = "D"
        elif heading == "L":
            row -= 1
            heading = "U"
        elif heading == "U":
            col -= 1
            heading = "L"
        elif heading == "D":
            col += 1
            heading = "R"
        return [(row, col, heading)]
    if current_char == "|":
        if heading == "R" or heading == "L":
            return [(row - 1, col, "U"), (row + 1, col, "D")]
        elif heading == "U":
            row -= 1
        elif heading == "D":
            row += 1
        return [(row, col, heading)]
    if current_char == "-":
        if heading == "R":
            col += 1
        elif heading == "L":
            col -= 1
        elif heading == "U" or heading == "D":
            return [(row, col - 1, "L"), (row, col + 1, "R")]
        return [(row, col, heading)]


test_data = [
    [".", ".", "\\"],
    ["/", "|", "|"],
    ["\\", ".", "/"]
]

pos = (0, 0, "R")
visited = [pos, ]
positions = move(pos)

while True:
    if not positions:
        break
    new_positions = []
    print(positions)
    for p in positions:
        if not p or p[0] < 0 or p[1] < 0:
            continue
        visited.append(p)
        m = move(p)
        new_positions.append(m)

    positions = [pp for pp in sum(new_positions, []) if pp not in visited]

valid_visited = [[v[0], v[1]] for v in visited if v[0] < len(lines) and v[1] < len(lines[0])]

unique_visits = []
for v in valid_visited:
    if v not in unique_visits:
        unique_visits.append(v)

p1 = len(unique_visits)

## p2

def get_energised(r, c, h):
    pos = (r, c, h)
    visited = [pos, ]
    positions = move(pos)

    while True:
        if not positions:
            break
        new_positions = []
        #print(positions)
        for p in positions:
            if not p or p[0] < 0 or p[1] < 0:
                continue
            visited.append(p)
            m = move(p)
            new_positions.append(m)

        positions = [pp for pp in sum(new_positions, []) if pp not in visited]

    valid_visited = [[v[0], v[1]] for v in visited if v[0] < len(lines) and v[1] < len(lines[0])]

    unique_visits = []
    for v in valid_visited:
        if v not in unique_visits:
            unique_visits.append(v)

    return len(unique_visits)

potentials = []
#top & bottom row
for col in range(len(lines[0])):
    # down from every col in first row
    en = get_energised(0, col,"D")
    potentials.append(en)

    # up from every col in last row
    en = get_energised(len(lines), col, "U")
    potentials.append(en)

for row in range(len(lines)):
    # right from every row in first col
    en = get_energised(row, 0, "R")
    potentials.append(en)

    # left from every row in last col
    en = get_energised(row, len(lines[0]), "L")
    potentials.append(en)

p2 = max(potentials)

