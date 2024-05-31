"""Tests for the `generate_rooms` function in `solver/rooms_generator.py`."""
import random

import pytest

from generators.hitori_randomizer import HitoriRandomizer
from solver.hitori_utils import InvalidInputError


def test_generate_rooms_valid_input():
    """Test for valid input."""
    randomizer = HitoriRandomizer()

    size = 5
    result = randomizer.generate_random_puzzle(size)
    assert isinstance(result, list)


def test_generate_rooms_invalid_input():
    """Test for invalid input."""
    randomizer = HitoriRandomizer()
    with pytest.raises(InvalidInputError) as exc_info:
        size = 1  # Size less than 2
        randomizer.generate_random_puzzle(size)
    assert str(
        exc_info.value) == "Size should be greater than 1"


def test_generate_rooms_output():
    """Test the output of the `generate_rooms` function."""
    # Define a fixed random seed for predictable results
    randomizer = HitoriRandomizer()
    random.seed(0)
    size = 5
    result = randomizer.generate_random_puzzle(size)
    assert isinstance(result, list)
    # assert len(result) == size

    # Assuming each room is represented as a dictionary with keys as coordinates
    # and values as room symbols
    for row in result:
        assert isinstance(row, list)
