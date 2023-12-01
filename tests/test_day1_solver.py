import re
import pytest

from Day1 import day1_solver

def test_single_occurrence():
    word = "hello"
    string = "hello world"
    expected_indices = [0]
    assert day1_solver.find_all_occurrences(word, string) == expected_indices

def test_multiple_occurrences():
    word = "o"
    string = "hello world"
    expected_indices = [4, 7]
    assert day1_solver.find_all_occurrences(word, string) == expected_indices

def test_no_occurrence():
    word = "foo"
    string = "hello world"
    expected_indices = []
    assert day1_solver.find_all_occurrences(word, string) == expected_indices

def test_find_matching_values():
    # Testing when inputline and search_values are empty
    assert day1_solver.find_matching_values("", []) == []

    # Testing when inputline is empty and search_values is not empty
    assert day1_solver.find_matching_values("", ["abc", "def"]) == []

    # Testing when inputline is not empty and search_values is empty
    assert day1_solver.find_matching_values("abc def ghi", []) == []

    # Testing when inputline and search_values have matching values
    assert day1_solver.find_matching_values("abc def ghi", ["abc", "ghi"]) == [("abc", 0), ("ghi", 8)]

    # Testing when inputline and search_values have no matching values
    assert day1_solver.find_matching_values("abc def ghi", ["xyz", "123"]) == []

    # Testing when search_values have duplicate values
    assert day1_solver.find_matching_values("abc abc abc", ["abc"]) == [("abc", 0), ("abc", 4), ("abc", 8)]

    # Testing when inputline has overlapping matching values
    assert day1_solver.find_matching_values("abcabcabc", ["abc"]) == [("abc", 0), ("abc", 3), ("abc", 6)]

    # Testing when inputline and search_values have matching values with different case
    assert day1_solver.find_matching_values("abc DEF ghi", ["abc", "DEF"]) == [("abc", 0), ("DEF", 4)]

    # Testing when inputline has spaces and search_values are longer strings
    assert day1_solver.find_matching_values("abc def ghi", ["abc def", "def ghi"]) == [("abc def", 0), ("def ghi", 4)]

def test_single_word():
    line = "one"
    assert day1_solver.join_first_last_numeric(line) == 11

def test_no_matching_values():
    line = "hello world"
    assert day1_solver.join_first_last_numeric(line) == 0

def test_multiple_matching_values():
    line = "one two three four five six"
    assert day1_solver.join_first_last_numeric(line) == 16

def test_matching_values_with_non_numeric_words():
    line = "five three two nine apple"
    assert day1_solver.join_first_last_numeric(line) == 59