import logging
from textwrap import dedent
from typing import List

from rich.logging import RichHandler
from rich.traceback import install

install(show_locals=True)
log = logging.getLogger("rich")


class Directory:
    def __init__(self, name: str) -> None:
        self.name = name

        self.files = dict()  # filename: filesize
        self.child_dirs = []

    def __repr__(self) -> str:
        out = f"{self.name}: ----------------"
        for fname, size in self.files.items():
            out += f"\n\t{fname} - {size}"
        for d in self.child_dirs:
            out += f"\n\t{d}"
        return out

    def total_size(self) -> int:
        size = 0
        size += sum(self.files.values())
        size += sum(d.total_size() for d in self.child_dirs)
        return size


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
    cwd = Directory("/")

    parent_dirs = []
    for ix, line in enumerate(inputs[1:]):
        log.debug("%d - %s", ix, str(cwd))
        log.debug(f"{ix} - Parent dirs: " + " ".join(d.name for d in parent_dirs))
        match line.split():
            case ["$", "ls"]:
                # Begin 'ls mode', a no-op
                log.debug("%d -starting 'ls'", ix)
                continue
            case ["$", "cd", ".."]:
                tmp: Directory = parent_dirs.pop(-1)
                log.debug(f"{ix} - 'cd ..' - moving from {cwd.name} to {tmp.name}")
                tmp.child_dirs.append(cwd)
                cwd = tmp
            case ["$", "cd", dirname]:
                log.debug(f"{ix} - Descending into {dirname}")
                parent_dirs.append(cwd)
                cwd = Directory(dirname)
            case ["dir", dirname]:
                # Any reason to do anything with these?
                log.debug(f"{ix} - directory - {dirname}")
                continue
            case [file_size, file_name]:
                log.debug(f"{ix} - adding file {file_name}")
                cwd.files[file_name] = int(file_size)
    # done processing inputs

    # Navigate back up the tree before returning
    while len(parent_dirs) > 0:
        pdir: Directory = parent_dirs.pop(-1)
        pdir.child_dirs.append(cwd)
        cwd = pdir

    log.info(str(cwd))
    return cwd


def sum_sub_100k(input: str) -> int:
    return 0


if __name__ == "__main__":
    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    inputs = """\
    $ cd /
    $ ls
    dir a
    14848514 b.txt
    8504156 c.dat
    dir d
    $ cd a
    $ ls
    dir e
    29116 f
    2557 g
    62596 h.lst
    $ cd e
    $ ls
    584 i
    $ cd ..
    $ cd ..
    $ cd d
    $ ls
    4060174 j
    8033020 d.log
    5626152 d.ext
    7214296 k
    """
    inputs = dedent(inputs).splitlines()
    d = navigate_directories(inputs)
    print(d.total_size())
