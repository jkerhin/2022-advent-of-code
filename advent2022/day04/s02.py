"""Paired elves, section overlap"""
import textwrap

from advent2022 import ses
from advent2022.day04.s01 import section_ids


def has_overlap(pair_spec: str) -> bool:
    """Test whether there is any overlap between elf sections"""
    spec_l, spec_r = pair_spec.split(",")
    sec_l = section_ids(spec_l)
    sec_r = section_ids(spec_r)
    return not sec_l.isdisjoint(sec_r)


def test_overlap_counts():
    pairs = """\
    2-4,6-8
    2-3,4-5
    5-7,7-9
    2-8,3-7
    6-6,4-6
    2-6,4-8"""
    pairs = textwrap.dedent(pairs).splitlines()

    count = sum(map(has_overlap, pairs))
    assert count == 4


if __name__ == "__main__":
    test_overlap_counts()

    r = ses.get("https://adventofcode.com/2022/day/4/input")
    r.raise_for_status()

    pair_specs = [line for line in r.text.splitlines() if line]

    count = sum(map(has_overlap, pair_specs))

    print(f"{len(pair_specs)} pairs, total with any overlap: {count}")
