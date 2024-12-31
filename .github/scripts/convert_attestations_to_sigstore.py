# Convert PEP 740 attestations to Sigstore bundles
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pypi-attestations==0.0.20"
# ]
# [tool.uv]
# prerelease = "allow"  # necessary for sigstore dependencies
# ///

import argparse
import io
from collections.abc import Sequence
from pathlib import Path

from pypi_attestations import Attestation


def main(argv: Sequence[str]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("attestations", nargs="+", type=argparse.FileType("r"))
    args = parser.parse_args(argv)

    here = Path.cwd()

    attestation_file: io.TextIOWrapper[io.BufferedReader]
    for attestation_file in args.attestations:
        from_ = Path(str(attestation_file.name)).resolve()
        base = from_.with_name(from_.stem)  # strip .attestation
        to_ = base.with_suffix(".sigstore")  # replaces .publish suffix
        print(f"Converting {from_.relative_to(here)} to {to_.relative_to(here)}")
        with attestation_file as source:
            attestation = Attestation.model_validate_json(source.read())
        sigstore_bundle = attestation.to_bundle()
        with to_.open("w") as dest:
            dest.write(sigstore_bundle.to_json())


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
