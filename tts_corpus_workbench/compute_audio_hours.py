from pathlib import Path
import soundfile as sf
from mutagen import File as MutagenFile


def get_duration_seconds(path: Path) -> float:
    suffix = path.suffix.lower()

    if suffix in {".wav", ".flac", ".ogg"}:
        try:
            info = sf.info(str(path))
            return float(info.frames) / float(info.samplerate)
        except Exception:
            pass

    try:
        m = MutagenFile(str(path))
        if m is not None and m.info is not None and hasattr(m.info, "length"):
            return float(m.info.length)
    except Exception:
        pass

    return 0.0


def find_audio_files(folder: Path, exts):
    files = []
    for ext in exts:
        files.extend(folder.rglob(f"*{ext}"))
    return files


def compute_audio_hours(folder: str, extensions: str):
    folder_path = Path(folder).resolve()
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    exts = [e.strip().lower() for e in extensions.split(",") if e.strip()]
    audio_files = find_audio_files(folder_path, exts)

    if not audio_files:
        return {
            "folder": str(folder_path),
            "total_files": 0,
            "total_seconds": 0.0,
            "hours": 0.0,
        }

    total_sec = sum(get_duration_seconds(f) for f in audio_files)

    return {
        "folder": str(folder_path),
            "total_files": len(audio_files),
        "total_seconds": total_sec,
        "hours": total_sec / 3600.0,
    }
