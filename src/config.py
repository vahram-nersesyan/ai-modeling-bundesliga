import tomllib
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.toml"

with open(CONFIG_PATH, "rb") as f:
    _config = tomllib.load(f)

TEAMS = _config["teams"]["names"]
NUM_TEAMS = len(TEAMS)
NUM_MATCHDAYS = (NUM_TEAMS - 1) * 2
SEASON_SPLIT = NUM_MATCHDAYS // 2
