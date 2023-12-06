data = """Time:        40     82     84     92
Distance:   233   1011   1110   1487"""
races_two = (40828492, 233101111101487)

races = [
    {"t":40, "d": 233},
    {"t":82, "d": 1011},
    {"t": 84, "d": 1110},
    {"t": 92, "d": 1487}
]


def get_record_beaters(race_time, record):
    return [i+1 for i,_ in enumerate([(race_time - s) * s for s in range(1, race_time)]) if _ > record]

all_count_methods = []
for race in races:
    count_methods = len(get_record_beaters(race.get("t"),race.get("d")))
    all_count_methods.append(count_methods)

result = 1
for m in all_count_methods:
    result = result * m


##p2
races_two = (40828492, 233101111101487)
record_beaters_two = get_record_beaters(races_two[0], races_two[1])
