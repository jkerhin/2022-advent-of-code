from advent2022.day07 import s01, test_inputs


def test_total_filesize():
    root_dir = s01.navigate_directories(test_inputs)
    assert root_dir.total_size() == 48381165


def test_sum_sub_100k():
    root_dir = s01.navigate_directories(test_inputs)
    result = s01.sum_sub_100k(root_dir)
    assert result == 95437


def test_min_over_30M():
    root_dir = s01.navigate_directories(test_inputs)
    result = s01.find_min_over_30M(root_dir)
    assert result == 24933642
