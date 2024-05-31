"""Solver module."""
from solver.hitori_utils import InvalidInputError


class HitoriSolver:
    """Solver class"""

    def __init__(self, puzzle):
        self.puzzle = puzzle

    def solve_hitori(self):
        """Main method of solver"""
        return self.solve_smart(self.puzzle)

    def solve_smart(self, puzzle):
        """CSP with Forward checking / MRV"""
        counter = 0
        nodes = [[0, 0]]
        states = [self.load_puzzle(puzzle)]

        while nodes:
            i, j = nodes.pop()
            state = states.pop()

            if self.check_solution(state):
                return {
                    "counter": counter,
                    "solution": state['puzzle'],
                }

            if i >= len(state['puzzle']):  # If out of bounds i.e. last cell as been reached
                continue

            state = self.cell_surrounded(state, i, j)
            if not state:
                continue

            # Go through the remaining values in the domain
            for d in state['domain'][i][j]:

                # If initial domain is white i.e. 'V', then value is already unique, so skip
                if d == 'V':
                    states.append(state)
                    nodes.append([i, j + 1] if j + 1 < len(state['puzzle'][i]) else [i + 1, 0])
                    continue

                # Append white
                if d == 'W':
                    white_state = self.copy(state)
                    white_state['domain'][i][j] = 'W'
                    counter += 1

                    # Forward check for Rule 1
                    new_domain_white = self.fc_white(white_state, i, j)
                    if not new_domain_white:
                        continue

                    states.append(white_state)
                    nodes.append([i, j + 1] if j + 1 < len(state['puzzle'][i]) else [i + 1, 0])

                # Append black
                if d == 'B' and self.black_allowed(state, i, j):
                    black_state = self.copy(state)
                    black_state['puzzle'][i][j] = 'B'
                    black_state['domain'][i][j] = 'B'
                    counter += 1

                    if not self.test_white_connected(black_state['domain'], black_state['edges']):
                        continue

                    # Forward check for Rule 2
                    black_state = self.fc_black(black_state, i, j)
                    if not black_state:
                        continue

                    states.append(black_state)
                    nodes.append([i, j + 1] if j + 1 < len(state['puzzle'][i]) else [i + 1, 0])
        return {'counter': counter}

    def load_puzzle(self, puzzle):
        for row in puzzle:
            if len(row) != len(puzzle[0]):
                raise InvalidInputError('Usage: Puzzle should be size N x M')

        domain = [['BW' for cell in row] for row in puzzle]
        edges = []
        for i in range(len(puzzle)):
            edges_row = []
            for j in range(len(puzzle[i])):
                self.check_values(puzzle[i][j])
                edges_cell = []
                u, d, l, r = i - 1, i + 1, j - 1, j + 1
                if u >= 0:
                    edges_cell.append([u, j])
                if d < len(puzzle):
                    edges_cell.append([d, j])
                if l >= 0:
                    edges_cell.append([i, l])
                if r < len(puzzle[i]):
                    edges_cell.append([i, r])
                edges_row.append(edges_cell)
            edges.append(edges_row)
        state = {
            'puzzle': puzzle,
            'domain': self.unique_white_cells(puzzle, domain),
            'edges': edges
        }
        return state

    def check_values(self, value):
        if not isinstance(value, int):
            raise TypeError("Value should be an integer")
        if value < 1:
            raise ValueError("Value should be positive")

    def copy(self, state):
        puzzle = [row[:] for row in state['puzzle']]
        domain = [row[:] for row in state['domain']]
        new_state = {
            'puzzle': puzzle,
            'domain': self.unique_white_cells(puzzle, domain),
            'edges': state['edges']
        }
        return new_state

    def check_solution(self, state):
        """General test - No solution if there are still unset cells"""
        return self.domain_complete(state['domain']) and self.test_duplicate_number(state['puzzle'])

    def domain_complete(self, domain):
        for i in domain:
            for j in i:
                if len(j) != 1:
                    return False
        return True

    # Rule 1 - No duplicate numbers in rows and columns for white cells
    def test_duplicate_number(self, puzzle):
        transpose = list(zip(*puzzle))  # Invert to get columns
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if puzzle[i][j] != 'B':
                    if self.has_duplicates(puzzle[i], transpose[j], puzzle[i][j]):
                        return False
        return True

    # Check if a number is a duplicate within its row or column
    def has_duplicates(self, row, col, value):
        if row.count(value) > 1 or col.count(value) > 1:
            return True
        return False

    # Marks numbers that are unique (they occur once in their row or column)
    # a number is uncertain, V must be white
    def unique_white_cells(self, puzzle, domain):
        transpose = list(zip(*puzzle))
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if (not self.has_duplicates(puzzle[i], transpose[j], puzzle[i][j])
                        and puzzle[i][j] != 'B'):
                    domain[i][j] = 'V'
        return domain

    # Rule 2 - No black cells are touching, diagonal is allowed, label black as 'B'
    # Check if cell is allowed to be black, regardless of whether it is black or white
    def black_allowed(self, state, i, j):
        for i2, j2 in state['edges'][i][j]:
            if state['puzzle'][i2][j2] == 'B':
                return False
        return True

    # Rule 3 - All white cells form one touching group
    def test_white_connected(self, grid, edges):
        visited = [[False for cell in row] for row in grid]
        node = self.first_white(grid)
        if self.total_white_cells(grid) == self.touch(node, visited, grid, edges, 1):
            return True
        return False

    # Count all white cells irrespective of touching
    def total_white_cells(self, grid):
        count = 0
        for i in grid:
            for j in i:
                if j != 'B':
                    count = count + 1
        return count

    # Recursive touch method to check if all white cells are connected, sets checked locations
    # to 'C' and counts them during backtracking
    def touch(self, node, visited, grid, edges, count):
        if node is None:
            return 0  # No white cells, so don't search
        else:
            i, j = node
            visited[i][j] = True
            for i2, j2 in edges[i][j]:
                if grid[i2][j2] != 'B' and not visited[i2][j2]:
                    count = self.touch([i2, j2], visited, grid, edges, count) + 1
            return count

    # Location of first white cell to count from
    def first_white(self, grid):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] != 'B':
                    return [i, j]
        return None

    # Forward checking - If a cell is turned black adjust the domains of adjacent cells
    # by removing 'B' from the domain
    def fc_black(self, state, i, j):
        for i2, j2 in state['edges'][i][j]:
            state['domain'][i2][j2] = state['domain'][i2][j2].replace('B', '')
            if state['domain'][i2][j2] == '':
                return None
        return state

    # Forward checking - If a cell is turned white adjust the domains of all the cells with
    # a duplicate value in the row and colum by removing 'W'
    def fc_white(self, state, i, j):
        size = len(state['puzzle'])
        k = 1
        while i - k >= 0:
            if state['puzzle'][i - k][j] == state['puzzle'][i][j]:
                state['domain'][i - k][j] = state['domain'][i - k][j].replace('W', '')
                if state['domain'][i - k][j] == '':
                    return None
            k += 1
        k = 1
        while i + k < size:
            if state['puzzle'][i + k][j] == state['puzzle'][i][j]:
                state['domain'][i + k][j] = state['domain'][i + k][j].replace('W', '')
                if state['domain'][i + k][j] == '':
                    return None
            k += 1
        k = 1
        while j - k >= 0:
            if state['puzzle'][i][j - k] == state['puzzle'][i][j]:
                state['domain'][i][j - k] = state['domain'][i][j - k].replace('W', '')
                if state['domain'][i][j - k] == '':
                    return None
            k += 1
        k = 1
        while j + k < size:
            if state['puzzle'][i][j + k] == state['puzzle'][i][j]:
                state['domain'][i][j + k] = state['domain'][i][j + k].replace('W', '')
                if state['domain'][i][j + k] == '':
                    return None
            k += 1
        return state

    def cell_surrounded(self, state, i, j):
        count = 0
        for i2, j2 in state['edges'][i][j]:
            if state['domain'][i2][j2] == 'B':
                count += 1

        if count == len(state['edges'][i][j]) - 1:
            for i2, j2 in state['edges'][i][j]:
                if state['domain'][i2][j2] != 'B':
                    state['domain'][i2][j2] = state['domain'][i2][j2].replace('B', '')
                    state['domain'][i][j] = state['domain'][i][j].replace('B', '')
                    if state['domain'][i2][j2] == '' or state['domain'][i][j] == '':
                        return None
        return state
