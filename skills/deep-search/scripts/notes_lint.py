#!/usr/bin/env python3
"""Optional diagnostics for legacy deep-search structured notes.

usage: notes_lint.py NOTES_DIR [--round N] [--max-chars N]

Per note: claims (official/secondary), claims missing src or quote, conflicts, gaps, leads.
Freeform notes are not assessed. A zero exit code means the diagnostics ran, not that
sources or research quality passed. The lead must inspect the evidence itself.
"""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

CLAIM = re.compile(r"^\s*-\s*\[C\d+\]")
SECTION = re.compile(r"^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def legacy_fields(line):
    """Read pipe-delimited metadata without treating quoted text as metadata."""
    fields = {}
    chunks, chunk = [], []
    closing = None
    escaped = False
    for char in line:
        if escaped:
            chunk.append(char)
            escaped = False
            continue
        if char == "\\" and closing:
            chunk.append(char)
            escaped = True
            continue
        if closing:
            if char == closing:
                closing = None
        elif char in ('"', '“', '「'):
            closing = {'"': '"', '“': '”', '「': '」'}[char]
        elif char == "|":
            chunks.append("".join(chunk))
            chunk = []
            continue
        chunk.append(char)
    chunks.append("".join(chunk))
    for part in chunks[1:]:
        match = re.fullmatch(r"\s*(src|quote|type):\s*(.*?)\s*", part, re.I)
        if match:
            fields[match.group(1).lower()] = match.group(2)
    return fields


def has_source(value):
    """Only validate URL shape; existence and claim support need manual review."""
    if not value or any(c.isspace() for c in value):
        return False
    try:
        url = urlsplit(value)
        return url.scheme in ("http", "https") and bool(url.hostname)
    except ValueError:
        return False


def has_quote(value):
    closers = {'"': '"', '“': '”', '「': '」'}
    return bool(value and value[0] in closers and len(value) > 2
                and value[-1] == closers[value[0]] and value[1:-1].strip())


def lint(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    row = {"file": path.name, "chars": len(text), "claims": 0, "official": 0, "secondary": 0,
           "no_src": [], "no_quote": [], "conflicts": 0, "gaps": 0, "leads": 0}
    section = None
    fence = None
    for line in text.splitlines():
        fm = FENCE.match(line)
        if fence:
            if fm and fm.group(1)[0] == fence[0] and len(fm.group(1)) >= len(fence) and not fm.group(2).strip():
                fence = None
            continue
        if fm:
            fence = fm.group(1)
            continue
        m = SECTION.match(line)
        if m:
            section = m.group(2).lower() if len(m.group(1)) == 2 else None
            continue
        if section == "claims" and CLAIM.match(line):
            row["claims"] += 1
            cid = re.search(r"\[(C\d+)\]", line).group(1)
            fields = legacy_fields(line)
            if not has_source(fields.get("src", "")):
                row["no_src"].append(cid)
            if not has_quote(fields.get("quote", "")):
                row["no_quote"].append(cid)
            if fields.get("type", "").lower() == "official":
                row["official"] += 1
            else:
                row["secondary"] += 1
        elif section in ("conflicts", "gaps", "leads") and line.strip().startswith("-"):
            if line.strip() in ("-", "- none", "- 无", "- <…>"):
                continue
            row[section] += 1
    return row


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notes_dir", type=Path)
    parser.add_argument("--round", type=int, dest="round_number")
    parser.add_argument("--max-chars", type=int, help="optional advisory length limit")
    args = parser.parse_args(argv[1:])
    if not args.notes_dir.is_dir():
        parser.error(f"notes directory does not exist: {args.notes_dir}")
    if args.max_chars is not None and args.max_chars < 1:
        parser.error("--max-chars must be positive")
    if args.round_number is not None and args.round_number < 0:
        parser.error("--round must be non-negative")
    notes = args.notes_dir
    pattern = f"r{args.round_number}-*.md" if args.round_number is not None else "*.md"
    rows = [lint(p) for p in sorted(notes.glob(pattern)) if p.is_file()]
    if not rows:
        print(f"NOT ASSESSED: no notes matching {notes}/{pattern}")
        return 0
    print("Legacy-format diagnostics only; source truth and freeform content are NOT ASSESSED.")
    print("| note | claims | official | secondary | no src | no quote | conflicts | gaps | leads |")
    print("|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['file']} | {r['claims']} | {r['official']} | {r['secondary']} | "
              f"{','.join(r['no_src']) or ''} | {','.join(r['no_quote']) or ''} | "
              f"{r['conflicts']} | {r['gaps']} | {r['leads']} |")
    tot = {k: sum(r[k] for r in rows) for k in ("claims", "official", "secondary", "conflicts", "gaps", "leads")}
    bad = sum(len(r["no_src"]) + len(r["no_quote"]) for r in rows)
    empty = [r["file"] for r in rows if r["claims"] == 0]
    print(f"\ntotal: {len(rows)} notes, {tot['claims']} claims "
          f"(official {tot['official']}, secondary {tot['secondary']}), {bad} missing src/quote, "
          f"{tot['conflicts']} conflicts, {tot['gaps']} gaps, {tot['leads']} leads")
    if empty:
        print("NOT ASSESSED: no legacy C# claims parsed in " + ", ".join(empty) +
              "; this may be freeform notes, an empty note, or a format problem. Read manually.")
    if args.max_chars is not None:
        long = [f"{r['file']} ({r['chars']})" for r in rows if r["chars"] > args.max_chars]
        if long:
            print(f"notes over {args.max_chars} chars: " + ", ".join(long))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
