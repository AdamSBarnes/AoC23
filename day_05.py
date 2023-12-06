USE_SAMPLE = False

sample = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

"""

if USE_SAMPLE:
    lines = sample.split('\n')
else:
    with open('data/day_05.txt', 'r') as f:
        lines = [l.replace('\n','') for l in f.readlines()]


def split_line(line):
    dest, source, num = [int(i) for i in line.split(" ")]
    return {
        "source_start": source,
        "source_end": source + num - 1,
        "offset":  dest - source
    }


def get_next_num(input_num, map_name):
    for v in maps.get(map_name):
        if v.get("source_start") <= input_num <= v.get("source_end"):
            return input_num + v.get("offset")
    return input_num


seeds = [int(l) for l in lines[0].split(":")[1].split(" ") if l]

maps = {l: {} for l in lines if l and 'map' in l}

for idx, map in enumerate(maps.keys()):
    start_map = [i for i,v in enumerate(lines) if v == map][0]
    end_map = start_map + [i for i,v in enumerate(lines[start_map:]) if not v][0]
    maps[map] = [split_line(l) for l in lines[start_map + 1:end_map]]

iter_locs = [k.split("-to-")[1].split(" ")[0] for k in maps.keys()]

def get_min_locs(seeds):

    seed_steps = {}
    for seed in seeds:
        seed_steps[seed] = {"seed": seed}

        key = "seed"

        for loc in iter_locs:
            name = f"{key}-to-{loc} map:"
            item_pos = seed_steps.get(seed).get(key)
            next_num = get_next_num(item_pos, name)
            seed_steps[seed][loc] = next_num
            key = loc

    return min([seed_steps.get(k).get('location') for k in seed_steps])

get_min_locs(seeds)

### part two
def get_loc(seed):
    key = 'seed'
    item_pos = seed
    for loc in iter_locs:
        name = f"{key}-to-{loc} map:"
        key = loc
        next_num = get_next_num(item_pos, name)
        item_pos = next_num
    return item_pos

new_seeds = []

for i in range(0,len(seeds),2):
    new_seeds.append((seeds[i], seeds[i] + seeds[i+1]))


rev_iter_locs = [l for l in reversed(iter_locs)][1:] + ['seed']

#reverse all the maps
reverse_maps = {}
for map in maps:
    new_maps = []
    for l in maps.get(map):
        new_map = {}
        new_map['source_start'] = l.get('source_start') + l.get('offset')
        new_map['source_end'] = l.get('source_end') + l.get('offset')
        new_map['offset'] = l.get('offset') * -1
        new_maps.append(new_map)
    name_parts = map.split(" ")[0].split("-")
    new_name = f"{name_parts[2]}-to-{name_parts[0]} map:"
    reverse_maps[new_name] = new_maps


def get_rev_num(input_num, map_name):
    for v in reverse_maps.get(map_name):
        if v.get("source_start") <= input_num <= v.get("source_end"):
            return input_num + v.get("offset")
    return input_num


rev_iter_locs = [l for l in reversed(iter_locs)][1:] + ['seed']

def get_reverse_loc(location):
    key = 'location'
    item_pos = location
    for loc in rev_iter_locs:
        name = f"{key}-to-{loc} map:"
        key = loc
        next_num = get_rev_num(item_pos, name)
        item_pos = next_num
    return item_pos

def in_list_ranges(num):
    for r in new_seeds:
        if r[0] <= num <= r[1]:
            return num
    return False

i = 0
while True:
    i += 1
    s = get_reverse_loc(i)
    if in_list_ranges(s):
        min_seed = i
        print(i)
        break
