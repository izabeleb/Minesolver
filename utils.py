"""Provides minesweeper utility functions."""
from typing import List
from minefield import MineField
from cell import Cell


def get_open_cells(field: MineField, cell: Cell) -> List[Cell]:
    """Get a list of open connected field cell coordinates.

    Args:
        field (MineField): the MineField to search for open and connected cells.
        cell (Cell): The starting cell from which to find open cells.

    Returns:
        (list): a list of all open and connected cells.
    """
    # TODO re-implement iteratively to safe stack space (especially for large boards)
    if cell.is_flag or cell.is_mine or not field.cell_is_safe(cell):
        return [cell]
    
    if cell.visited:
        return

    open_cells: list = list()
    cell.visited = True
    open_cells.append(cell)

    for cell in field.surrounding_cells(cell):
        open_cells.append(cell)
        if cell.is_flag or cell.visited or not field.cell_is_safe(cell):
            continue


        open_cells += get_open_cells(field, cell)

    return open_cells
