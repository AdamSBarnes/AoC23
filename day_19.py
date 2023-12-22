import re

#['in', 'qqz', 'qs', 'lnx', 'A']
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

USE_SAMPLE = False

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
nodes = list(wf_map.keys())

node = 'in'
edges = []

def recurse(cn):
    rules = wf_map.get(cn)
    connecting_nodes = [r.split(":")[1] for r in rules[:-1]] + [rules[-1]]
    for n in connecting_nodes:
        new_combo = (cn, n)
        if new_combo not in edges:
            edges.append((cn, n))
        if n not in ["A", "R"]:
            recurse(n)

recurse(node)

graph = {}
for node in nodes:
    graph[node] = [e[1] for e in edges if e[0] == node]

all_paths = []

def fap(s, p=[]):
    p = p + [s,]
    if s in ("A", "R"):
        all_paths.append(p)
        return None
    for n in graph.get(s):
        fap(n, p)

def flatten_nested_list(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_nested_list(item))
        else:
            result.append(item)
    return result


fap('in')
valid_paths = [p for p in all_paths if p[-1] == "A"]

path_logic = {}
#wf = 'lnx'
for wf in wf_map:
    path_logic[wf] = {}
    source = wf
    neg_rules = []
    for rule in wf_map.get(wf):
        print(rule)
        if ":" in rule:
            rule_logic, dest = rule.split(":")
            rev = rule_logic.replace("<", ">=") if "<" in rule else rule_logic.replace(">","<=")
            out_rule = [rule_logic] + neg_rules
            neg_rules.append(rev)
        else:
            dest = rule
            out_rule = neg_rules
        if not path_logic[wf].get(dest):
            path_logic[wf][dest] = {'raw': out_rule}
        else:
            path_logic[wf][dest]['raw'].append(out_rule)

    path_logic[wf][dest]['raw'] = flatten_nested_list(path_logic[wf][dest]['raw'])

    for dest in path_logic[wf].keys():
        for char in ["x", "m", "a", "s"]:
            char_rules = []
            print(char)
            if not path_logic[wf][dest].get(char):
                path_logic[wf][dest][char] = []
            relevant_rules = [r for r in path_logic[wf][dest]['raw'] if r[0] == char]
            print(relevant_rules)
            if relevant_rules:
                path_logic[wf][dest][char].append(f'({" or ".join(relevant_rules)})')

chars = ["x", "m", "a", "s"]
all_node_rules = []
for path in valid_paths:
    path_char_logic = {k: [] for k in chars}
    for idx, node in enumerate(path[:-1]):
        n1 = node
        n2 = path[idx + 1]
        for char in chars:
            logic = path_logic.get(n1).get(n2).get(char)
            if logic:
                path_char_logic[char].extend(logic)


    for char in chars:
        #if not path_char_logic[char]:
        #    continue
        path_char_logic[char] = " and ".join([p for p in path_char_logic[char] if p])

    all_node_rules.append(path_char_logic)

def prod(l):
    result = 1
    for x in l:
        result = result * x
    return result

def replace_matching_char(input_str, char_to_replace, replacement_char):
    pattern = re.compile(f"{re.escape(char_to_replace)}(?=[<>])")
    result = re.sub(pattern, replacement_char, input_str)
    return result


def eval_path(logic: dict):
    x = []
    for char in ["x", "m", "a", "s"]:
        char_vals = 0
        char_logic = logic.get(char)
        if char_logic == '':
            x.append(4000)
            continue

        for i in range(1,4001):
            eval_term = replace_matching_char(char_logic, char, str(i))

            res = eval(eval_term)
            if res:
                char_vals += 1
        x.append(char_vals)
    return x


p2 = [eval_path(l) for l in all_node_rules]
import pandas as pd

df = pd.DataFrame(p2, columns=chars)
df['path'] = [' '.join(v) for v in valid_paths]

jj = path_logic['zc']
#['m<1722:A', 'x>1506:A', 'x>1464:R', 'A']

wf_map['zc']