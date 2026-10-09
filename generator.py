
import random
from config_loader import Config
# from config_loader import config_load

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

ALL_WALLS = NORTH | EAST | SOUTH | WEST


class MazeGenerator:
    def __init__(
        self,
        config: Config,
    ) -> None:
        self.width = config.width
        self.height = config.height
        self.entry = config.entry
        self.exit = config.exit
        self.perfect = config.perfect
        self.random = random.Random(config.seed)
        self.blocked: set[tuple[int, int]] = set()
        self.output_file = config.output_file
        self.grid = [
            [ALL_WALLS for _ in range(config.width)]
            for _ in range(config.height)
        ]

    def _place_42_pattern(self) -> None:
        if self.width < 9 or self.height < 7:
            print("Maze too small to display the 42 pattern")
            return

        center_x = self.width // 2
        center_y = self.height // 2

        pattern = [
            (-3, -2),         (-1, -2),
            (-3, -1),         (-1, -1),
            (-3, 0), (-2, 0), (-1, 0),
                              (-1, 1),
                              (-1, 2),

            (1, -2), (2, -2), (3, -2),
                              (3, -1),
            (1, 0),  (2, 0),  (3, 0),
            (1, 1),
            (1, 2),  (2, 2),  (3, 2),
        ]

        for dx, dy in pattern:
            x = center_x + dx
            y = center_y + dy

            self.blocked.add((x, y))

    def is_inside(self, x: int, y: int) -> bool:
        return (
            0 <= x < self.width
            and 0 <= y < self.height
        )

    def _confirm_entry_exit(self) -> None:
        if not self.is_inside(*self.entry):
            raise ValueError(f"The entry {self.entry} is outside the maze")

        if not self.is_inside(*self.exit):
            raise ValueError(f"The exit {self.exit} is outside the maze")

        if self.entry in self.blocked:
            raise ValueError(f"The entry {self.entry} is not valid")

        if self.exit in self.blocked:
            raise ValueError(f"The exit {self.exit} is not valid")

    def remove_wall(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int
    ) -> None:
        if x2 == x1 + 1 and y2 == y1:
            self.grid[y1][x1] &= ~EAST
            self.grid[y2][x2] &= ~WEST
        elif x2 == x1 and y2 == y1 + 1:
            self.grid[y1][x1] &= ~SOUTH
            self.grid[y2][x2] &= ~NORTH
        elif x2 == x1 - 1 and y2 == y1:
            self.grid[y1][x1] &= ~WEST
            self.grid[y2][x2] &= ~EAST
        elif x2 == x1 and y2 == y1 - 1:
            self.grid[y1][x1] &= ~NORTH
            self.grid[y2][x2] &= ~SOUTH

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        neighbors = []
        nx = x
        ny = y - 1

        if self.is_inside(nx, ny):
            neighbors.append((nx, ny))

        nx = x + 1
        ny = y

        if self.is_inside(nx, ny):
            neighbors.append((nx, ny))

        nx = x
        ny = y + 1

        if self.is_inside(nx, ny):
            neighbors.append((nx, ny))

        nx = x - 1
        ny = y

        if self.is_inside(nx, ny):
            neighbors.append((nx, ny))

        return neighbors

    def _count_openings(self, x: int, y: int) -> int:
        openings = 0

        if not self.grid[y][x] & NORTH:
            openings += 1
        if not self.grid[y][x] & EAST:
            openings += 1
        if not self.grid[y][x] & SOUTH:
            openings += 1
        if not self.grid[y][x] & WEST:
            openings += 1

        return openings

    def _find_dead_ends(self) -> list[tuple[int, int]]:
        dead_ends = []

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.blocked:
                    continue

                if self._count_openings(x, y) == 1:
                    dead_ends.append((x, y))

        return dead_ends

    def _open_dead_end(self, x: int, y: int) -> None:
        candidates = []

        for nx, ny in self.get_neighbors(x, y):
            if (nx, ny) in self.blocked:
                continue

            if nx == x + 1 and self.grid[y][x] & EAST:
                candidates.append((nx, ny))
            elif nx == x - 1 and self.grid[y][x] & WEST:
                candidates.append((nx, ny))
            elif ny == y + 1 and self.grid[y][x] & SOUTH:
                candidates.append((nx, ny))
            elif ny == y - 1 and self.grid[y][x] & NORTH:
                candidates.append((nx, ny))

        if candidates:
            nx, ny = self.random.choice(candidates)
            self.remove_wall(x, y, nx, ny)

    def _make_playable(self) -> None:
        dead_ends = self._find_dead_ends()

        for x, y in dead_ends:
            if self._count_openings(x, y) == 1:
                self._open_dead_end(x, y)

    def generate(self) -> None:
        self._place_42_pattern()
        self._confirm_entry_exit()

        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []

        start = (0, 0)

        visited.add(start)
        stack.append(start)

        while stack:
            x, y = stack[-1]

            neighbors = self.get_neighbors(x, y)
            unvisited = []

            for nx, ny in neighbors:
                if (
                    (nx, ny) not in visited
                    and (nx, ny) not in self.blocked
                ):
                    unvisited.append((nx, ny))

            if unvisited:
                nx, ny = self.random.choice(unvisited)

                self.remove_wall(x, y, nx, ny)
                visited.add((nx, ny))
                stack.append((nx, ny))

            else:
                stack.pop()

        if not self.perfect:
            self._make_playable()

    def _get_accessible_neighbors(
        self, x: int, y: int
    ) -> list[tuple[int, int]]:
        neighbors = []

        if (
            self.is_inside(x, y - 1)
            and not (self.grid[y][x] & NORTH)
        ):
            neighbors.append((x, y - 1))

        if (
            self.is_inside(x + 1, y)
            and not (self.grid[y][x] & EAST)
        ):
            neighbors.append((x + 1, y))

        if (
            self.is_inside(x - 1, y)
            and not (self.grid[y][x] & WEST)
        ):
            neighbors.append((x - 1, y))

        if (
            self.is_inside(x, y + 1)
            and not (self.grid[y][x] & SOUTH)
        ):
            neighbors.append((x, y + 1))

        return neighbors

    def solve(self) -> list[tuple[int, int]]:
        queue = [self.entry]
        index = 0
        visited = {self.entry}
        parents: dict[tuple[int, int], tuple[int, int]] = {}

        while index < len(queue):
            x, y = queue[index]
            index += 1

            if (x, y) == self.exit:
                break

            for nx, ny in self._get_accessible_neighbors(x, y):
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parents[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

        if self.exit not in visited:
            raise ValueError("No path found between entry and exit")

        path = [self.exit]
        current = self.exit

        while current != self.entry:
            current = parents[current]
            path.append(current)

        path.reverse()
        return path

    def path_to_directions(self, path: list[tuple[int, int]]) -> str:
        directions = ""

        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]

            if x2 == x1 + 1:
                directions += "E"
            elif x2 == x1 - 1:
                directions += "W"
            elif y2 == y1 + 1:
                directions += "S"
            elif y2 == y1 - 1:
                directions += "N"

        return directions

    def write_output(self) -> None:
        path = self.solve()
        directions = self.path_to_directions(path)

        with open(self.output_file, "w") as file:
            for row in self.grid:
                file.write("".join(f"{cell:X}" for cell in row) + "\n")

            file.write("\n")
            file.write(f"{self.entry[0]},{self.entry[1]}\n")
            file.write(f"{self.exit[0]},{self.exit[1]}\n")
            file.write(directions + "\n")


# config = config_load()
# maze = MazeGenerator(config)


# print("ANTES:")
# for row in maze.grid:
#     for cell in row:
#         print(f"{cell:X}", end="")
#     print()

# maze.generate()

# print("Entrada:", maze.entry)
# print("Salida:", maze.exit)
# print("Bloqueadas:", maze.blocked)

# print("Despues:")
# for row in maze.grid:
#     for cell in row:
#         print(f"{cell:X}", end="")
#     print()

# maze.write_output()
# path = maze.solve

# print("\nDESPUÉS:")
# for row in maze.grid:
#     for cell in row:
#         print(f"{cell:X}", end="")
#     print()

# print("Entrada:", maze.entry)
# print("Salida:", maze.exit)
# print("Camino:", path)
# print("Número de movimientos:", len(path) - 1)


# print(maze.grid)
# print(maze.grid[2][2])
# maze.grid[2][2] &= ~EAST
# print(maze.grid[2][2])

# maze.remove_wall(0, 0, 1, 0)

# print(maze.grid)
