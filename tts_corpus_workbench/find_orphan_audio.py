from pathlib import Path

import pandas as pd


def load_metadata_paths(metadata_csv: str, audio_col: str):
    df = pd.read_csv(metadata_csv)
    if audio_col not in df.columns:
        raise ValueError(f"Column not found: {audio_col}")
    vals = df[audio_col].astype(str)
    vals = [v for v in vals if v and v.lower() != "nan"]
    norm = [Path(v).as_posix() for v in vals]
    return set(norm)


def scan_audio_files(folder: Path, exts):
    files = []
    for ext in exts:
        files.extend(folder.rglob(f"*{ext}"))
    rel = [f.relative_to(folder).as_posix() for f in files]
    return set(rel)


def find_orphan_audio(
    metadata_csv: str,
    audio_col: str,
    folder: str,
    extensions: str,
):
    folder_path = Path(folder).resolve()
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    exts = [e.strip().lower() for e in extensions.split(",") if e.strip()]

    meta_set = load_metadata_paths(metadata_csv, audio_col)
    disk_set = scan_audio_files(folder_path, exts)

    ok = meta_set & disk_set
    missing = meta_set - disk_set
    orphan = disk_set - meta_set

    return {
        "folder": str(folder_path),
        "total_metadata": len(meta_set),
        "total_on_disk": len(disk_set),
        "ok": sorted(ok),
        "missing": sorted(missing),
        "orphan": sorted(orphan),
    }


def delete_orphan_files(folder: str, orphan_rel_paths):
    base = Path(folder).resolve()
    deleted = 0
    for rel in orphan_rel_paths:
        p = base / rel
        if p.exists():
            try:
                p.unlink()
                deleted += 1
            except Exception:
                pass
    return deleted
