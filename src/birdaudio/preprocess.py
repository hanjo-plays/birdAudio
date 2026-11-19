"""Convert raw mp3 recordings into 3-second mel spectrogram segments (.npy).

Resumable: segments that already exist are skipped.

Usage:
    uv run python -m birdaudio.preprocess
"""

import numpy as np

from birdaudio.audio_utils import audio_to_segments, segment_to_mel
from birdaudio.config import PROCESSED_DIR, RAW_DIR


def preprocess_species(species_folder):
    input_dir = RAW_DIR / species_folder
    output_dir = PROCESSED_DIR / species_folder
    output_dir.mkdir(parents=True, exist_ok=True)

    mp3_files = sorted(input_dir.glob("*.mp3"))
    total_segments = 0

    for i, mp3_file in enumerate(mp3_files):
        recording_id = mp3_file.stem
        segments = audio_to_segments(mp3_file)

        for j, segment in enumerate(segments):
            output_path = output_dir / f"{recording_id}_seg{j}.npy"
            if output_path.exists():
                total_segments += 1
                continue
            try:
                np.save(output_path, segment_to_mel(segment))
                total_segments += 1
            except PermissionError:
                print(f"  Permission denied: {output_path}, skipping")

        if (i + 1) % 50 == 0:
            print(f"  Processed {i + 1}/{len(mp3_files)} files, {total_segments} segments so far")

    return total_segments


def main():
    grand_total = 0
    for folder in sorted(p for p in RAW_DIR.iterdir() if p.is_dir()):
        print(f"Processing: {folder.name}")
        count = preprocess_species(folder.name)
        grand_total += count
        print(f"  → {count} segments saved\n")

    print(f"Done! Total segments: {grand_total}")


if __name__ == "__main__":
    main()
