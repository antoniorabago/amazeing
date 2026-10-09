from enum import Enum
from pydantic import (
    BaseModel, Field, model_validator, field_validator, ConfigDict
)


class ConfigKey(str, Enum):
    WIDTH = "width"
    HEIGHT = "height"
    ENTRY = "entry"
    EXIT = "exit"
    OUTPUT_FILE = "output_file"
    PERFECT = "perfect"
    SEED = "seed"
    ALGORITHM = "algorithm"


class Algorithms(str, Enum):
    DNF = "dnf"
    PRIM = "prim"


class Config(BaseModel):
    model_config = ConfigDict(frozen=True)

    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None
    algorithm: Algorithms | None = None

    @field_validator("output_file")
    @classmethod
    def validate_output_file(cls, file_name: str) -> str:
        if not file_name:
            raise ValueError("Output file is missing")
        if not file_name.endswith(".txt"):
            raise ValueError("Output file must have a .txt extension")
        if file_name == ".txt":
            raise ValueError("Output file name is missing")
        return file_name

    @model_validator(mode="after")
    def config_rules(self) -> "Config":
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit

        if not ((0 <= entry_x < self.width) and (0 <= entry_y < self.height)):
            raise ValueError("Entry is outside the maze")
        if not ((0 <= exit_x < self.width) and (0 <= exit_y < self.height)):
            raise ValueError("Exit is outside the maze")
        if self.entry == self.exit:
            raise ValueError("Entry and exit cannot be the same")
        return self


def parse_tuple(value: str, field: ConfigKey) -> tuple[int, int]:
    try:
        x, y = value.split(",", 1)
        return int(x), int(y)
    except ValueError:
        raise ValueError(
            f"Error in '{field.value.upper()}': invalid tuple value"
        )


def parse_int(value: str, field: ConfigKey) -> int:
    try:
        return int(value)
    except ValueError:
        raise ValueError(
            f"Error in '{field.value.upper()}': invalid integer value"
        )


def parse_bool(value: str, field: ConfigKey) -> bool:
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    else:
        raise ValueError(
            f"Error in '{field.value.upper()}': invalid boolean value"
        )


def parse_algorithm(value: str, field: ConfigKey) -> Algorithms:
    try:
        return Algorithms(value.lower())
    except ValueError:
        raise ValueError(
            f"Error in '{field.value.upper()}': "
            "invalid algorithm"
        )


def config_load() -> Config:
    with open("config.txt") as file:
        content = file.read()

    dict_config: dict[ConfigKey, str] = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(
                f"Invalid line: '{line}'. Expected 'KEY=VALUE'"
            )
        key, value = line.strip().split("=", 1)
        config_key = ConfigKey(key.lower().strip())
        config_value = value.lower().strip()
        dict_config[config_key] = config_value

    required_keys = set(ConfigKey) - {ConfigKey.SEED, ConfigKey.ALGORITHM}
    missing_keys = required_keys - dict_config.keys()
    if missing_keys:
        for key in missing_keys:
            print(f"Error in '{key.value.upper()}': field is missing")
        raise ValueError("Missing required configuration fields")

    if ConfigKey.SEED in dict_config:
        seed = parse_int(dict_config[ConfigKey.SEED], ConfigKey.SEED)
    else:
        seed = None
    if ConfigKey.ALGORITHM in dict_config:
        algorithm = parse_algorithm(
            dict_config[ConfigKey.ALGORITHM],
            ConfigKey.ALGORITHM
        )
    else:
        algorithm = None

    config_file = Config(
        width=parse_int(dict_config[ConfigKey.WIDTH], ConfigKey.WIDTH),
        height=parse_int(dict_config[ConfigKey.HEIGHT], ConfigKey.HEIGHT),
        entry=parse_tuple(dict_config[ConfigKey.ENTRY], ConfigKey.ENTRY),
        exit=parse_tuple(dict_config[ConfigKey.EXIT], ConfigKey.EXIT),
        output_file=dict_config[ConfigKey.OUTPUT_FILE],
        perfect=parse_bool(
            dict_config[ConfigKey.PERFECT],
            ConfigKey.PERFECT
        ),
        seed=seed,
        algorithm=algorithm
    )
    return config_file
