import re

with open('data/day_03.txt', 'r') as f:
    lines = f.readlines()

lines = [l.replace('\n','') for l in lines]

def contains_non_numeric_or_period(input_string):
    pattern = re.compile(r'[^0-9.]')
    match = pattern.search(input_string)
    return bool(match)


def find_specific_number_positions(input_string, target_number):
    pattern = fr'(?<!\d){re.escape(target_number)}(?!\d)'
    matches = [(match.start(), match.end()) for match in re.finditer(pattern, input_string)]

    return matches

#get all the part numbers
all_parts = list(set([re.sub(r'[^0-9]', '', s) for s in re.split(r'[^0-9]', ".".join(lines)) if s != '']))

def is_part(lines, line_idx, part_positions, print_debug=False):
    matches = 0
    chars = []
    for part_pos in part_positions:
        start = part_pos[0]
        end = part_pos[1]
        
        # immediately before
        if start > 0:
            chars.append(lines[line_idx][start - 1])

        # immediately after
        if end < len(lines[line_idx]) - 1:
            chars.append(lines[line_idx][end])

        search_range = range(start, end)

        # line above
        for s in search_range:
            if s == 0:
                offsets = [0, 1]
            elif s == len(lines[line_idx]) - 1:
                offsets = [-1, 0]
            else:
                offsets = [-1, 0, 1]

            for offset in offsets:
                if line_idx > 0:
                    #print(f"searching line {line_idx - 1} at position {s + offset}")
                    chars.append(lines[line_idx - 1][s + offset])
                if line_idx < len(lines) - 1:
                    #print(f"searching line {line_idx + 1} at position {s + offset}")
                    chars.append(lines[line_idx + 1][s + offset])
        
        for c in chars:
            if contains_non_numeric_or_period(c):
                matches +=1
                break
    return matches

matches = []
for part in all_parts:
    for line_idx, line in enumerate(lines):
        part_positions = find_specific_number_positions(line, part)
        if part_positions:
            part_instances = is_part(lines, line_idx, part_positions, True)
            matches.append(part_instances * int(part))

sum(matches)

# part two
# maybe should have done this first up..?
number_map = {}
for line_idx, line in enumerate(lines):
    number_map[line_idx] = {}
    numbers_on_line = [s for s in re.split(r'[^0-9]', line) if s != '']
    for number in numbers_on_line:
        locs = find_specific_number_positions(line, number)
        for loc in locs:
            for i in range(loc[0], loc[1]):
                number_map[line_idx][i] = number          

                                                     
def is_gear(lines, line_idx, char_index):
    
    matched_numbers = []
    # immediately before
    if char_index > 0:
        if lines[line_idx][char_index - 1].isdigit():
            matched_numbers.append(number_map[line_idx][char_index - 1])

    # immediately after
    if char_index < len(lines[line_idx]) - 1:
        if lines[line_idx][char_index + 1].isdigit():
            matched_numbers.append(number_map[line_idx][char_index + 1])

    # line above
    if char_index == 0:
        offsets = [0, 1]
    elif char_index == len(lines[line_idx]) - 1:
        offsets = [-1, 0]
    else:
        offsets = [-1, 0, 1]

    for offset in offsets:
        if line_idx > 0:
            if lines[line_idx - 1][char_index + offset].isdigit():
                matched_numbers.append(number_map[line_idx - 1][char_index + offset])

        if line_idx < len(lines) - 1:
            if lines[line_idx + 1][char_index + offset].isdigit():
                matched_numbers.append(number_map[line_idx + 1][char_index + offset])
        
    out_nums = list(set([int(m) for m in matched_numbers]))
    if len(out_nums) == 2:
        return out_nums[0] * out_nums[1]
    else:
        return 0

gears = []
for line_idx, line in enumerate(lines):
    for char_idx, char in enumerate(line):
        if char == '*':
            gears.append(is_gear(lines, line_idx, char_idx))   

sum(gears)