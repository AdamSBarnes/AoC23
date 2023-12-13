sample = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

USE_SAMPLE = False

if USE_SAMPLE:
    lines = [l for l in sample.split('\n')]
else:
    with open('data/day_13.txt', 'r') as f:
        lines = [l.replace('\n', '') for l in f.readlines()]

line_groups = []
last_idx = 0
for idx, row in enumerate(lines):
    if not (row.startswith("#") or row.startswith(".")):
        line_groups.append(lines[last_idx:idx])
        last_idx = idx + 1


def rotate_lines(lines):
    out=[]
    for i in range(len(lines[0])):
        str = ''
        for l in lines:
            str += l[i]
        out.append(str)
    return out


def find_reflection(lines):
    for idx, line in enumerate(lines):
        if idx == len(lines) - 1:
            break

        block1, block2 = idx + 1, len(lines) - idx - 1

        b1 = lines[:block1]
        b2 = lines[len(lines) - block2:]

        if len(b2) > len(b1):
            b2 = b2[:len(b1)]
        elif len(b1) > len(b2):
            b1 = b1[-len(b2):]

        if ''.join(b1) == ''.join([r for r in reversed(b2)]):
            return idx + 1
    return 0

outs = []
for lg in line_groups:
    row_reflections = find_reflection(lg)
    col_reflections = find_reflection(rotate_lines(lg))
    outs.append((row_reflections, col_reflections))


row_sums = sum([o[0] * 100 for o in outs])
col_sums = sum([o[1] for o in outs])

p1 = row_sums + col_sums

# part two

def find_reflection_two(lines):
    for idx, line in enumerate(lines):
        if idx == len(lines) - 1:
            break

        block1, block2 = idx + 1, len(lines) - idx - 1

        b1 = lines[:block1]
        b2 = lines[len(lines) - block2:]

        if len(b2) > len(b1):
            b2 = b2[:len(b1)]
        elif len(b1) > len(b2):
            b1 = b1[-len(b2):]

        s1, s2 = ''.join(b1), ''.join([r for r in reversed(b2)])
        mismatch_counter = 0
        for cidx, char in enumerate(s1):
            if char != s2[cidx]:
                mismatch_counter += 1
        if mismatch_counter == 1:
            return idx + 1
    return 0


outs_p2 = []
for lg in line_groups:
    row_reflections = find_reflection_two(lg)
    col_reflections = find_reflection_two(rotate_lines(lg))
    outs_p2.append((row_reflections, col_reflections))


row_sums_two = sum([o[0] * 100 for o in outs_p2])
col_sums_two = sum([o[1] for o in outs_p2])

p2 = row_sums_two + col_sums_two
