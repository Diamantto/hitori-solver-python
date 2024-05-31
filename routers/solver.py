"""Endpoints for the solver module."""
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Depends

from auth.utils import get_current_user
from database import DB
from generators.hitori_randomizer import HitoriRandomizer
from solver.hitori_utils import InvalidInputError
from solver.models import Condition
from solver.solver import HitoriSolver

router = APIRouter(
    prefix='/api',
    tags=['solver']
)


@router.post('/solve')
async def solve_puzzle(data: Condition, user: dict = Depends(get_current_user)) \
        -> Any:
    """Solve the matrix and return the solved puzzle."""
    try:
        solver = HitoriSolver(data.puzzle)
        result = solver.solve_hitori()
        if solution := result.get("solution"):
            await DB["history-puzzles"].insert_one({"puzzle": data.puzzle, "user": user['id']})
            return {
                "counter": result["counter"],
                "solution": solution,
                "puzzle": data.puzzle,
            }
        raise HTTPException(status_code=401, detail=result.get("error"))
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except TypeError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.get('/generate')
async def generate_matrix(size: int, user: dict = Depends(get_current_user)) -> Condition:
    """
    This endpoint generates a random matrix of rooms. You need to provide the number of rooms.
    In response, you will get a list of rooms (regions).
    """
    try:
        randomizer = HitoriRandomizer()
        data = randomizer.generate_random_puzzle(size)

        await DB["generated-matrices"].insert_one({"puzzle": data, "user": user['id']})

        return Condition(puzzle=data)
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
