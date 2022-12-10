"""Moving crates"""
import re
import textwrap
from collections import defaultdict
from typing import Dict, List

from advent2022 import ses


class CrateStacks:
    def __init__(self, stacks: Dict[int, List[str]]) -> None:
        self.stacks = stacks

    def __repr__(self) -> str:
        return f"CrateStacks: {self.stacks}"

    def move_crate(self, source: int, destination: int) -> None:
        """Move topmost crate from `source` to `destination`"""
        self.stacks[destination].append(self.stacks[source].pop())

    def move_multiple_crates(
        self, n_crates: int, source: int, destination: int
    ) -> None:
        """Move top n_crates from `source` to `destination`"""
        tmp = self.stacks[source][-1 * n_crates :]
        self.stacks[source] = self.stacks[source][: -1 * n_crates]
        self.stacks[destination].extend(tmp)

    def execute_instruction(self, instruction: str, one_by_one: bool = True) -> None:
        """Parse the instruction, and move crates according to direction

        Sample instruction:
            "move 3 from 1 to 3"

        Will move move the top three crates from stack `1` placing them onto stack `3`

        The `one_by_one` parameter defines whether crates will be moved one at a time
        (resulting in them being stacked in opposite order in destination stack) or all
        at once (resulting with them in the same order on the destination stack)

        """
        m = re.match(
            r"move (?P<n_moves>\d+) from (?P<src>\d+) to (?P<dst>\d+)", instruction
        )
        vals = {k: int(v) for k, v in m.groupdict().items()}

        if one_by_one:
            for _ in range(vals["n_moves"]):
                self.move_crate(source=vals["src"], destination=vals["dst"])
        else:
            self.move_multiple_crates(vals["n_moves"], vals["src"], vals["dst"])

    def check_top_crates(self) -> str:
        """All the crate letters for the top crate from each stack"""
        return "".join(self.stacks[k][-1] for k in sorted(self.stacks.keys()))

    @classmethod
    def from_ascii(cls, ascii_in: str) -> "CrateStacks":
        """Build a CrateStacks object from the ASCII-art input

        Uses a regex to find the indicies of the "stack" numbers, and then uses these
        indicies to build up the stacks

        """
        lines = ascii_in.splitlines()

        header = lines.pop()
        lines.reverse()

        matches = list(re.finditer(r"(\d)", header))
        stacks = defaultdict(list)

        for line in lines:
            for m in matches:
                crate = line[m.start()]
                if crate == " ":
                    continue
                stack_num = int(m.group(1))
                stacks[stack_num].append(crate)

        return cls(dict(stacks))


def test_ascii_parser():
    # Grr... trailing whitespace pre-commit stage jacks this up, so
    # need to have non-standard art...
    ascii_in = """\
        [D]     |
    [N] [C]     |
    [Z] [M] [P] |
     1   2   3  |
    """
    ascii_in = textwrap.dedent(ascii_in)

    cs = CrateStacks.from_ascii(ascii_in)

    ref_stacks = {1: list("ZN"), 2: list("MCD"), 3: list("P")}
    test_stacks = cs.stacks

    assert ref_stacks == test_stacks


def test_move_one_by_one():
    stacks = CrateStacks({1: list("ZN"), 2: list("MCD"), 3: list("P")})

    instructions = """\
    move 1 from 2 to 1
    move 3 from 1 to 3
    move 2 from 2 to 1
    move 1 from 1 to 2"""
    instructions = textwrap.dedent(instructions).splitlines()

    for instruction in instructions:
        stacks.execute_instruction(instruction, one_by_one=True)

    assert stacks.check_top_crates() == "CMZ"


def test_move_multiple():
    stacks = CrateStacks({1: list("ZN"), 2: list("MCD"), 3: list("P")})

    instructions = """\
    move 1 from 2 to 1
    move 3 from 1 to 3
    move 2 from 2 to 1
    move 1 from 1 to 2"""
    instructions = textwrap.dedent(instructions).splitlines()

    for instruction in instructions:
        stacks.execute_instruction(instruction, one_by_one=False)

    assert stacks.check_top_crates() == "MCD"


def solve_challenge():
    r = ses.get("https://adventofcode.com/2022/day/5/input")
    r.raise_for_status()

    all_lines = r.text.splitlines()

    ascii = "\n".join(all_lines[:9])
    instructions = [x for x in all_lines[10:] if x]
    print(f"{len(instructions)} total instructions")

    cs = CrateStacks.from_ascii(ascii)
    for instruction in instructions:
        cs.execute_instruction(instruction, one_by_one=True)

    print(f"Moving one-by-one, the answer is {cs.check_top_crates()}")

    cs = CrateStacks.from_ascii(ascii)
    for instruction in instructions:
        cs.execute_instruction(instruction, one_by_one=False)

    print(f"Moving multiple each time, the answer is {cs.check_top_crates()}")


if __name__ == "__main__":
    test_move_one_by_one()
    test_move_multiple()
    test_ascii_parser()
    solve_challenge()
