from pydantic import ValidationError
from config_loader import config_load


def main() -> None:
    try:
        config = config_load()
        print(config)

    except ValidationError as e:
        for error in e.errors():
            field = str(error["loc"][0])
            message = error["msg"].replace("Value error, ", "")
            print(f"Error in '{field.upper()}': {message}")
        return
    except ValueError as e:
        print(e)
        return


if __name__ == "__main__":
    main()
