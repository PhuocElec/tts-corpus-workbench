import argparse

from .compute_audio_hours import compute_audio_hours
from .find_orphan_audio import find_orphan_audio, delete_orphan_files


def build_parser():
    parser = argparse.ArgumentParser(
        prog="tts-corpus-workbench",
        description="CLI tool for TTS corpus utilities",
    )

    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        required=True,
    )

    p_hours = subparsers.add_parser(
        "compute-audio-hours",
        help="Compute total audio duration in a folder",
    )
    p_hours.add_argument("--folder", required=True)
    p_hours.add_argument(
        "--extensions",
        default=".wav,.mp3,.flac,.m4a",
    )
    p_hours.set_defaults(func=cmd_compute_audio_hours)

    p_orphan = subparsers.add_parser(
        "find-orphan-audio",
        help="Compare metadata CSV with audio folder and find orphan/missing files",
    )
    p_orphan.add_argument(
        "--metadata",
        required=True,
        help="CSV file containing audio metadata",
    )
    p_orphan.add_argument(
        "--audio-col",
        default="file",
        help="Column name in CSV that stores audio file name/path (default: file)",
    )
    p_orphan.add_argument(
        "--folder",
        required=True,
        help="Folder containing audio files",
    )
    p_orphan.add_argument(
        "--extensions",
        default=".wav,.mp3,.flac,.m4a",
        help="Audio extensions, comma separated",
    )
    p_orphan.add_argument(
        "--delete-orphan",
        action="store_true",
        help="Delete orphan files (present on disk but not in metadata)",
    )
    p_orphan.set_defaults(func=cmd_find_orphan_audio)

    return parser


def cmd_compute_audio_hours(args):
    result = compute_audio_hours(args.folder, args.extensions)

    print("===========================================")
    print("Audio Hours Summary")
    print("===========================================")
    print(f"Folder         : {result['folder']}")
    print(f"Total files    : {result['total_files']}")
    print(f"Total seconds  : {result['total_seconds']:.2f}")
    print(f"Total minutes  : {result['total_seconds'] / 60:.2f}")
    print(f"Total hours    : {result['hours']:.4f}")
    print("===========================================")


def cmd_find_orphan_audio(args):
    result = find_orphan_audio(
        metadata_csv=args.metadata,
        audio_col=args.audio_col,
        folder=args.folder,
        extensions=args.extensions,
    )

    folder = result["folder"]
    total_meta = result["total_metadata"]
    total_disk = result["total_on_disk"]
    ok = len(result["ok"])
    missing = len(result["missing"])
    orphan = len(result["orphan"])

    print("===========================================")
    print("Find Orphan Audio")
    print("===========================================")
    print(f"Folder              : {folder}")
    print(f"Metadata entries    : {total_meta}")
    print(f"Files on disk       : {total_disk}")
    print(f"OK (exists both)    : {ok}")
    print(f"Missing (in meta)   : {missing}")
    print(f"Orphan (on disk)    : {orphan}")
    print("===========================================")

    if missing:
        print("Examples of missing (first 5):")
        for p in result["missing"][:5]:
            print("  MISSING:", p)

    if orphan:
        print("Examples of orphan (first 5):")
        for p in result["orphan"][:5]:
            print("  ORPHAN :", p)

    if args.delete_orphan and orphan:
        deleted = delete_orphan_files(folder, result["orphan"])
        print(f"\nDeleted orphan files: {deleted}")


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
