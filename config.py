from pydantic import BaseModel, Field, ValidationError
from enum import StrEnum


class Config(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None
    algorithm: str | None = None

    # @model_validator(mode="after")
    # def config_rules(self) -> None:
    #     pass


def main() -> None:
    print("Comenzamos a leer el fichero config.txt")
    with open("config.txt") as file:
        content = file.read()
    dict_config = {}
    for line in content.splitlines():
        key, value = line.strip().split("=", 1)
        dict_config[key.lower().strip()] = value.lower().strip()
    print(dict_config)

    try:
        x_entry, y_entry = dict_config["entry"].split(",", 1)
        x_exit, y_exit = dict_config["exit"].split(",", 1)
        config_file = Config(
            width=int(dict_config["width"]),
            height=int(dict_config["height"]),
            entry=(int(x_entry), int(y_entry)),
            exit=(int(x_exit), int(y_exit)),
            output_file=str(dict_config["output_file"]),
            perfect=bool(dict_config["perfect"])
        )
        print(config_file)
    except ValidationError as e:
        for error in e.errors():
            field = error["loc"][0]
            message = error["msg"]
            print(f"Error en '{field}': {message}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
