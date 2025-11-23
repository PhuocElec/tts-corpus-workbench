import re
import pandas as pd


def detect_acronyms(metadata_csv: str, text_col: str = "text", output_csv: str | None = None):
    df = pd.read_csv(metadata_csv)

    if text_col not in df.columns:
        raise ValueError(f"Text column not found: {text_col}")

    pattern = re.compile(r"\b[A-Z][A-Z0-9]{1,}\b")

    counts: dict[str, int] = {}
    for text in df[text_col].astype(str):
        for ac in pattern.findall(text):
            counts[ac] = counts.get(ac, 0) + 1

    rows = [{"acronym": k, "count": v} for k, v in sorted(counts.items())]
    out_df = pd.DataFrame(rows)

    if output_csv:
        out_df.to_csv(output_csv, index=False)

    return {
        "input_csv": metadata_csv,
        "text_col": text_col,
        "output_csv": output_csv,
        "unique_acronyms": len(out_df),
    }
