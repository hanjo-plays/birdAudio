"""Project-wide settings: data paths, API config and the species list."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# Where raw mp3s and processed spectrograms live. Set DATA_DIR in .env to keep
# the (large) dataset outside the repo, e.g. on an external drive.
DATA_DIR = Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data"))
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

XC_API_URL = "https://xeno-canto.org/api/3/recordings"


def get_api_key():
    """Return the Xeno-Canto API key. Only needed for downloading."""
    key = os.getenv("XC_API_KEY")
    if not key:
        raise RuntimeError(
            "XC_API_KEY is not set. Copy .env.example to .env and add your "
            "Xeno-Canto API key, or set the XC_API_KEY environment variable."
        )
    return key


# (folder name, Xeno-Canto English name, target number of recordings)
# Xeno-Canto names differ from common usage for a few species
# (e.g. "Blackcap", "Common Starling"), which is why both are kept.
SPECIES = [
    ("Eurasian_Blackbird",       "Common Blackbird",         500),
    ("Great_Tit",                "Great Tit",                500),
    ("Blue_Tit",                 "Blue Tit",                 500),
    ("European_Robin",           "European Robin",           500),
    ("Common_Chaffinch",         "Common Chaffinch",         500),
    ("Eurasian_Wren",            "Eurasian Wren",            500),
    ("Song_Thrush",              "Song Thrush",              500),
    ("Common_Blackcap",          "Blackcap",                 500),
    ("Eurasian_Magpie",          "Eurasian Magpie",          500),
    ("Hooded_Crow",              "Hooded Crow",              500),
    ("Common_Wood_Pigeon",       "Common Wood Pigeon",       350),
    ("European_Starling",        "Common Starling",          500),
    ("House_Sparrow",            "House Sparrow",            500),
    ("Eurasian_Jay",             "Eurasian Jay",             500),
    ("Common_Swift",             "Common Swift",             500),
    ("Eurasian_Nuthatch",        "Eurasian Nuthatch",        500),
    ("Great_Spotted_Woodpecker", "Great Spotted Woodpecker", 500),
    ("European_Goldfinch",       "European Goldfinch",       500),
    ("Eurasian_Treecreeper",     "Eurasian Treecreeper",     500),
    ("Common_Nightingale",       "Common Nightingale",       500),
    ("Common_Chiffchaff",        "Common Chiffchaff",        500),
    ("Long-tailed_Tit",          "Long-tailed Tit",          500),
    ("Marsh_Tit",                "Marsh Tit",                500),
    ("Common_Buzzard",           "Common Buzzard",           350),
    ("Black_Redstart",           "Black Redstart",           500),
    ("White_Wagtail",            "White Wagtail",            500),
    ("Common_Linnet",            "Common Linnet",            500),
    ("Eurasian_Siskin",          "Eurasian Siskin",          500),
    ("Stock_Dove",               "Stock Dove",               350),
]
