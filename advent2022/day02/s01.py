"""Rock Paper Scissors

(note that `.env` was populated with SESSION_TOKEN; easy now that I'm using Pipenv)
"""
import os

import requests

SHAPE_SCORES = {
    "Rock": 1,
    "Paper": 2,
    "Scissors": 3,
}


class HandShape:
    def __init__(self, name: str) -> None:
        self.name = name
        self.shape_score = SHAPE_SCORES[name]

        if name == "Rock":
            self.defeats = "Scissors"
            self.loses_to = "Paper"
        elif name == "Paper":
            self.defeats = "Rock"
            self.loses_to = "Scissors"
        elif name == "Scissors":
            self.defeats = "Paper"
            self.loses_to = "Rock"

    @classmethod
    def from_opponent_coice(cls, choice: str):
        if choice.upper() == "A":
            return cls("Rock")
        elif choice.upper() == "B":
            return cls("Paper")
        elif choice.upper() == "C":
            return cls("Scissors")
        else:
            raise ValueError("A, B, C are only allowed choices")

    @classmethod
    def from_player_choice(cls, choice: str):
        if choice.upper() == "X":
            return cls("Rock")
        elif choice.upper() == "Y":
            return cls("Paper")
        elif choice.upper() == "Z":
            return cls("Scissors")
        else:
            raise ValueError("X, Y, Z are only allowed choices")


def score_match(match_str: str) -> int:
    """Given a match definition string, calculate the score

    Uses a bizarre scoring definition where the 'hand shape'
    that the player picks impacts the score

    """
    oppoent_letter, player_letter = match_str.split(" ")
    opponent_shape = HandShape.from_opponent_coice(oppoent_letter)
    player_shape = HandShape.from_player_choice(player_letter)

    if player_shape.defeats == opponent_shape.name:
        # Victory!
        return player_shape.shape_score + 6
    elif player_shape.loses_to == opponent_shape.name:
        # Loss
        return player_shape.shape_score + 0
    else:
        # Draw
        return player_shape.shape_score + 3


def test_score_match():
    """Use the known inputs/outputs from challenge"""
    matches = r"""A Y
    B X
    C Z""".splitlines()
    matches = [x.strip() for x in matches]

    total_score = sum(map(score_match, matches))
    assert total_score == 15


if __name__ == "__main__":
    # TODO: Move this to a common/utils location...
    ses = requests.Session()
    ses.cookies.set("session", os.getenv("SESSION_TOKEN"))

    r = ses.get("https://adventofcode.com/2022/day/2/input")
    r.raise_for_status()

    # Maybe a better way to strip trailing newline?
    match_strs = [line for line in r.text.splitlines() if line]
    total_score = sum(map(score_match, match_strs))

    print(f"{len(match_strs)} matches, total score: {total_score}")
