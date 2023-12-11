sample = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

USE_SAMPLE = False

if USE_SAMPLE:
    lines = [l for l in sample.split('\n') if l]
else:
    with open('data/day_11.txt', 'r') as f:
        lines = [l.replace('\n', '') for l in f.readlines()]


new_lines = lines

row_breaks = []
for i, l in enumerate(lines):
    if l == "." * len(l):
        row_breaks.append(i)


col_chars = []
for c in range(len(new_lines[0])):
    chars = []
    for i, l in enumerate(new_lines):
        chars.append(new_lines[i][c])
    col_chars.append(chars)

col_breaks = []
for idx, col in enumerate(col_chars):
    if ''.join(col) == "." * len(col):
        col_breaks.append(idx)

map = []
for li, line in enumerate(new_lines):
    for ci, char in enumerate(line):
        if char == "#":
            map.append((li, ci))


pairs = []
for i, m in enumerate(map):
    x, y = m
    pair_list = []
    for mm in map:
        if mm[0] >= x and m != mm:
            pair_list.append(mm)
    pairs.append(pair_list)

matched_pairs = []
for i, m in enumerate(map):
    for p in pairs[i]:
        fp = [m, p]
        if [p, m] not in matched_pairs:
            matched_pairs.append(fp)


def dist(pair, line_val):
    r1, c1 = pair[0]
    r2, c2 = pair[1]

    r = abs(r1 - r2)
    d = abs(c1 - c2)

    for rd in range(r1, r2):
        if rd in row_breaks:
            r += line_val - 1

    for cd in range(min(c1,c2),max(c1,c2)):
        if cd in col_breaks:
            d += line_val - 1

    return r + d

#part one
out = sum([dist(p, 2) for p in matched_pairs])

#part two
out_two = sum([dist(p, 1000000) for p in matched_pairs])