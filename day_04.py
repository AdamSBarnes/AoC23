USE_SAMPLE = False

sample = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

if USE_SAMPLE:
    lines = sample.split('\n')
else:
    with open('data/day_04.txt', 'r') as f:
        lines = [l.replace('\n','') for l in f.readlines()]

## part one

score = 0
for line in lines:

    split = line.split(":")[1].split("|")
    winners = [w for w in split[0].split(" ") if w]
    mine = [w for w in split[1].split(" ") if w]

    sub_score = 0
    for number in mine:
        if number in winners:
            sub_score = 1 if sub_score == 0 else sub_score * 2

    score += sub_score

print(score)

### part two

def get_win_count(line):
    split = line.split(":")[1].split("|")
    winners = [w for w in split[0].split(" ") if w]
    mine = [w for w in split[1].split(" ") if w]
    matches = [m for m in mine if m in winners]
    return len(matches)

deck = {i: 1 for i, _ in enumerate(lines)}

for idx, line in enumerate(lines):
    win_count = get_win_count(line)
    for _idx in range(idx + 1, idx + 1 + win_count):
        deck[_idx] += 1 * deck.get(idx)

print(sum([v for v in deck.values()]))