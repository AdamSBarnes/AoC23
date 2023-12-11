sample = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
"""

valid_moves = {
    "|": [["|", "7", "F"], ["|", "J", "L"], None, None],
    "-": [None, None, ["-", "F", "L"], ["-", "7", "J"]],
    "L": [["|", "7", "F"], None, None, ["-", "7", "J"]],
    "J": [["|", "7", "F"], None, ["-", "L", "F"], None],
    "7": [None, ["|", "L", "J"], ["-", "L", "F"], None],
    "F": [None, ["|", "L", "J"], None, ["-", "7", "J"]]
}

USE_SAMPLE = False

if USE_SAMPLE:
    lines = [l for l in sample.split('\n') if l]
else:
    with open('data/day_10.txt', 'r') as f:
        lines = [l.replace('\n', '') for l in f.readlines()]

lines = [["." * len(lines[0]), ], lines, ["." * len(lines[0]), ]]
lines = [f".{l}." for l in sum(lines,[])]

def find_start_pipe():
    for idx, row in enumerate(lines):
        for cidx, char in enumerate(row):
            if char == "S":
                return (idx, cidx)


sidx = find_start_pipe()


def find_start_pipe_type(sidx):
    brow, bcol = sidx

    pabove = lines[brow - 1][bcol]
    pbelow = lines[brow + 1][bcol]
    pleft = lines[brow][bcol - 1]
    pright = lines[brow][bcol + 1]

    for move in valid_moves:
        move_options = valid_moves[move]
        if (not bool(move_options[0]) or pabove in move_options[0]) and (
                not bool(move_options[1]) or pbelow in move_options[1]) and (
                not bool(move_options[2]) or pleft in move_options[2]) and (
                not bool(move_options[3]) or pright in move_options[3]):
            return move




new_lines = [l.replace("S", find_start_pipe_type(sidx)) for l in lines]

def find_valid_moves(sidx):
    brow, bcol = sidx
    current_char = new_lines[brow][bcol]

    out = []

    pabove = new_lines[brow - 1][bcol]
    pbelow = new_lines[brow + 1][bcol]
    pleft = new_lines[brow][bcol - 1]
    pright = new_lines[brow][bcol + 1]

    move_options = valid_moves[current_char]
    if bool(move_options[0]) and pabove in move_options[0]:
        out.append((-1, 0))
    if bool(move_options[1]) and pbelow in move_options[1]:
        out.append((1, 0))
    if bool(move_options[2]) and pleft in move_options[2]:
        out.append((0, -1))
    if bool(move_options[3]) and pright in move_options[3]:
        out.append((0, 1))

    return [(o[0] + brow, o[1] + bcol) for o in out]

visited = []

idx = sidx
move_count = 0

while True:
    print(idx)
    visited.append(idx)
    legal_moves = find_valid_moves(idx)
    idx_opts = [v for v in legal_moves if v not in visited]
    if len(idx_opts) == 0:
        break
    idx = idx_opts[0]
    move_count += 1


part_one = round(move_count / 2)

##part_two

import shapely

p = shapely.Polygon(visited)

proper = []
for ridx in range(len(new_lines)):
    for cidx in range(len(new_lines[0])):
        point = shapely.Point(ridx, cidx)
        if p.contains_properly(point):
            proper.append((ridx, cidx))

part_two = len(proper)
