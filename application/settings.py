import pathlib
from typing import Final

# Root path
ROOT_PATH: Final[pathlib.Path] = pathlib.Path(__file__).parents[1]
# Path to DB
db_path: Final[pathlib.Path] = ROOT_PATH.joinpath("db", "db.sqlite")
