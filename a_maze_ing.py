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

        solution_path = maze.solve()
        print(solution_path)
        renderer = Renderer(maze, solution_path)
        renderer.draw()
        maze.write_output()

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
    except BaseException as e:
        print(e.__class__.__name__)


if __name__ == "__main__":
    main()
