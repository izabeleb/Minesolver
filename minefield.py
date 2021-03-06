"""Defines the Minefield class gor generating game board."""
from __future__ import annotations
import json
from random import randint
import struct
from typing import Generator
from typing import Tuple
from cell import Cell


class BadField(Exception):
    """Raised when a field is corrupted or malformed."""


class OutOfFieldCell(Exception):
    """Raised when a cell location is outside the range of the field."""


class MineField:
    """Wrapper class for the minesweeper board.

    If mine field is specified the values of row and col are ignored,
    and the size of the mine field is determined based off of the field.

    Args:
        row (int): the width of the board.
        col (int): the height of the board.
        mine_field (list): a predefined mine_field 2-D array for

    """
    def __init__(self, row: int = 10, col: int = 10, mine_field: list = None,
                 mine_count: int = None):
        self.mine_count = -1

        if mine_field is not None:
            self.mine_field = mine_field
            self.max_row = len(self.mine_field)
            self.max_col = len(self.mine_field[0])
        else:
            self.max_row = row
            self.max_col = col

            # TODO research more effective bomb distribution ratios
            if mine_count is None:
                self.mine_count = row * col // 4
            else:
                self.mine_count = mine_count

            self.flagged_count = 0
            self.mine_field = [
                [Cell(r, c) for c in range(self.max_col)]
                for r in range(self.max_row)
            ]
            self._generate_mines()

    def __repr__(self) -> str:
        repr_list: list = list()
        for i in range(self.max_row):
            repr_list.append(
                ' '.join([repr(cell) for cell in self.mine_field[i]])
            )
        return '\n'.join(repr_list)

    def __iter__(self):
        for row in self.mine_field:
            for cell in row:
                yield cell

    def _generate_mines(self):
        """Populate the mine field with mines"""
        bombs_in_grid = 0

        while bombs_in_grid < self.mine_count:
            rand_row = randint(0, self.max_row - 1)
            rand_col = randint(0, self.max_col - 1)

            if not self.mine_field[rand_row][rand_col].is_mine:
                self.mine_field[rand_row][rand_col].is_mine = True
                self._increment_neighbors(self.get_cell_at(rand_row, rand_col))
                bombs_in_grid += 1

    def _increment_neighbors(self, cell: Cell):
        """Increment the amount of mines areound the target cell by one.

        Args:
            cell (Cell): the target cell.
        """
        for cell in self.surrounding_cells(cell):
            cell.mine_count += 1

    def _decrement_neighbors(self, cell: Cell):
        """Decrement th amount of mines around the target cell by one.

        Args:
            cell (Cell): the target cell.
        """
        for cell in self.surrounding_cells(cell):
            cell.mine_count -= 1

    def encode(self, encoding: str = 'ascii') -> bytes:
        """Encode a minefield object.

        Args:
            encoding (str)): the format to use when encoding.

        Returns:
            (bytes): the encoded JSON representation of the MineField instance.
        """

        json_dict: dict = {'COLS': self.max_col,
                           'ROWS': self.max_row,
                           'CELLS': []}
        for cell in self:
            cell_dict = {'COL': cell.get_col(),
                         'ROW': cell.get_row(),
                         'MINE_COUNT': cell.get_mine_count(),
                         'IS_MINE': cell.is_mine(),
                         'IS_FLAG': cell.is_flag(),
                         'IS_VISITED': cell.is_visited(),
                         'IS_CLICKED': cell.is_clicked()}
            json_dict['CELLS'].append(cell_dict)
        json_str: str = json.dumps(json_dict)
        json_len: bytes = struct.pack('!I', len(json_str))

        return json_len + json_str.encode(encoding)

    def surrounding_cells(self, cell: Cell) -> Generator[Cell]:
        """Generator for cells surrounding the target cell.

        Args:
            cell (Cell): the cell to use as the center.

        Returns:
            (list): a list of all open and connected cells.
        """
        cell_row: int = cell.row
        cell_col: int = cell.col

        for i in range(-1, 2):
            if not -1 < cell_row + i < self.max_row:
                continue
            for j in range(-1, 2):
                if i == j == 0 or not -1 < cell_col + j < self.max_col:
                    continue
                yield self.get_cell_at(cell.row + i, cell.col + j)

    def cell_is_safe(self, cell: Cell) -> bool:
        """Determine if a cell should be considered safe.

        A cell is considered safe if it has an equal number of mines around it
        as flags placed by the player.

        Args:
            cell (Cell): the cell to test for safety.

        Returns:
            (bool): True is safe, False otherwise.
        """
        if cell.mine_count == 0:
            return True

        mines_found: int = 0

        for cell in self.surrounding_cells(cell):
                mines_found += 1

        return cell.mine_count == mines_found

    def field_is_safe(self) -> bool:
        """Check if every mine in the field has been flagged.

        Returns:
            (bool): Ture iss evey mine has been flagged, False otherwise.
        """
        for cell in self:
            if cell.is_mine() and not cell.is_flag():
                return False
        return True

    def get_cell_at(self, row: int, col: int) -> Cell:
        """Retrieve the cell at the given row and column.

        Args:
            row (int): The row of the cell.
            col (int): The column of the cell.

        Returns:
            (Cell): The cell at the target location.
        """
        return self.mine_field[row][col]

    def move_mine(self, cell: Cell) -> Tuple[int, int]:
        """Move a mine to another location in the mine field.

        Args:
            cell (Cell): the cell with the mine to be moved.

        Returns:
            (tuple): a tuple of the new mine coordinates.
        """
        rand_row: int = randint(0, self.max_row - 1)
        rand_col: int = randint(0, self.max_col - 1)

        while (self.mine_field[rand_row][rand_col].is_mine()):
            rand_row = randint(0, self.max_row - 1)
            rand_col = randint(0, self.max_col - 1)

        self.mine_field[rand_row][rand_col].set_mine(True)
        cell.is_mine = False

        return rand_row, rand_col

    @staticmethod
    def decode(field: bytes, encoding: str = 'ascii') -> MineField:
        """Decode the encoded JSON representation of a MineField instance.

        Args:
            field (bytes): the encoded representation of a mIneField object.
            encoding (str): the encoding format to decode by.

        Returns:
            (MineField): the decoded MIneField instance.
        """
        field: str = field.decode(encoding)
        field_json: dict = json.loads(field)

        max_cols: int = field_json['COLS']
        max_rows: int = field_json['ROWS']
        cell_list: list = field_json['CELLS']
        mine_field: list = [
            [None for j in range(max_cols)] for i in range(max_rows)
        ]

        for cell in cell_list:
            col = cell['COL']
            row = cell['ROW']
            mine_field[row][col] = Cell(row, col, cell['IS_MINE'],
                                        cell['IS_FLAG'], cell['MINE_COUNT'],
                                        cell['IS_VISITED'], cell['IS_CLICKED'])

        if len(mine_field) != max_rows:
            raise BadField

        for row in mine_field:
            if len(row) != max_cols:
                raise BadField

        return MineField(mine_field=mine_field)
