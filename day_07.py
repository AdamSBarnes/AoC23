import pandas as pd

USE_SAMPLE = False

sample = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

if USE_SAMPLE:
    lines = sample.split('\n')
else:
    with open('data/day_07.txt', 'r') as f:
        lines = [l.replace('\n','') for l in f.readlines()]

def split_line(l):
    ll = l.split(" ")
    return (ll[0], int(ll[1]))


inputs = [split_line(line) for line in lines]

cards = "AKQJT98765432"
hand_rank = ["five_kind", "four_kind", "full_house", "three_kind", "two_pair", "pair", "high"]

def rank_hand(hand_tuple):

    hand = hand_tuple[0]
    bet = hand_tuple[1]

    out_dict = {'input_hand': hand, 'bet': bet}

    tally = {}
    for char in hand:
        if char not in tally:
            tally[char] = 1
        else:
            tally[char] += 1

    ranks = [cards.find(char) for char in hand]
    for idx, rank in enumerate(ranks):
        out_dict[f"card_{idx}"] = rank

    matches = []
    for t in tally:
        if tally[t] == 5:
            matches.append("five_kind")
        elif tally[t] == 4:
            matches.append("four_kind")
        elif tally[t] == 3:
            matches.append("three_kind")
        elif tally[t] == 2:
            matches.append("pair")
        else:
            matches.append("high")

    if 'pair' in matches and 'three_kind' in matches:
        matches = ["full_house", ]

    if len([m for m in matches if m == "pair"]) == 2:
        matches = ["two_pair", ]

    matches_rank = []
    for m in matches:
        matches_rank.append([(m, i) for i, h in enumerate(hand_rank) if h == m][0])

    matches_rank.sort(key=lambda x: x[1], reverse=False)
    hand_result, hand_result_rank = matches_rank[0]

    out_dict['hand_result'] = hand_result
    out_dict['hand_result_rank'] = hand_result_rank

    return out_dict

scored_hands = [rank_hand(h) for h in inputs]

df = pd.DataFrame(scored_hands)

sorted_df = df.sort_values(by=["hand_result_rank", "card_0", "card_1", "card_2", "card_3", "card_4"], ascending=[False, False, False, False, False, False]).reset_index(drop=True).reset_index(drop=False)

sorted_df["index"] = sorted_df["index"] + 1
sorted_df["hand_return"] = sorted_df["index"] * sorted_df["bet"]

sum(sorted_df['hand_return'])