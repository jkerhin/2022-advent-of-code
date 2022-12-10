"""Paired elves, section overlap"""
import textwrap

from advent2022 import ses


def section_ids(spec: str) -> set:
    """Get the 'section ids' from a specification string

    >>> section_ids("2-4")
    {2, 3, 4}

    """
    low, high = map(int, spec.split("-"))
    return set(range(low, high + 1))


def has_fully_contained(pair_spec: str) -> bool:
    """Test whether either elf has sections that are completely contained by pair elf"""
    spec_l, spec_r = pair_spec.split(",")
    sec_l = section_ids(spec_l)
    sec_r = section_ids(spec_r)
    return sec_l.issubset(sec_r) or sec_r.issubset(sec_l)


def test_fully_contained_counts():
    pairs = """\
    2-4,6-8
    2-3,4-5
    5-7,7-9
    2-8,3-7
    6-6,4-6
    2-6,4-8"""
    pairs = textwrap.dedent(pairs).splitlines()

    count = sum(map(has_fully_contained, pairs))
    assert count == 2


if __name__ == "__main__":
    test_fully_contained_counts()

    r = ses.get("https://adventofcode.com/2022/day/4/input")
    r.raise_for_status()

    pair_specs = [line for line in r.text.splitlines() if line]

    count = sum(map(has_fully_contained, pair_specs))

    print(f"{len(pair_specs)} pairs, total with fully contained: {count}")
