sample = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

USE_SAMPLE = True

if USE_SAMPLE:
    lines = sample.split("\n")
else:
    with open('data/day_19.txt', 'r') as f:
        lines = [l.replace('\n', '') for l in f.readlines()]

workflows = lines[:[idx for idx, val in enumerate(lines) if not val][0]]
inputs = [l.replace("}","").replace("{","").split(",") for l in lines[[idx for idx, val in enumerate(lines) if not val][0] + 1:]]
inputs = [{
    "x": int(i[0].split("=")[1]),
    "m": int(i[1].split("=")[1]),
    "a": int(i[2].split("=")[1]),
    "s": int(i[3].split("=")[1])
} for i in inputs]

def _eval(rules, x=None, m=None, a=None, s=None):
    _else = rules[-1]
    for rule in rules[:-1]:
        r1, r2 = rule.split(":")
        t = eval(r1)
        if t:
            return r2
    return _else

wf_map = {}
for wf in workflows:
    name = wf[:wf.find("{")]
    rules = wf[wf.find("{") + 1: wf.find("}")].split(",")
    wf_map[name] = rules

accepted = []
rejected = []

for i in inputs:
    workflow = 'in'
    while True:
        new_workflow = _eval(wf_map.get(workflow), **i)
        if new_workflow == "A":
            accepted.append(i)
            break
        elif new_workflow == "R":
            rejected.append(i)
            break
        else:
            workflow = new_workflow

p1 = sum([sum(a.values()) for a in accepted])

#p2
for wf in wf_map:
    m = wf_map.get(wf)
    wf_map.get('in')
