"""Failed attempt at day7 question 2:

That's not the right answer; your answer is too high. If you're stuck, make sure you're
using the full input data; there are also some general tips on the about page, or you
can ask for hints on the subreddit. Please wait one minute before trying again.
(You guessed 37948890.) [Return to Day 7]

30000000 - Minimum
37948890 - Too High
48381165 - Current (????) - Ugh, passed test_inputs instead of actuals!
37948890 - What?!?! Wrong again? - Well, at least I re-read the problem before submitting
7068748  - This is the correct answer

Did not read word problem closely enough - weren't looking for smallest node >30M, were
looking to determine current free space, how much minimally required to get the 30M,
and then which directory minimally exceeds the needed size

Update: Coroutines (`yield from`) while elegant, were more complex than needed. A simple
list that gets accumulated was a much easier way to track state
"""
import logging
from typing import List, Optional

from rich.logging import RichHandler
from rich.traceback import install

from advent2022 import ses
from advent2022.day07 import test_inputs

install(show_locals=True)
log = logging.getLogger("rich")


class Directory:
    def __init__(self, name: str, parent_dir: Optional["Directory"] = None) -> None:
        self.name = name
        self.parent_dir = parent_dir

        self.files = dict()  # filename: filesize
        self.child_dirs = []

    def __repr__(self) -> str:
        out = f"{self.name}: ----------------"
        for fname, size in self.files.items():
            out += f"\n\t{fname} - {size}"
        for d in self.child_dirs:
            c_dir_str = str(d)
            for line in c_dir_str.splitlines():
                out += f"\n\t{line}"
        return out

    def total_size(self) -> int:
        size = 0
        size += sum(self.files.values())
        size += sum(d.total_size() for d in self.child_dirs)
        return size

    @staticmethod
    def traverse(cwd: Optional["Directory"], traversed_directories: List["Directory"]):
        """Append the current directory, and return any child directories"""
        traversed_directories.append(cwd)

        if len(cwd.child_dirs) > 0:
            for child in cwd.child_dirs:
                Directory.traverse(child, traversed_directories)


def navigate_directories(inputs: List[str]) -> Directory:
    """Given a list of inputs, navigate the directories and return root directory

    Commands are prefixed with a '$'. Availible commands:
        $ cd dirname
        $ cd ..
        $ ls

    Hey! A good use of the new `match` statement introduced in 3.10
    """
    if inputs[0] != "$ cd /":
        raise IOError("Not starting at root directory!")
    root_dir = Directory("/")
    cwd = root_dir

    for ix, line in enumerate(inputs[1:]):
        log.debug("%d - %s", ix, str(cwd))
        match line.split():
            case ["$", "ls"]:
                # Begin 'ls mode', a no-op
                log.debug("%d -starting 'ls'", ix)
                continue
            case ["$", "cd", ".."]:
                parent = cwd.parent_dir
                log.debug(f"{ix} - 'cd ..' - moving from {cwd.name} to {parent.name}")
                cwd = parent
            case ["$", "cd", dirname]:
                log.debug(f"{ix} - Descending into {dirname}")
                child = Directory(dirname, parent_dir=cwd)
                cwd.child_dirs.append(child)
                cwd = child
            case ["dir", dirname]:
                # Any reason to do anything with these?
                log.debug(f"{ix} - directory - {dirname}")
                continue
            case [file_size, file_name]:
                log.debug(f"{ix} - adding file {file_name}")
                cwd.files[file_name] = int(file_size)
    # done processing inputs

    log.info(str(root_dir))
    return root_dir


def sum_sub_100k(root_dir: Directory) -> int:
    """Find the total size of all directories whose contents are less than 100000b"""
    all_dirs = []
    Directory.traverse(root_dir, all_dirs)

    total = 0
    for d in all_dirs:
        d: Directory = d
        size = d.total_size()
        log.debug(f"Checking size of {d.name} - {size}")
        if size <= 100_000:
            total += size
            log.info(f"{d.name} is small")

    return total


def find_min_over_30M(root_dir: Directory, system_total_size: int = 70_000_000) -> int:
    """Given a fixed system size, find minimal directory needed for 30M free space

    system_total_size defines the total space availible on the system

    Find the minimally sized directory that can be deleted to bring unallocated storage
    up to 30_000_000 bytes, and return the size of that directory

    """
    current_allocated_space = root_dir.total_size()
    current_free_space = system_total_size - current_allocated_space
    log.info(
        "%d currently allocated (%d free)", current_allocated_space, current_free_space
    )
    needed_free_space = 30_000_000 - current_free_space
    log.info("Need to free %d", needed_free_space)

    all_dirs = []
    Directory.traverse(root_dir, all_dirs)

    dir_sizes = [d.total_size() for d in all_dirs]
    log.debug(dir_sizes)
    for size in sorted(dir_sizes):
        if size >= needed_free_space:
            # Since we've sorted the sizes, the first one will be the solution
            return size


if __name__ == "__main__":
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    root_dir = navigate_directories(test_inputs)
    print(root_dir.total_size())
    total_sub = sum_sub_100k(root_dir)
    print(f"Total sub 100k: {total_sub}")

    r = ses.get("https://adventofcode.com/2022/day/7/input")
    r.raise_for_status()

    inputs = [line for line in r.text.splitlines() if line]
    root_dir = navigate_directories(inputs)

    total_sub = sum_sub_100k(root_dir)
    print(f"{len(inputs)} instructions - {total_sub}")

    min_dir_size = find_min_over_30M(root_dir)
    print(f"Minimal size > 30M: {min_dir_size}")
