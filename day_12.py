import re
import itertools

sample = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

USE_SAMPLE = False


def find_contiguous_blocks(text):
    pattern = re.compile(r'#+')
    matches = pattern.finditer(text)
    locations = [(match.start(), match.end()) for match in matches]
    return [l[1] - l[0] for l in locations]


if USE_SAMPLE:
    lines = [l for l in sample.split('\n') if l]
else:
    with open('data/day_12.txt', 'r') as f:
        lines = [l.replace('\n', '') for l in f.readlines()]

clean_lines = []
for line in lines:
    inputs = "." + line.split(" ")[0] + "."
    spring_lens = [int(i) for i in line.split(" ")[1].split(",")]
    clean_lines.append((inputs, spring_lens, len(inputs)))

line_lengths = list(set([len(c[0]) for c in clean_lines]))

all_possible_dict = {}
for l in line_lengths:
    all_possibles = [''.join(a) for a in itertools.product(["#", "."], repeat=l)]
    all_possibles = [(a, find_contiguous_blocks(a)) for a in all_possibles]
    all_possible_dict[l] = all_possibles

def check_match(pm, _str):
    for idx, char in enumerate(pm):
        if not (char == _str[idx] or _str[idx] == "?"):
            return None
    return pm

all_matches = []
for cl in clean_lines:
    _str, _ind, _len = cl
    potential_matches = [a[0] for a in all_possible_dict.get(_len) if a[1] == _ind]
    matches = []
    for pm in potential_matches:
        if check_match(pm, _str):
            matches.append(pm)
    all_matches.append(matches)

part_one = sum([len(m) for m in all_matches])