"""Find common item across three elves"""
import os
from string import ascii_letters
from typing import List

import requests


def calculate_badge_priority(sacks: List[str]) -> int:
    """Find the duplicated letter, and return its score

    Letter scoring is just `ascii_letters`, but 1-indexed instead of 0-indexed
    """
    a, b, c = map(set, sacks)
    common_letter = list(a & b & c)[0]
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

    total_score = calculate_badge_priority(sacks[:3]) + calculate_badge_priority(
        sacks[3:]
    )
    assert total_score == 70


if __name__ == "__main__":
    test_prioritization()

    ses = requests.Session()
    ses.cookies.set("session", os.getenv("SESSION_TOKEN"))

    r = ses.get("https://adventofcode.com/2022/day/3/input")
    r.raise_for_status()

    # Maybe a better way to strip trailing newline?
    sack_strs = [line for line in r.text.splitlines() if line]

    total_score, ix = 0, 0
    while ix < len(sack_strs):
        total_score += calculate_badge_priority(sack_strs[ix : ix + 3])
        ix += 3

    print(f"{len(sack_strs)} sacks, total score: {total_score}")
