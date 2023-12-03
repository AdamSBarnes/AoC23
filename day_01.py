import math

with open('data/day_one.txt', 'r') as f:
    lines = f.readlines()


def get_numbers(input: str):
    numbers = [s for s in input if s.isdigit()]
    return int(numbers[0] + numbers[-1])


sum([get_numbers(l) for l in lines])

map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}


def get_numbers_two(search_string: str):

    for m in map.keys():
        if search_string.find(m) >= 0:
            search_string = search_string.replace(m, f"{m}{map.get(m)}{m}")

    numbers = [s for s in search_string if s.isdigit()]

    return int(numbers[0] + numbers[-1])



test = ["two1nine","eightwothree","abcone2threexyz","xtwone3four","4nineeightseven2","zoneight234","7pqrstsixteen"]

get_numbers_two('3oneighth')

sum([get_numbers_two(l) for l in lines])

with open('out.txt', 'w') as f:
    for l in lines:
        f.write(str(get_numbers_two(l)))
        f.write("\n")

'xtwone3four'[10]
