"""Delete corrupted (near-empty) downloads from the raw data folder.

Usage:
    uv run python -m birdaudio.data_collection.clean_corrupted
"""

from birdaudio.config import RAW_DIR

MIN_FILE_SIZE = 1000  # bytes; anything smaller is a failed download


def main():
    removed = 0
    for filepath in RAW_DIR.glob("*/*.mp3"):
        if filepath.stat().st_size < MIN_FILE_SIZE:
            filepath.unlink()
            removed += 1
            print(f"Deleted: {filepath}")

    print(f"\nRemoved {removed} corrupted files")


if __name__ == "__main__":
    main()
