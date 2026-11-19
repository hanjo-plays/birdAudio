"""Download bird recordings from the Xeno-Canto API.

Resumable: species folders that already hold recordings are topped up to
their target instead of starting over.

Usage:
    uv run python -m birdaudio.data_collection.download          # download
    uv run python -m birdaudio.data_collection.download --check  # only show availability
"""

import argparse
import time

import requests

from birdaudio.config import RAW_DIR, SPECIES, XC_API_URL, get_api_key


def count_available(xc_name, api_key):
    """Number of recordings Xeno-Canto has for a species."""
    params = {"query": f'en:"{xc_name}"', "key": api_key}
    response = requests.get(XC_API_URL, params=params, timeout=30).json()
    return int(response.get("numRecordings", 0))


def download_species(xc_name, output_dir, target, api_key):
    output_dir.mkdir(parents=True, exist_ok=True)
    existing_ids = {f.stem for f in output_dir.glob("*.mp3")}
    existing = len(existing_ids)
    needed = target - existing

    if needed <= 0:
        print(f"{xc_name}: already has {existing}, skipping")
        return

    print(f"{xc_name}: has {existing}, downloading {needed} more")

    downloaded = 0
    page = 1

    while downloaded < needed:
        params = {"query": f'en:"{xc_name}"', "key": api_key, "page": page}
        response = requests.get(XC_API_URL, params=params, timeout=30).json()

        if not response.get("recordings"):
            print(f"  No more recordings on page {page}")
            break

        for rec in response["recordings"]:
            if downloaded >= needed:
                break
            if rec["id"] in existing_ids:
                continue

            try:
                audio_data = requests.get(rec["file"], timeout=30)
                (output_dir / f"{rec['id']}.mp3").write_bytes(audio_data.content)
                existing_ids.add(rec["id"])
                downloaded += 1
                print(f"  {xc_name}: {existing + downloaded}/{target}")
            except Exception as e:
                print(f"  Failed {rec['id']}: {e}")

        # Stop if we've gone through all pages
        if page >= int(response.get("numPages", 1)):
            break

        page += 1
        time.sleep(0.5)  # be polite to the API


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="only print how many recordings are available per species")
    args = parser.parse_args()
    api_key = get_api_key()

    if args.check:
        print(f"{'Folder Name':<30} {'XC Name':<30} {'Available':>10}")
        print("-" * 72)
        total = 0
        for folder_name, xc_name, _ in SPECIES:
            count = count_available(xc_name, api_key)
            total += count
            print(f"{folder_name:<30} {xc_name:<30} {count:>10}")
        print("-" * 72)
        print(f"{'TOTAL':<61} {total:>10}")
        return

    for folder_name, xc_name, target in SPECIES:
        print(f"\n--- {xc_name} ---")
        download_species(xc_name, RAW_DIR / folder_name, target, api_key)


if __name__ == "__main__":
    main()
