"""Find common item in a single set"""
import os
from string import ascii_letters

import requests


def calculate_priority(sack: str) -> int:
    """Find the duplicated letter, and return its score

    Letter scoring is just `ascii_letters`, but 1-indexed instead of 0-indexed
    """
    ix_half = int(len(sack) / 2)
    first_compartment = set(sack[:ix_half])
    second_compartment = set(sack[ix_half:])
    common_letter = list(first_compartment & second_compartment)[0]
    return ascii_letters.index(common_letter) + 1


def test_prioritization():
    """Use the known inputs/outputs from challenge"""
    sacks = """vJrwpWtwJgWrhcsFMMfFFhFp
    jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    PmmdzqPrVvPwwTWBwg
    wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ttgJtRGJQctTZtZT
    CrZsJsPPZsGzwwsLwLmpwMDw""".splitlines()
    sacks = [x.strip() for x in sacks]

    total_score = sum(map(calculate_priority, sacks))
    assert total_score == 157


if __name__ == "__main__":
    test_prioritization()

    ses = requests.Session()
    ses.cookies.set("session", os.getenv("SESSION_TOKEN"))

    r = ses.get("https://adventofcode.com/2022/day/3/input")
    r.raise_for_status()

    # Maybe a better way to strip trailing newline?
    sack_strs = [line for line in r.text.splitlines() if line]
    total_score = sum(map(calculate_priority, sack_strs))

    print(f"{len(sack_strs)} sacks, total score: {total_score}")
