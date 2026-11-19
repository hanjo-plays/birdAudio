"""Show how many raw recordings and processed segments exist per species.

Usage:
    uv run python -m birdaudio.stats
"""

from birdaudio.config import PROCESSED_DIR, RAW_DIR, SPECIES


def count_files(folder, pattern):
    return len(list(folder.glob(pattern))) if folder.exists() else 0


def main():
    print(f"Data directory: {RAW_DIR.parent}\n")
    print(f"{'Species':<30} {'Recordings':>12} {'Target':>8} {'Segments':>10}")
    print("-" * 63)

    total_recordings = total_segments = 0
    for folder_name, _, target in SPECIES:
        recordings = count_files(RAW_DIR / folder_name, "*.mp3")
        segments = count_files(PROCESSED_DIR / folder_name, "*.npy")
        total_recordings += recordings
        total_segments += segments
        print(f"{folder_name:<30} {recordings:>12} {target:>8} {segments:>10}")

    print("-" * 63)
    print(f"{'TOTAL':<30} {total_recordings:>12} {'':>8} {total_segments:>10}")


if __name__ == "__main__":
    main()
