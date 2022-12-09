"""Rock Paper Scissors

Part 2, new scoring
"""
import os

import requests
from s01 import HandShape


def score_match(match_str: str) -> int:
    """Given a match definition string, calculate the score

    Uses a bizarre scoring definition where the 'hand shape'
    that the player picks impacts the score

    For this modified version, the player now needs to chose a hand shape based on
    desired victory conditions:

        "Anyway, the second column says how the round needs to end: X means you need to
        lose, Y means you need to end the round in a draw, and Z means you need to win.
        Good luck!"

    """
    oppoent_letter, player_letter = match_str.split(" ")
    opponent_shape = HandShape.from_opponent_coice(oppoent_letter)

    if player_letter == "X":
        # Force player loss
        player_shape = HandShape(opponent_shape.defeats)
        victory_points = 0
    elif player_letter == "Y":
        # Force draw
        player_shape = HandShape(opponent_shape.name)
        victory_points = 3
    else:
        # Force victory
        player_shape = HandShape(opponent_shape.loses_to)
        victory_points = 6

    return victory_points + player_shape.shape_score


def test_score_match():
    """Use the known inputs/outputs from challenge"""
    matches = r"""A Y
    B X
    C Z""".splitlines()
    matches = [x.strip() for x in matches]

    total_score = sum(map(score_match, matches))
    assert total_score == 12


if __name__ == "__main__":
    # test_score_match()

    ses = requests.Session()
    ses.cookies.set("session", os.getenv("SESSION_TOKEN"))

    r = ses.get("https://adventofcode.com/2022/day/2/input")
    r.raise_for_status()

    # Maybe a better way to strip trailing newline?
    match_strs = [line for line in r.text.splitlines() if line]
    total_score = sum(map(score_match, match_strs))

    print(f"{len(match_strs)} matches, total score: {total_score}")
