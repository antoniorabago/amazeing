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
    RABBIT = "\U0001F430"
    CARROT = "\U0001F955"


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
    CELL_WIDTH = 4
    CELL_HEIGHT = 2

    def __init__(self,
                 maze: MazeGenerator,
                 path: list[tuple[int, int]]) -> None:
        self.grid = maze.grid
        self.grid_width = maze.width
        self.grid_height = maze.height
        self.entry = maze.entry
        self.exit = maze.exit
        self.blocked = maze.blocked
        self.path = path

    # Función que crea la cuadrícula del laberinto
    def _create_canvas(self) -> list[list[str]]:
        drawing: list[list[str]] = []
        for _ in range(self.grid_height * self.CELL_HEIGHT + 1):
            row = []
            for _ in range(self.grid_width * self.CELL_WIDTH + 1):
                row.append(" ")
            drawing.append(row)
        return drawing

    # Función que obtiene el valor de las celdas vecinas
    def _get_neighbors_cells(
        self,
        row_index: int,
        col_index: int
    ) -> dict[NeighborPos, int | None]:
        neighbors: dict[NeighborPos, int | None] = {}
        # NORTH
        if row_index == 0:
            neighbors[NeighborPos.NORTH] = None
        else:
            neighbor_row = row_index - 1
            neighbor_col = col_index
            neighbors[NeighborPos.NORTH] = (
                self.grid[neighbor_row][neighbor_col]
            )
        # WEST
        if col_index == 0:
            neighbors[NeighborPos.WEST] = None
        else:
            neighbor_row = row_index
            neighbor_col = col_index - 1
            neighbors[NeighborPos.WEST] = self.grid[neighbor_row][neighbor_col]
        # SOUTH
        if row_index == self.grid_height - 1:
            neighbors[NeighborPos.SOUTH] = None
        else:
            neighbor_row = row_index + 1
            neighbor_col = col_index
            neighbors[NeighborPos.SOUTH] = (
                self.grid[neighbor_row][neighbor_col]
            )
        # EAST
        if col_index == self.grid_width - 1:
            neighbors[NeighborPos.EAST] = None
        else:
            neighbor_row = row_index
            neighbor_col = col_index + 1
            neighbors[NeighborPos.EAST] = self.grid[neighbor_row][neighbor_col]

        return neighbors

    # Función que indica las paredes a dibujar de cada celda
    def _get_cell_walls(self,
                        cell: int
                        ) -> dict[NeighborPos, bool]:
        drawing = {
            NeighborPos.NORTH: bool(cell & Walls.NORTH),
            NeighborPos.EAST: bool(cell & Walls.EAST),
            NeighborPos.SOUTH: bool(cell & Walls.SOUTH),
            NeighborPos.WEST: bool(cell & Walls.WEST),
        }
        return drawing

    # Función que muestra cada celda
    def _draw_cell_walls(self,
                         row_index: int,
                         col_index: int,
                         drawing: dict[NeighborPos, bool],
                         draw_grid: list[list[str]]
                         ) -> None:
        top = row_index * self.CELL_HEIGHT
        left = col_index * self.CELL_WIDTH
        draw_grid[top][left] = "*"
        draw_grid[top][left + self.CELL_WIDTH] = "*"
        draw_grid[top + self.CELL_HEIGHT][left] = "*"
        draw_grid[top + self.CELL_HEIGHT][left + self.CELL_WIDTH] = "*"

        if drawing[NeighborPos.NORTH]:
            for position in range(1, self.CELL_WIDTH):
                draw_grid[top][left + position] = Unicode.HORIZONTAL.value
        if drawing[NeighborPos.SOUTH]:
            for position in range(1, self.CELL_WIDTH):
                draw_grid[top + self.CELL_HEIGHT][left + position] = (
                    Unicode.HORIZONTAL.value
                )
        if drawing[NeighborPos.EAST]:
            draw_grid[top + 1][left + self.CELL_WIDTH] = Unicode.VERTICAL.value
        if drawing[NeighborPos.WEST]:
            draw_grid[top + 1][left] = Unicode.VERTICAL.value

    # Función que muestra la ruta de la solución
    def _draw_solution_path(
        self,
        path: list[tuple[int, int]],
        draw_grid: list[list[str]],
    ) -> None:
        arrows = {
            "E": "→",
            "W": "←",
            "S": "↓",
            "N": "↑",
        }
        for index, (col, row) in enumerate(path):
            top = row * self.CELL_HEIGHT
            left = col * self.CELL_WIDTH
            center = top + 1, left + (self.CELL_WIDTH // 2)

            if (col, row) == self.entry:
                draw_grid[center[0]][center[1]] = Unicode.RABBIT
            elif (col, row) == self.exit:
                draw_grid[center[0]][center[1]] = Unicode.CARROT
            else:
                next_col, next_row = path[index + 1]
                if next_col > col:
                    direction = "E"
                elif next_col < col:
                    direction = "W"
                elif next_row > row:
                    direction = "S"
                else:
                    direction = "N"
                char = arrows[direction]
                draw_grid[center[0]][center[1]] = char

    # Función que cambia de color el patrón 42
    def _draw_42_pattern(self, draw_grid: list[list[str]]) -> None:
        for x, y in self.blocked:
            top = y * self.CELL_HEIGHT
            left = x * self.CELL_WIDTH

            for position in range(1, self.CELL_WIDTH):
                draw_grid[top + 1][left + position] = (
                    Ansi.RED.value + "█" + Ansi.RESET.value
                )

    # Función que imprime la cuadrícula del laberinto
    def _print_canvas(self, draw_grid: list[list[str]]) -> None:
        for row in draw_grid:
            col_index = 0

            while col_index < len(row):
                col = row[col_index]
                color = Ansi.BLUE_BG.value + Ansi.WHITE_FG.value

                print(
                    f"{color}{col}{Ansi.RESET.value}",
                    end=""
                )

                if col in (Unicode.RABBIT, Unicode.CARROT):
                    col_index += 1

                col_index += 1

            print()

    def render(self) -> None:
        # Borrar pantalla
        print(Ansi.CLEAR.value, end="")

        # Crear laberinto
        draw_grid = self._create_canvas()

        # Dibujar celdas
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                neighbors = self._get_neighbors_cells(row_index, col_index)
                print(neighbors)
                drawing = self._get_cell_walls(cell)
                self._draw_cell_walls(row_index, col_index, drawing, draw_grid)

        # Dibujar Ruta de la solución
        self._draw_solution_path(self.path, draw_grid)

        # Dibujar el patrón 42
        self._draw_42_pattern(draw_grid)

        # Imprimir laberinto
        self._print_canvas(draw_grid)
