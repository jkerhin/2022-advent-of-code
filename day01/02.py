"""Solve bonus day 1 challenge

A little more explicit with Elf dataclass
"""
from dataclasses import dataclass

import requests


@dataclass
class Elf:
    num: int
    snack_cal: int


# Same data
ses = requests.Session()
ses.cookies.set("session", "536xxxx")  # Redacted
r = ses.get("https://adventofcode.com/2022/day/1/input")

elves = []
for ix, chunk in enumerate(r.text.split("\n\n")[:-1]):
    cal = sum(map(int, chunk.split("\n")))
    elves.append(Elf(ix, cal))

# Top three elves
print(sorted(elves, key=lambda e: e.snack_cal, reverse=True)[:3])

# Their calories
print(
    sum(e.snack_cal for e in sorted(elves, key=lambda e: e.snack_cal, reverse=True)[:3])
)
