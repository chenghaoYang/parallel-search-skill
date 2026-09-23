#!/usr/bin/env python3
"""Rebuild the report.md inputs of the external arms (not redistributed in this repo).

usage: fetch_external.py

justin-handbook-layer0  docs/llm-api-protocols.md of justinatusa/llm-api-protocols @ d1d3f5d
justin-handbook-full    all 13 markdown files concatenated in the README reading order
"""

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = "https://github.com/justinatusa/llm-api-protocols.git"
COMMIT = "d1d3f5d"
ORDER = [
    "README.md", "docs/llm-api-protocols.md", "docs/taxonomy.md", "docs/field-atlas.md",
    "docs/details/tool-calls.md", "docs/details/native-formats.md", "docs/details/vendors.md",
    "docs/details/streaming.md", "docs/details/caching.md", "docs/details/hosted-claude.md",
    "docs/details/ops.md", "docs/details/conflicts.md", "docs/details/sources.md",
]


def main():
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["git", "clone", "--quiet", REPO, tmp], check=True)
        subprocess.run(["git", "-C", tmp, "checkout", "--quiet", COMMIT], check=True)
        src = Path(tmp)
        layer0 = (src / "docs/llm-api-protocols.md").read_text(encoding="utf-8")
        full = "".join(f"\n\n<!-- file: {name} -->\n\n" + (src / name).read_text(encoding="utf-8")
                       for name in ORDER)
    for arm, text in (("justin-handbook-layer0", layer0), ("justin-handbook-full", full)):
        out = ROOT / "runs" / arm / "report.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"{out.relative_to(ROOT)}: {len(text)} chars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
