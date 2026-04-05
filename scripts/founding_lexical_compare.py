#!/usr/bin/env python3
"""
Preregistered lexical proxy for Greco-Roman vs English constitutional idiom in founding-era
texts fetched as HTML (or plain text) from Avalon, Archives, Founders' Constitution (Chicago),
Wikisource, Gutenberg, constitution.org, etc. **Not** semantic understanding: counts are sensitive
to word-list choice. For operator research only; not Record.

Usage (from repo root):
  python3 scripts/founding_lexical_compare.py
  python3 scripts/founding_lexical_compare.py --json

Canon: 32 rows aligned with `docs/skill-work/work-strategy/founding-influences-graeco-roman-vs-english.md` (Table 1).
Row 3 (*Farmer*) concatenates twelve Wikisource letter URLs. Sources are frozen in FOUNDING_CANON.

Word lists (lowercase, whole-token match, min length 3 from [a-z]+):

- **EN_LEX** — British imperial–constitutional / colonial–legal proxy (crown, parliament, colonies, charter, jury, taxation, petition, …); not limited to “grievance” rhetoric.
- **EN2_LEX** — rights / common-law / adjudication proxy (liberty, rights, court, constitution, …).
  Sensitivity block compares buckets under EN vs EN2 against the same **GR_LEX**.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from html import unescape

# Classical-republic / design-discourse proxy (Montesquieu–Polybius family, civic language).
GR_LEX = frozenset(
    {
        "republic",
        "republican",
        "republicans",
        "senate",
        "faction",
        "factions",
        "virtue",
        "virtues",
        "corruption",
        "corrupt",
        "ambition",
        "ambitious",
        "ancient",
        "roman",
        "despotic",
        "despotism",
        "magistrate",
        "magistrates",
        "legislature",
        "legislative",
        "legislatures",
        "confederacy",
        "confederacies",
        "confederate",
        "democracy",
        "democratic",
        "majority",
        "majorities",
        "minority",
        "minorities",
        "department",
        "departments",
        "tyranny",
        "tyrant",
        "tyrants",
        "vice",
        "vices",
        "senatorial",
        "polybius",
    }
)

# English: Westminster-and-empire / colonial legal idiom (parliament, crown, colonies, charter, jury, tax, …).
EN_LEX = frozenset(
    {
        "king",
        "crown",
        "british",
        "parliament",
        "charter",
        "charters",
        "jury",
        "taxation",
        "tax",
        "taxes",
        "petition",
        "petitions",
        "grievance",
        "grievances",
        "assent",
        "governor",
        "governors",
        "subjects",
        "repeal",
        "english",
        "colonies",
        "colony",
        "colonial",
        "prince",
    }
)

# English / rights–common-law register proxy (liberty, courts, written constitution).
# Preregistered for sensitivity vs EN_LEX; not a substitute for semantic coding.
EN2_LEX = frozenset(
    {
        "rights",
        "right",
        "liberty",
        "liberties",
        "law",
        "laws",
        "lawful",
        "unlawful",
        "precedent",
        "property",
        "constitution",
        "constitutional",
        "unconstitutional",
        "habeas",
        "counsel",
        "court",
        "courts",
        "judge",
        "judges",
        "judgment",
        "judicial",
        "equity",
        "witness",
        "witnesses",
        "indictment",
        "trial",
        "trials",
        "franchise",
        "freeholder",
        "freeholders",
        "contract",
        "contracts",
        "suffrage",
    }
)

AV = "https://avalon.law.yale.edu/18th_century"
FC = "https://press-pubs.uchicago.edu/founders/documents"
WS_FARMER = "https://en.wikisource.org/wiki/Letters_from_a_Farmer_in_Pennsylvania/Letter_{}?action=render"

# (matrix #, short title, one or more URLs — fetched and concatenated in order)
FOUNDING_CANON: list[tuple[int, str, tuple[str, ...]]] = [
    (
        1,
        "Virginia Resolves (1765)",
        ("https://constitution.org/2-Authors/bcp/vir_res1765.txt",),
    ),
    (2, "Stamp Act Congress: Declaration of Rights and Grievances (1765)", (f"{AV}/resolu65.asp",)),
    (
        3,
        "Letters from a Farmer in Pennsylvania (1767-68)",
        tuple(WS_FARMER.format(i) for i in range(1, 13)),
    ),
    (4, "Massachusetts Circular Letter (1768)", (f"{AV}/mass_circ_let_1768.asp",)),
    (
        5,
        "Summary View of the Rights of British America (1774)",
        ("https://en.wikisource.org/wiki/A_Summary_View_of_the_Rights_of_British_America?action=render",),
    ),
    (
        6,
        "First Continental Congress: Declaration and Resolves (1774)",
        (f"{AV}/resolves.asp",),
    ),
    (7, "Continental Association (1774)", (f"{AV}/contcong_10-20-74.asp",)),
    (8, "Olive Branch Petition (1775)", (f"{AV}/contcong_07-08-75.asp",)),
    (9, "Declaration of Causes: Taking Up Arms (1775)", (f"{AV}/arms.asp",)),
    (
        10,
        "Common Sense (1776)",
        # Prefer bundled HTML; /cache/epub/…/pg375.txt intermittently fails or stalls with strict bots.
        ("https://www.gutenberg.org/files/375/375-h/375-h.htm",),
    ),
    (11, "Declaration of Independence (1776)", (f"{AV}/declare.asp",)),
    (12, "Virginia Declaration of Rights (1776)", (f"{AV}/virginia.asp",)),
    (13, "Articles of Confederation", (f"{AV}/artconf.asp",)),
    (14, "Northwest Ordinance (1787)", (f"{AV}/nworder.asp",)),
    (15, "Virginia Plan (1787)", (f"{FC}/v1ch8s7.html",)),
    (16, "New Jersey Plan (1787)", (f"{FC}/v1ch8s9.html",)),
    (
        17,
        "US Constitution (1787; Archives transcript)",
        ("https://www.archives.gov/founding-docs/constitution-transcript",),
    ),
    (
        18,
        "Washington: Letter of Transmittal (1787)",
        (f"{AV}/translet.asp",),
    ),
    (19, "The Federalist No. 1", (f"{AV}/fed01.asp",)),
    (20, "The Federalist No. 10", (f"{AV}/fed10.asp",)),
    (21, "The Federalist No. 37", (f"{AV}/fed37.asp",)),
    (22, "The Federalist No. 39", (f"{AV}/fed39.asp",)),
    (23, "The Federalist No. 47", (f"{AV}/fed47.asp",)),
    (24, "The Federalist No. 48", (f"{AV}/fed48.asp",)),
    (25, "The Federalist No. 51", (f"{AV}/fed51.asp",)),
    (26, "The Federalist No. 63", (f"{AV}/fed63.asp",)),
    (27, "The Federalist No. 78", (f"{AV}/fed78.asp",)),
    (28, 'Anti-Federalist Brutus I', (f"{FC}/v1ch8s13.html",)),
    (29, "Anti-Federalist Brutus II", (f"{FC}/v1ch14s26.html",)),
    (30, "Anti-Federalist Federal Farmer I", (f"{FC}/v1ch8s12.html",)),
    (31, "Anti-Federalist Federal Farmer II", (f"{FC}/v1ch13s20.html",)),
    (32, "Anti-Federalist Centinel I", (f"{FC}/v1ch11s11.html",)),
]


def fetch_html(url: str, timeout: int = 60) -> str:
    # Browser-like UA: some mirrors (e.g. Project Gutenberg) block non-browser defaults.
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (compatible; grace-mar-founding-lexical/1.1; "
                "+https://github.com/) AppleWebKit/537.36 (KHTML, like Gecko)"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def html_to_text(html: str) -> str:
    html = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style.*?>.*?</style>", " ", html)
    html = re.sub(r"<[^>]+>", " ", html)
    return unescape(html)


def _share(gr: int, en: int) -> float:
    d = gr + en
    return (gr / d) if d else 0.0


def analyze(text: str) -> dict[str, float | int]:
    tokens = re.findall(r"[a-z]{3,}", text.lower())
    n = len(tokens)
    if n == 0:
        return {
            "n_tokens": 0,
            "gr_hits": 0,
            "en_hits": 0,
            "en2_hits": 0,
            "gr_per_1k": 0.0,
            "en_per_1k": 0.0,
            "en2_per_1k": 0.0,
            "gr_share_of_lex_hits": 0.0,
            "gr_share_gr_en2": 0.0,
        }
    gr_hits = sum(1 for t in tokens if t in GR_LEX)
    en_hits = sum(1 for t in tokens if t in EN_LEX)
    en2_hits = sum(1 for t in tokens if t in EN2_LEX)
    gr_per_1k = 1000.0 * gr_hits / n
    en_per_1k = 1000.0 * en_hits / n
    en2_per_1k = 1000.0 * en2_hits / n
    return {
        "n_tokens": n,
        "gr_hits": gr_hits,
        "en_hits": en_hits,
        "en2_hits": en2_hits,
        "gr_per_1k": round(gr_per_1k, 2),
        "en_per_1k": round(en_per_1k, 2),
        "en2_per_1k": round(en2_per_1k, 2),
        "gr_share_of_lex_hits": round(_share(gr_hits, en_hits), 3),
        "gr_share_gr_en2": round(_share(gr_hits, en2_hits), 3),
    }


def process_entry(cid: int, title: str, urls: tuple[str, ...]) -> dict[str, object]:
    parts: list[str] = []
    errors: list[str] = []
    for u in urls:
        try:
            raw = fetch_html(u)
            parts.append(html_to_text(raw))
        except OSError as e:
            errors.append(f"{u}: {e}")
    if errors and not parts:
        return {
            "canon_id": cid,
            "title": title,
            "url": urls[0],
            "urls": list(urls),
            "error": "; ".join(errors),
        }
    combined = "\n\n".join(parts)
    stats = analyze(combined)
    return {
        "canon_id": cid,
        "title": title,
        "url": urls[0],
        "url_count": len(urls),
        "urls": list(urls),
        **stats,
        **({"fetch_errors": errors} if errors else {}),
    }


def mean_per_1k(rs: list[dict], key: str) -> float:
    ok = [r for r in rs if "error" not in r and r.get("n_tokens", 0) > 0]
    return sum(float(x[key]) for x in ok) / len(ok) if ok else 0.0


def mean_gr_share(rs: list[dict], key: str = "gr_share_of_lex_hits") -> float:
    if key == "gr_share_of_lex_hits":
        ok = [r for r in rs if "error" not in r and (r.get("gr_hits", 0) + r.get("en_hits", 0)) > 0]
    else:
        ok = [r for r in rs if "error" not in r and (r.get("gr_hits", 0) + r.get("en2_hits", 0)) > 0]
    if not ok:
        return 0.0
    return sum(float(x[key]) for x in ok) / len(ok)


def bucket(rows_by_id: dict[int, dict], lo: int, hi: int) -> list[dict]:
    return [rows_by_id[i] for i in range(lo, hi + 1) if i in rows_by_id and "error" not in rows_by_id[i]]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="Emit JSON rows to stdout")
    args = ap.parse_args()
    rows: list[dict[str, object]] = []
    for cid, title, urls in FOUNDING_CANON:
        rows.append(process_entry(cid, title, urls))

    rows_by_id = {int(r["canon_id"]): r for r in rows}

    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    print(
        f"GR_LEX n={len(GR_LEX)} EN_LEX n={len(EN_LEX)} EN2_LEX n={len(EN2_LEX)} "
        f"GR∩EN={sorted(GR_LEX & EN_LEX)} GR∩EN2={sorted(GR_LEX & EN2_LEX)} "
        f"EN∩EN2={sorted(EN_LEX & EN2_LEX)}"
    )
    print(f"Canon units: {len(FOUNDING_CANON)} (row 3 = {len(FOUNDING_CANON[2][2])} concatenated URLs)")
    print()
    hdr = (
        f"{'#':>3} {'Document':<40} {'N tok':>7} {'GR':>4} {'EN':>4} {'E2':>4} "
        f"{'GR/1k':>7} {'EN/1k':>7} {'E2/1k':>7} {'G/(G+E)':>8} {'G/(G+E2)':>9}"
    )
    print(hdr)
    print("-" * len(hdr))
    for r in sorted(rows, key=lambda x: int(x["canon_id"])):  # type: ignore[arg-type, return-value]
        if "error" in r:
            print(f"{r['canon_id']:>3} {str(r['title'])[:39]:<40} ERROR {str(r['error'])[:45]}")
            continue
        fe = " *" if r.get("fetch_errors") else ""
        print(
            f"{r['canon_id']:>3} {str(r['title'])[:39]:<40} {r['n_tokens']:>7} "
            f"{r['gr_hits']:>4} {r['en_hits']:>4} {r['en2_hits']:>4} "
            f"{r['gr_per_1k']:>7.2f} {r['en_per_1k']:>7.2f} {r['en2_per_1k']:>7.2f} "
            f"{r['gr_share_of_lex_hits']:>8.3f} {r['gr_share_gr_en2']:>9.3f}{fe}"
        )
    if any(r.get("fetch_errors") for r in rows):
        print("\n* Partial fetch: some URLs failed; stats use successfully fetched parts only.")

    def summarize(
        label: str,
        slice_rows: list[dict],
        *,
        include_en2: bool = False,
    ) -> None:
        if not slice_rows:
            return
        line = (
            f"  {label} (n={len(slice_rows)}): mean GR/1k = {mean_per_1k(slice_rows, 'gr_per_1k'):.2f}, "
            f"EN/1k = {mean_per_1k(slice_rows, 'en_per_1k'):.2f}, "
            f"mean GR/(GR+EN) = {mean_gr_share(slice_rows, 'gr_share_of_lex_hits'):.3f}"
        )
        if include_en2:
            line += (
                f" | EN2/1k = {mean_per_1k(slice_rows, 'en2_per_1k'):.2f}, "
                f"mean GR/(GR+EN2) = {mean_gr_share(slice_rows, 'gr_share_gr_en2'):.3f}"
            )
        print(line)

    print()
    print("Bucket summary (lexical proxy; matches Phase A row bands in founding doc §5):")
    summarize("Rows 1-12 (imperial crisis to independence)", bucket(rows_by_id, 1, 12), include_en2=True)
    summarize("Rows 13-18 (Articles through transmittal)", bucket(rows_by_id, 13, 18), include_en2=True)
    summarize("Rows 19-27 (Federalist sample)", bucket(rows_by_id, 19, 27), include_en2=True)
    summarize("Rows 28-32 (Anti-Federalist sample)", bucket(rows_by_id, 28, 32), include_en2=True)
    ok_all = [r for r in rows if "error" not in r]
    summarize("All 32 units (successful fetches only)", ok_all, include_en2=True)

    fed = bucket(rows_by_id, 19, 27)
    non_fed = [r for r in ok_all if int(r["canon_id"]) not in range(19, 28)]  # type: ignore[arg-type]
    if fed and non_fed:
        print()
        print("Legacy 2-bucket (non-Federalist vs Federalist 19-27):")
        summarize("Non-Federalist (rows 1-18 + 28-32)", non_fed, include_en2=True)
        summarize("Federalist 19-27", fed, include_en2=True)

    print()
    print("Sensitivity (EN vs EN2 on same GR_LEX; EN = imperial–constitutional/colonial; EN2 = rights/common-law):")
    print(
        f"{'Slice':<46} {'EN/1k':>8} {'EN2/1k':>8} {'GR/(G+E)':>10} {'GR/(G+E2)':>11} "
        f"{'Δ share':>8}"
    )
    print("-" * 91)

    def sens_row(name: str, slice_rows: list[dict]) -> None:
        if not slice_rows:
            return
        m_en = mean_per_1k(slice_rows, "en_per_1k")
        m_e2 = mean_per_1k(slice_rows, "en2_per_1k")
        s1 = mean_gr_share(slice_rows, "gr_share_of_lex_hits")
        s2 = mean_gr_share(slice_rows, "gr_share_gr_en2")
        print(f"{name:<46} {m_en:>8.2f} {m_e2:>8.2f} {s1:>10.3f} {s2:>11.3f} {s2 - s1:>+8.3f}")

    sens_row("Rows 1-12", bucket(rows_by_id, 1, 12))
    sens_row("Rows 13-18", bucket(rows_by_id, 13, 18))
    sens_row("Rows 19-27 (Federalist)", bucket(rows_by_id, 19, 27))
    sens_row("Rows 28-32 (Anti-Federalist)", bucket(rows_by_id, 28, 32))
    sens_row("All 32", ok_all)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
