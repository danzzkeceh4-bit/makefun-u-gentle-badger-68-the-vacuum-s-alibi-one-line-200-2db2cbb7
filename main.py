#!/usr/bin/env python3
"""The Vacuum's Alibi: One Line, 200 Characters.

Deterministic program for the make.fun competition
u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7.

Writes exactly one alibi line (1-200 characters, UTF-8) to
/output/entry.txt. No network, no randomness, no arguments.
"""

import os
import sys

ALIBI_LINE = (
    "I did not miss that spot. I deliberately preserved it as a "
    "control sample for future cleaning research."
)

MIN_LENGTH = 1
MAX_LENGTH = 200


def output_path() -> str:
    """Resolve the output file path.

    Uses MAKEFUN_OUTPUT_DIR when set, otherwise /output.
    """
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(output_dir, "entry.txt")


def validate_alibi(line: str) -> str:
    """Validate the alibi line before it is written out.

    Rules (from the competition brief):
    - exactly one line, 1-200 characters, UTF-8 encodable
    - must not be empty or whitespace only

    Returns the stripped line on success, raises ValueError otherwise.
    """
    if not isinstance(line, str):
        raise ValueError("alibi line must be a string")
    stripped = line.strip()
    if not stripped:
        raise ValueError("alibi line is empty or only whitespace")
    if not (MIN_LENGTH <= len(stripped) <= MAX_LENGTH):
        raise ValueError(
            f"alibi line is {len(stripped)} characters, "
            f"must be {MIN_LENGTH}-{MAX_LENGTH}"
        )
    # Reject embedded newlines: the entry must be exactly one line.
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("alibi line must be a single line")
    # UTF-8 round-trip check.
    stripped.encode("utf-8")
    return stripped


def main() -> int:
    """Validate the alibi line and write it to the output file."""
    try:
        line = validate_alibi(ALIBI_LINE)
    except ValueError as exc:
        print(
            f"error: invalid alibi line ({exc}); "
            f"entry must be one line of {MIN_LENGTH}-{MAX_LENGTH} "
            "non-whitespace UTF-8 characters",
            file=sys.stderr,
        )
        return 1

    # Final guard: never write leading/trailing whitespace.
    if line != line.strip():
        print("error: alibi line has leading/trailing whitespace", file=sys.stderr)
        return 1
    path = output_path()
    output_dir = os.path.dirname(path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
