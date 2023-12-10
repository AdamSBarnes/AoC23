sample="""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

USE_SAMPLE = False

if USE_SAMPLE:
    lines = sample.split('\n')
else:
    with open('data/day_09.txt', 'r') as f:
        lines = [l.replace('\n','') for l in f.readlines()]

input = []
for line in lines:
    input.append(
        [int(l) for l in line.split(" ")]
    )


def get_diffs(l):
    out = []
    for i, v in enumerate(l[:-1]):
        out.append(l[i + 1] - l[i])
    return out


def predict_next(active_seq):

    all_diffs = [active_seq]

    search_range = len(active_seq) - 1
    for i in range(search_range):
        diffs = get_diffs(active_seq)
        all_diffs.append(diffs)
        if diffs[0] == 0 and diffs.count(diffs[0]) == len(diffs):
            break

        active_seq = diffs

    reverse_diffs = [r for r in reversed(all_diffs)]

    for i in range(len(reverse_diffs) - 1):
        new_val = reverse_diffs[i][-1] + reverse_diffs[i + 1][-1]
        reverse_diffs[i + 1].extend([new_val])

    return reverse_diffs[-1][-1]

vals = [predict_next(l) for l in input]

sum(vals)