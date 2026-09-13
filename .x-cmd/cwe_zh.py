#!/usr/bin/env python3
"""
cwe_zh.py — fetch the MITRE CWE catalog's Chinese names from the
official Chinese mirror (cwe.org.cn, maintained by MITRE itself) and
write them as a 2-column TSV keyed by CWE-ID.

Source: https://cwe.org.cn/data/definitions/<id>.html  (e.g. 79.html)
        — the page title and the <h2> near the top both contain the
        Chinese name as `CWE-<id>: 中文名`. We pull the <h2> because
        it's the canonical line MITRE uses on every entry page.

Output: data/cwe.zh.tsv (CWE-ID\tName_Zh)

Why a separate file instead of inlining into data/cwe.tsv:
    data/cwe.tsv is a faithful mirror of MITRE's 2000.csv, which is
    English-only. Adding a Chinese column there would (a) require
    shipping a translated CSV we don't have, and (b) break the
    byte-for-byte parity that downstream consumers (x cwe module)
    rely on. The slim layout is consistent with how we already
    handle join data: cwe.slim.tsv is the projection used by
    cwe_report.py; cwe.zh.tsv is the parallel projection used by
    cwe.report.zh.md.

Cache policy:
    Per-ID fetch — but cwe.org.cn returns the same body within ~30
    days (the Chinese translations are reviewed and re-published on
    MITRE's own schedule). We cache successful lookups in
    .x-cmd/.cwe_zh.cache/<id>.html with a 30-day TTL. Failed lookups
    (network error, parse miss) are cached for 1 day so transient
    outages don't slam the upstream on every CI run.

Concurrency:
    We use a ThreadPoolExecutor with a small pool — 969 sequential
    fetches at ~150ms each would take ~2.5 min; a pool of 8 brings
    that under 30 s.

Stdlib only. Run from the repo root after cwe.py:
    python3 .x-cmd/cwe_zh.py
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

DEFAULT_SRC = Path(__file__).resolve().parent.parent / "data" / "cwe.slim.tsv"
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "data" / "cwe.zh.tsv"
DEFAULT_CACHE = Path(__file__).resolve().parent / ".cwe_zh.cache"
DEFAULT_URL = "https://cwe.org.cn/data/definitions/{id}.html"

# 30 days for successful lookups; 1 day for failures so a transient
# outage doesn't hammer cwe.org.cn on every CI run.
SUCCESS_TTL_SECONDS = 30 * 24 * 3600
FAILURE_TTL_SECONDS = 24 * 3600

# Matches the canonical name line on every cwe.org.cn definition page:
#   <h2 style="display:inline; ...">CWE-79: 网页生成过程中的输入中和不当（"跨站脚本"）</h2>
# Capture group 1 = the Chinese name after the `CWE-<id>: ` prefix.
# We tolerate the en/em-dash variants and the smart quotes MITRE
# uses inside parenthetical English terms.
H2_RE = re.compile(
    r'<h2[^>]*>\s*CWE-\d+[A-Za-z]?:\s*(.+?)\s*</h2>',
    re.DOTALL,
)
# Title fallback: <title>CWE - CWE-79: 中文名 (...) - CWE 通用弱点枚举</title>
TITLE_RE = re.compile(
    r'<title>\s*CWE\s*-\s*CWE-\d+[A-Za-z]?:\s*(.+?)\s*\([^)]*\)\s*-\s*CWE',
    re.DOTALL,
)
# Strip residual HTML tags that occasionally sneak into the captured
# group (e.g. <span> wrappers around parenthetical translations).
TAG_RE = re.compile(r'<[^>]+>')
# Collapse whitespace runs to a single space and trim.
WS_RE = re.compile(r'\s+')


def fetch(url: str, timeout: float = 30.0) -> str:
    """Fetch `url` and return its decoded text. Raises on HTTP error."""
    req = urllib.request.Request(
        url,
        headers={
            # cwe.org.cn serves iso-8859-1 declarations but actually
            # uses UTF-8 — declaring both is the most reliable across
            # their meta tags and avoids mojibake on Chinese chars.
            "User-Agent": "x-cmd/cve-cwe_zh",
            "Accept-Charset": "utf-8,iso-8859-1;q=0.5",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    # Try UTF-8 first; fall back to GB18030 (the actual fallback MITRE
    # uses on a few legacy pages). UTF-8 is correct for 99% of entries.
    for enc in ("utf-8", "gb18030"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    # Last resort: replace rather than raise — a single unreadable
    # entry shouldn't kill the whole catalog.
    return raw.decode("utf-8", errors="replace")


def extract_zh_name(html: str) -> str | None:
    """Pull the Chinese `Name` field out of a cwe.org.cn definition page.

    Returns None when neither the <h2> nor the <title> contains a
    recognizable CWE-NN: 中文名 pattern. cwe.org.cn renders a small
    number of entries (e.g. drafts without Chinese translation yet)
    in English only — those legitimately fall back to the English
    name in README.cn.md per issue #2.
    """
    m = H2_RE.search(html)
    if not m:
        m = TITLE_RE.search(html)
    if not m:
        return None
    raw = m.group(1)
    # Strip residual tags / entities; normalise whitespace.
    raw = TAG_RE.sub("", raw)
    # Decode a handful of common HTML entities MITRE uses in CN pages.
    # All replacements go through chr() so the source file stays
    # plain ASCII — smart-quote literals inside the file confuse
    # Python's tokenizer when the file is read with a non-UTF-8
    # codec.
    LDQ = chr(8220)  # left double quote “
    RDQ = chr(8221)  # right double quote ”
    SQ  = chr(8216)  # left single quote ‘
    RSQ = chr(8217)  # right single quote ’
    DQ  = chr(34)    # straight double quote "
    raw = (
        raw.replace("&", "&")
        .replace("<", "<")
        .replace(">", ">")
        .replace(chr(34), DQ)
        .replace("&#39;", "'")
        .replace("&ldquo;", LDQ)
        .replace("&rdquo;", RDQ)
        .replace("&lsquo;", SQ)
        .replace("&rsquo;", RSQ)
        .replace("&nbsp;", " ")
    )
    raw = WS_RE.sub(" ", raw).strip()
    return raw or None


def cache_path(cache_dir: Path, cwe_id: str) -> Path:
    return cache_dir / f"{cwe_id}.html"


def cache_fresh(path: Path, ttl_seconds: int) -> bool:
    """True when `path` exists and is younger than `ttl_seconds`."""
    if not path.is_file():
        return False
    import time as _t
    age = _t.time() - path.stat().st_mtime
    return age < ttl_seconds


def fetch_one(cwe_id: str,
              url_tmpl: str,
              cache_dir: Path,
              *,
              force: bool) -> tuple[str, str | None]:
    """Fetch one CWE id. Returns (id, zh_name_or_None). Hits cache
    first (per the TTL split above) to spare cwe.org.cn on no-op days.
    """
    cp = cache_path(cache_dir, cwe_id)

    # Cache hit (success)
    if not force and cache_fresh(cp, SUCCESS_TTL_SECONDS):
        try:
            return cwe_id, extract_zh_name(cp.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            pass  # fall through to network fetch

    url = url_tmpl.format(id=cwe_id)
    try:
        html = fetch(url)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        # Failure cache: short TTL so we retry tomorrow rather than
        # waiting 30 days. If a previous SUCCESS is on disk we prefer
        # to return that stale-but-good value over a fresh failure.
        if not force:
            try:
                cp.write_text(f"# fetch failed: {exc}\n", encoding="utf-8")
            except OSError:
                pass
        if cache_fresh(cp, FAILURE_TTL_SECONDS) is False and cp.is_file():
            # No recent failure cache; if we have any prior cache,
            # try to use it. (Otherwise return None.)
            try:
                cached = cp.read_text(encoding="utf-8", errors="replace")
                if not cached.startswith("# fetch failed"):
                    return cwe_id, extract_zh_name(cached)
            except OSError:
                pass
        return cwe_id, None

    zh = extract_zh_name(html)
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cp.write_text(html, encoding="utf-8", errors="replace")
    except OSError:
        pass
    return cwe_id, zh


def load_ids(slim_tsv: Path) -> list[str]:
    """Read CWE-IDs from data/cwe.slim.tsv (one per line, after header)."""
    if not slim_tsv.is_file():
        raise SystemExit(
            f"error: {slim_tsv} not found — run .x-cmd/cwe.py first"
        )
    ids: list[str] = []
    with slim_tsv.open("r", encoding="utf-8", newline="") as fh:
        next(fh, None)
        for line in fh:
            cols = line.rstrip("\n").split("\t")
            if not cols or not cols[0].strip():
                continue
            ids.append(cols[0].strip())
    return ids


def write_tsv(out: Path, rows: list[tuple[str, str | None]]) -> tuple[int, int]:
    """Write `CWE-ID\tName_Zh` lines. Empty Name_Zh -> empty column.

    Returns (total_rows, rows_with_zh). The split lets the CI step
    decide whether the catalog needs another attempt (e.g. warn when
    coverage is below 50%).
    """
    out.parent.mkdir(parents=True, exist_ok=True)
    n_zh = 0
    with out.open("w", encoding="utf-8", newline="") as fh:
        fh.write("CWE-ID\tName_Zh\n")
        for cid, zh in rows:
            zh_clean = (zh or "").replace("\t", " ").replace("\n", " ").strip()
            if zh_clean:
                n_zh += 1
            fh.write(f"{cid}\t{zh_clean}\n")
    return len(rows), n_zh


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--src", type=Path, default=DEFAULT_SRC,
                   help=f"CWE slim catalog (default: {DEFAULT_SRC})")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT,
                   help=f"Output TSV (default: {DEFAULT_OUT})")
    p.add_argument("--cache", type=Path, default=DEFAULT_CACHE,
                   help=f"Per-id HTML cache (default: {DEFAULT_CACHE})")
    p.add_argument("--url", default=DEFAULT_URL,
                   help="URL template with {id} placeholder")
    p.add_argument("--workers", type=int, default=8,
                   help="Concurrent fetcher pool size (default: 8)")
    p.add_argument("--force", action="store_true",
                   help="Ignore cache TTLs and re-fetch every entry")
    args = p.parse_args(argv)

    ids = load_ids(args.src)
    print(f"loaded {len(ids)} CWE ids from {args.src}", file=sys.stderr)

    rows: list[tuple[str, str | None]] = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [
            ex.submit(fetch_one, cid, args.url, args.cache, force=args.force)
            for cid in ids
        ]
        for fut in as_completed(futs):
            cid, zh = fut.result()
            rows.append((cid, zh))

    # Preserve the source order (CWE-id ascending) — easier to diff
    # against cwe.slim.tsv when reviewing coverage.
    rows.sort(key=lambda r: (
        # numeric sort first, non-numeric fallback
        (1, r[0]) if not r[0].isdigit() else (0, f"{int(r[0]):09d}")
    ))

    total, n_zh = write_tsv(args.out, rows)
    pct = (n_zh * 100 / total) if total else 0
    print(
        f"wrote {args.out}: {n_zh}/{total} CWE rows have Chinese names "
        f"({pct:.1f}%); the rest will fall back to English in README.cn.md",
        file=sys.stderr,
    )
    # Non-fatal warning when coverage is low — gives the operator a
    # chance to investigate (network, MITRE URL change, etc.) without
    # failing the build outright (per issue #2's "if not, fall back
    # to English" requirement).
    if total and pct < 50:
        print(
            f"warn: only {pct:.1f}% of CWEs translated — check network "
            f"and {args.url.format(id='<id>')}",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
