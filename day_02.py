"""
The Elf would first like to know which games would have been possible if the bag contained
only 12 red cubes, 13 green cubes, and 14 blue cubes?
"""
import re

with open('data/day_two.txt', 'r') as f:
    lines = f.readlines()

samples = ["Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
           "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
           "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
           "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
           "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"]

colours = {"red": 12, "green": 13, "blue": 14}

def check_game(sample: str):
    game_number = int(sample.split(" ")[1].split(':')[0])

    sets = sample.split(":")[1].split(";")
    for set in sets:
        cubes = set.split(",")
        for cube in cubes:
            for colour in colours.keys():
                if colour in cube:
                    number = int(re.sub(r'[^0-9]', '', cube))
                    if number > colours.get(colour):
                        return 0
    return game_number

answer_one = sum([check_game(l) for l in lines])

def check_game_two(sample: str):
    maxes = {
        "green" : 0,
        "red" : 0,
        "blue" : 0
    }

    sets = sample.split(":")[1].split(";")
    for set in sets:
        cubes = set.split(",")
        for cube in cubes:
            for colour in colours.keys():
                if colour in cube:
                    number = int(re.sub(r'[^0-9]', '', cube))
                    if number > maxes.get(colour):
                        maxes[colour] = number
    return maxes.get("green") * maxes.get("blue") * maxes.get("red")

answer_two = sum([check_game_two(l) for l in lines])
