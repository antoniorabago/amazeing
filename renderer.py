from generator import MazeGenerator
from enum import Enum


class Ansi(str, Enum):
    ESC = '\033'
    CLEAR = ESC + '[2J'
    RED = ESC + '[31m'
    YELLOW = ESC + '[33m'
    GREEN = ESC + '[32m'
    BLUE = ESC + '[34m'
    PURPLE = ESC + '[35m'
    WHITE_FG = ESC + '[37m'
    RED_BG = ESC + '[41m'
    YELLOW_BG = ESC + '[43m'
    GREEN_BG = ESC + '[42m'
    BLUE_BG = ESC + '[44m'
    PURPLE_BG = ESC + '[45m'
    RESET = ESC + '[0m'


class Unicode(str, Enum):
    HORIZONTAL = "─"
    VERTICAL = "│"
    TOP_LEFT = "┌"
    TOP = "┬"
    TOP_RIGHT = "┐"
    LEFT = "├"
    CROSS = "┼"
    RIGHT = "┤"
    BOTTOM_LEFT = "└"
    BOTTOM = "┴"
    BOTTOM_RIGHT = "┘"


class Walls(int, Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class NeighborPos(str, Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"


class Renderer:
    def __init__(self, maze: MazeGenerator) -> None:
        self.grid = maze.grid
        self.grid_width = maze.width
        self.grid_height = maze.height

    def _get_real_walls(self,
                        cell: int,
                        row_index: int,
                        col_index: int
                        ) -> int:
        if row_index == 0:
            cell |= Walls.NORTH
        if row_index == self.grid_height - 1:
            cell |= Walls.SOUTH
        if col_index == 0:
            cell |= Walls.WEST
        if col_index == self.grid_width - 1:
            cell |= Walls.EAST
        return cell

    # def _get_neighbors(
    #     self,
    #     row_index: int,
    #     col_index: int
    # ) -> dict[NeighborPos, int | None]:
    #     neighbors = {}
    #     # NORTH
    #     if row_index == 0:
    #         neighbors[NeighborPos.NORTH] = None
    #     else:
    #         neighbor_row = row_index - 1
    #         neighbor_col = col_index
    #         neighbors[NeighborPos.NORTH] = self._get_real_walls(
    #             self.grid[neighbor_row][neighbor_col],
    #             neighbor_row,
    #             neighbor_col
    #         )
    #     # WEST
    #     if col_index == 0:
    #         neighbors[NeighborPos.WEST] = None
    #     else:
    #         neighbor_row = row_index
    #         neighbor_col = col_index - 1
    #         neighbors[NeighborPos.WEST] = self._get_real_walls(
    #             self.grid[neighbor_row][neighbor_col],
    #             neighbor_row,
    #             neighbor_col
    #         )
    #     # SOUTH
    #     if row_index == self.grid_height - 1:
    #         neighbors[NeighborPos.SOUTH] = None
    #     else:
    #         neighbor_row = row_index + 1
    #         neighbor_col = col_index
    #         neighbors[NeighborPos.SOUTH] = self._get_real_walls(
    #             self.grid[neighbor_row][neighbor_col],
    #             neighbor_row,
    #             neighbor_col
    #         )
    #     # EAST
    #     if col_index == self.grid_width - 1:
    #         neighbors[NeighborPos.EAST] = None
    #     else:
    #         neighbor_row = row_index
    #         neighbor_col = col_index + 1
    #         neighbors[NeighborPos.EAST] = self._get_real_walls(
    #             self.grid[neighbor_row][neighbor_col],
    #             neighbor_row,
    #             neighbor_col
    #         )
    #     return neighbors

    def _create_drawing(self) -> list[list[str]]:
        drawing: list[list[str]] = []
        for _ in range(self.grid_height * 2 + 1):
            row = []
            for _ in range(self.grid_width * 6 + 1):
                row.append(" ")
            drawing.append(row)
        return drawing

    def _get_drawing(self,
                     cell: int
                     ) -> dict[NeighborPos, bool]:
        drawing = {
            NeighborPos.NORTH: bool(cell & Walls.NORTH),
            NeighborPos.EAST: bool(cell & Walls.EAST),
            NeighborPos.SOUTH: bool(cell & Walls.SOUTH),
            NeighborPos.WEST: bool(cell & Walls.WEST),
        }
        return drawing

    def _render_cell(self,
                     row_index: int,
                     col_index: int,
                     drawing: dict[NeighborPos, bool],
                     draw_grid: list[list[str]]
                     ) -> None:
        top = row_index * 2
        left = col_index * 6
        draw_grid[top][left] = "*"
        draw_grid[top][left + 6] = "*"
        draw_grid[top + 2][left] = "*"
        draw_grid[top + 2][left + 6] = "*"

        if drawing[NeighborPos.NORTH]:
            for position in range(1, 6):
                draw_grid[top][left + position] = Unicode.HORIZONTAL.value
        if drawing[NeighborPos.SOUTH]:
            for position in range(1, 6):
                draw_grid[top + 2][left + position] = Unicode.HORIZONTAL.value
        if drawing[NeighborPos.EAST]:
            draw_grid[top + 1][left + 6] = Unicode.VERTICAL.value
        if drawing[NeighborPos.WEST]:
            draw_grid[top + 1][left] = Unicode.VERTICAL.value

    def draw(self) -> None:
        # Borrar pantalla
        print(Ansi.CLEAR.value, end="")

        # Crear laberinto
        draw_grid = self._create_drawing()

        for row_index, row in enumerate(self.grid):
            for col_index, col in enumerate(row):
                cell = self._get_real_walls(col, row_index, col_index)
                # neighbors = self._get_neighbors(row_index, col_index)
                # print(f"Cell [{row_index}, {col_index}] = {cell}")
                # print(neighbors)
                drawing = self._get_drawing(cell)
                # print(drawing)
                self._render_cell(row_index, col_index, drawing, draw_grid)
                print()
            print()

        # Imprimir laberinto
        for row in draw_grid:
            print("".join(row))
            print()
