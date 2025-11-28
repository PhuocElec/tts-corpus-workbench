# tts-corpus-workbench

CLI utilities for inspecting and cleaning a TTS corpus.

## Install
- Requires Python 3.9+.
- Install in editable mode (ensures entry point is available): `pip install -e .`
- The tools use `soundfile`, `mutagen`, and `pandas`. If `pandas` is missing, add it: `pip install pandas`.

## Usage
- Show help: `tts-corpus-workbench --help`
- All commands accept comma-separated audio extensions (default: `.wav,.mp3,.flac,.m4a`).

### Compute audio hours
- Count total duration in a folder:  
  `tts-corpus-workbench compute-audio-hours --folder data/audio --extensions ".wav,.flac"`

### Find orphan audio
- Compare metadata CSV with an audio folder:  
  `tts-corpus-workbench find-orphan-audio --metadata metadata.csv --audio-col file --folder data/audio`
- Prints counts for matches/missing/orphans; add `--delete-orphan` to remove files on disk that are not in metadata.

### Detect acronyms
- Export acronym frequency stats from a text column:  
  `tts-corpus-workbench detect-acronyms --metadata metadata.csv --text-col text --output acronym_stats.csv`
