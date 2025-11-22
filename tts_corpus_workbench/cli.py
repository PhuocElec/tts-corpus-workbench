import argparse
from .compute_audio_hours import compute_audio_hours


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


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
