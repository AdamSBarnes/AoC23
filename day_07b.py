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

cards = "AKQT98765432J"
hand_rank = ["five_kind", "four_kind", "full_house", "three_kind", "two_pair", "pair", "high"]

def rank_hand(hand_tuple):

    hand = hand_tuple[0]
    bet = hand_tuple[1]



    out_dict = {'input_hand': hand, 'bet': bet}

    tally = {}
    for char in hand:
        if char == "J":
            continue

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

    for _ in [c for c in hand if c == "J"]:
        try:
            current_hand = matches_rank[0][0]
            if current_hand == "high":
                new_hand = "pair"
            elif current_hand == "pair":
                new_hand = "three_kind"
            elif current_hand == "two_pair":
                new_hand = "full_house"
            elif current_hand == "three_kind":
                new_hand = "four_kind"
            elif current_hand == "four_kind":
                new_hand = "five_kind"
            else:
                new_hand = current_hand
        except IndexError:
            # assumption that nothing in matches rank means JJJJJ
            new_hand = "five_kind"

        new_hand_rank = [(new_hand, i) for i, h in enumerate(hand_rank) if h == new_hand][0]
        if matches_rank:
            matches_rank[0] = new_hand_rank
        else:
            matches_rank = [new_hand_rank,]

    hand_result, hand_result_rank = matches_rank[0]

    out_dict['hand_result'] = hand_result
    out_dict['hand_result_rank'] = hand_result_rank

    return out_dict

scored_hands = []
for i, h in enumerate(inputs):
    print(f"{i}:{h}")
    scored_hands.append(rank_hand(h))


df = pd.DataFrame(scored_hands)

sorted_df = df.sort_values(by=["hand_result_rank", "card_0", "card_1", "card_2", "card_3", "card_4"], ascending=[False, False, False, False, False, False]).reset_index(drop=True).reset_index(drop=False)

sorted_df["index"] = sorted_df["index"] + 1
sorted_df["hand_return"] = sorted_df["index"] * sorted_df["bet"]

sum(sorted_df['hand_return'])