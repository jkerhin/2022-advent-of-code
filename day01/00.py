"""Orienting myself in the repl before pulling the data
"""

elf = r"""1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

elves = elf.split("\n\n")

for i, e in enumerate(elves):
    cal = sum(map(int, e.split("\n")))
    print(f"{i}: {cal}")
