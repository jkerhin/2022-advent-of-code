from advent2022.day07 import s01

inputs = """$ cd /
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
7214296 k""".splitlines()


def test_total_filesize():
    root_dir = s01.navigate_directories(inputs)
    assert root_dir.total_size() == 48381165


def test_sum_sub_100k():
    result = s01.sum_sub_100k(inputs)
    assert result == 95437
