from generator import MazeGenerator
from enum import Enum


class Ansi(str, Enum):
    ESC = '\033'
    CLEAR = ESC + '[2J'
    HOME = ESC + '[H'
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
    def __init__(self,
                 maze: MazeGenerator,
                 path: list[tuple[int, int]]) -> None:
        self.grid = maze.grid
        self.grid_width = maze.width
        self.grid_height = maze.height
        self.entry = maze.entry
        self.exit = maze.exit
        self.path = path

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

    def _render_solution(
        self,
        path: set[tuple[int, int]],
        draw_grid: list[list[str]],
    ) -> None:
        for col, row in path:
            top = row * 2
            left = col * 6
            if (col, row) == self.entry:
                draw_grid[top + 1][left + 3] = "S"
            elif (col, row) == self.exit:
                draw_grid[top + 1][left + 3] = "F"
            else:
                draw_grid[top + 1][left + 3] = "●"

    def _print_grid(self, draw_grid: list[list[str]]) -> None:
        for row in draw_grid:
            print(Ansi.BLUE_BG.value, end="")
            print(Ansi.YELLOW.value, end="")
            print("".join(row), end="")
            print(Ansi.RESET.value)
        print()

    def draw(self) -> None:
        # Borrar pantalla
        # print(Ansi.CLEAR.value, end="")

        # Crear laberinto
        draw_grid = self._create_drawing()

        # Ruta de la solución (sin entrada y salida)
        self.path_cells = set(self.path)
        # self.path_cells = self.path_cells - {self.entry, self.exit}

        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                # neighbors = self._get_neighbors(row_index, col_index)
                # print(neighbors)
                drawing = self._get_drawing(cell)
                self._render_cell(row_index, col_index, drawing, draw_grid)

        # Imprimir laberinto
        # for row in draw_grid:
        #     print("".join(row), end="")
        #     print()

        self._render_solution(self.path_cells, draw_grid)
        self._print_grid(draw_grid)

        # self._render_solution(self.path_cells, draw_grid)
        # print(self.path_cells)

    # def draw_solution(self, path, draw_grid):
        #     self._render_solution(path, self.draw_grid)

        #     for row in self.draw_grid:
        #         print("".join(row))

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
