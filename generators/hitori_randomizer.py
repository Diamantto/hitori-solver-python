"""This module contains the hitori randomizer"""
import random

from generators.hitori_puzzles import puzzles
from solver.hitori_utils import InvalidInputError


class HitoriRandomizer:
    def __init__(self):
        self.puzzles = puzzles

    def generate_random_puzzle(self, size: int):
        if size < 2:
            raise InvalidInputError("Size should be greater than 1")
        puzzle_list = list(self.puzzles[str(size)])
        if puzzle_list is None:
            return None
        return random.choice(puzzle_list)
