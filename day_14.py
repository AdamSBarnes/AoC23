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

lines = [l for l in lines]
rotated_lines = [''.join(l) for l in list(zip(*lines))]

def replace_char(string, index, new_char):
    string_list = list(string)
    string_list[index] = new_char
    result_string = ''.join(string_list)
    return result_string


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

nums = []
for ix, ol in enumerate(final_switch):
    num = len([c for c in ol if c == 'O']) * (len(final_switch) - ix)
    nums.append(num)

sum(nums)
