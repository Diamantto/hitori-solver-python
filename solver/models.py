"""Models"""
from typing import List

from pydantic import BaseModel

from generators.hitori_puzzles import puzzles

example_data_for_docs: dict = {
    "puzzle": puzzles["5"][2]
}


class Condition(BaseModel):
    """Input data for the solver endpoint"""
    puzzle: List[List[int]]

    model_config = {
        "json_schema_extra": {
            "puzzle": example_data_for_docs,
        }
    }
