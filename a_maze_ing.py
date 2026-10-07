from pydantic import ValidationError
from config_loader import config_load
from generator import MazeGenerator
from renderer import Renderer


def main() -> None:
    try:
        config = config_load()
        maze = MazeGenerator(config)
        maze.generate()
        print("\nHEX:")

        for row in maze.grid:
            for cell in row:
                print(format(cell, "X"), end="")
            print()

        solved = maze.solve()
        print(solved)

        renderer = Renderer(maze, solved)
        renderer.draw()

    except ValidationError as e:
        for error in e.errors():
            loc = error["loc"]
            if loc:
                field = str(loc[0])
            else:
                field = "maze"
            message = error["msg"].replace("Value error, ", "")
            print(f"Error in '{field.upper()}': {message}")
        return

    except ValueError as e:
        print(e)
        return


if __name__ == "__main__":
    main()
