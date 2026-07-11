"""
Download the Spotify Tracks Dataset from Kaggle and save it to data/raw/.
Skips the download if the CSV already exists locally.
"""

import os
import shutil
import kagglehub


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DATASET_SLUG = "maharshipandya/-spotify-tracks-dataset"

# Resolve paths relative to the project root (one level up from src/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
OUTPUT_FILE = os.path.join(RAW_DIR, "spotify_tracks.csv")


def download_dataset() -> str:
    """Download the dataset if the CSV does not already exist.

    Returns:
        The path to the local CSV file.
    """
    # --- Check if CSV already exists ---
    if os.path.exists(OUTPUT_FILE):
        print(f"[SKIP] CSV already exists at: {OUTPUT_FILE}")
        return OUTPUT_FILE

    print("[INFO] CSV not found. Downloading from Kaggle …")

    # kagglehub.dataset_download returns the path to the downloaded folder
    downloaded_path = kagglehub.dataset_download(DATASET_SLUG)
    print(f"[INFO] Dataset downloaded to: {downloaded_path}")

    # --- Locate the CSV inside the downloaded folder ---
    csv_file = None
    for root, _dirs, files in os.walk(downloaded_path):
        for f in files:
            if f.endswith(".csv"):
                csv_file = os.path.join(root, f)
                break
        if csv_file:
            break

    if csv_file is None:
        raise FileNotFoundError(
            f"No CSV file found in the downloaded dataset at {downloaded_path}"
        )

    # --- Ensure output directory exists & copy the file ---
    os.makedirs(RAW_DIR, exist_ok=True)
    shutil.copy2(csv_file, OUTPUT_FILE)
    print(f"[DONE] CSV saved to: {OUTPUT_FILE}")

    return OUTPUT_FILE


# ---------------------------------------------------------------------------
# Entry‑point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    path = download_dataset()
    print(f"\nDataset is ready at: {path}")
