sample = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

USE_SAMPLE = False

if USE_SAMPLE:
    lines = [l for l in sample.split('\n') if l]
else:
    with open('data/day_14.txt', 'r') as f:
        lines = [l.replace('\n', '') for l in f.readlines()]

original_lines = lines.copy()

def replace_char(string, index, new_char):
    string_list = list(string)
    string_list[index] = new_char
    result_string = ''.join(string_list)
    return result_string


def cycle(lines):
    rotated_lines = [''.join(l) for l in list(zip(*lines))]
    out_lines = []

    for line in rotated_lines:
        line_len = len(line)
        reverse_line = line#[::-1]

        for idx in range(line_len):
            if reverse_line[idx] == ".":
                offset = 1
                while True:
                    try:
                        if reverse_line[idx + offset] == ".":
                            offset += 1
                            continue
                        elif reverse_line[idx + offset] == "#":
                            break
                        else:
                            if idx + offset < line_len:
                                reverse_line = replace_char(reverse_line, idx + offset, ".")
                                reverse_line = replace_char(reverse_line, idx, "O")
                            break
                    except IndexError:
                        break
        out_lines.append(reverse_line)#[::-1])

    final_switch = []

    for oix, ol in enumerate(out_lines[0]):
        new_line = ''.join([o[oix] for o in out_lines])
        final_switch.append(new_line)

    return final_switch



def cycle_four(lines):

    #do north
    lines = cycle(lines)

    #rotate west
    lines = [''.join(l) for l in list(zip(*lines[::-1]))]
    lines = cycle(lines)

    # south
    lines = [''.join(l) for l in list(zip(*lines[::-1]))]
    lines = cycle(lines)

    #west
    lines = [''.join(l) for l in list(zip(*lines[::-1]))]
    lines = cycle(lines)

    lines = [''.join(l) for l in list(zip(*lines[::-1]))]
    return lines

sampled_lines = []
for _ in range(200):
    lines = cycle_four(lines)
    sampled_lines.append(lines)

f = []
for lines in sampled_lines:
    nums = []
    for ix, ol in enumerate(lines):
        num = len([c for c in ol if c == 'O']) * (len(lines) - ix)
        nums.append(num)
    f.append(sum(nums))


zz = []
for idx, _ in enumerate(f[:-1]):
    zz.append(f[idx + 1] - f[idx])

#starting at idx 108, pattern repeats of diffs
# 108 is
repeating_nums = f[108:126]

p2 = repeating_nums[(1000000000 - 109) % len(repeating_nums)]