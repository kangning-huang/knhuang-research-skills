#!/usr/bin/env python3
"""
doi_to_bibtex.py — Resolve DOI to verified BibTeX via CrossRef API.

Usage:
    python3 doi_to_bibtex.py "10.1038/nature25181"                    # DOI → BibTeX
    python3 doi_to_bibtex.py --search "global travel time cities"     # Search → top matches
    python3 doi_to_bibtex.py --search "Weiss 2018 travel time" --top 5

Part of manage-refs skill.
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.parse
import urllib.error


CROSSREF_API = "https://api.crossref.org/works"
# CrossRef's "polite pool" prefers a real contact email in User-Agent.
# Set CROSSREF_EMAIL env var to your address for faster, more reliable responses.
_email = os.environ.get("CROSSREF_EMAIL", "lulab-research-skills@example.com")
USER_AGENT = f"CitationManager/1.0 (mailto:{_email})"


def fetch_json(url):
    """Fetch JSON from URL with polite headers."""
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code} for {url}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"ERROR: URL error for {url}: {e.reason}", file=sys.stderr)
        return None


def resolve_doi(doi):
    """Fetch metadata for a single DOI from CrossRef."""
    doi = doi.strip().strip("https://doi.org/")
    url = f"{CROSSREF_API}/{urllib.parse.quote(doi, safe='')}"
    data = fetch_json(url)
    if not data or data.get("status") != "ok":
        return None
    return data["message"]


def search_crossref(query, top=3):
    """Search CrossRef by bibliographic query."""
    params = urllib.parse.urlencode({
        "query.bibliographic": query,
        "rows": top,
        "select": "DOI,title,author,container-title,published-print,published-online,volume,issue,page,type"
    })
    url = f"{CROSSREF_API}?{params}"
    data = fetch_json(url)
    if not data or data.get("status") != "ok":
        return []
    return data["message"].get("items", [])


def extract_authors(item):
    """Extract author list from CrossRef item."""
    authors = item.get("author", [])
    parts = []
    for a in authors:
        given = a.get("given", "")
        family = a.get("family", "")
        if family:
            parts.append(f"{family}, {given}")
    return parts


def format_author_bibtex(authors):
    """Format authors for BibTeX 'author' field."""
    return " and ".join(authors)


def format_author_readable(authors):
    """Format authors for human-readable citation."""
    if len(authors) == 0:
        return "Unknown"
    elif len(authors) == 1:
        return authors[0].split(",")[0]
    elif len(authors) == 2:
        return f"{authors[0].split(',')[0]} & {authors[1].split(',')[0]}"
    else:
        return f"{authors[0].split(',')[0]} et al."


def get_year(item):
    """Extract year from CrossRef date fields."""
    for field in ["published-print", "published-online", "created"]:
        date_parts = item.get(field, {}).get("date-parts", [[]])
        if date_parts and date_parts[0] and date_parts[0][0]:
            return str(date_parts[0][0])
    return "n.d."


def make_bibtex_key(item):
    """Generate bibtex key: firstauthor_lowercase + year."""
    authors = item.get("author", [])
    if authors:
        family = authors[0].get("family", "unknown").lower()
        family = re.sub(r"[^a-z]", "", family)
    else:
        family = "unknown"
    year = get_year(item)
    return f"{family}{year}"


def item_to_bibtex(item):
    """Convert CrossRef item to BibTeX string."""
    doi = item.get("DOI", "")
    title = item.get("title", [""])[0] if item.get("title") else ""
    journal = item.get("container-title", [""])[0] if item.get("container-title") else ""
    year = get_year(item)
    volume = item.get("volume", "")
    issue = item.get("issue", "")
    page = item.get("page", "")
    authors = extract_authors(item)
    key = make_bibtex_key(item)

    entry_type = item.get("type", "article-journal")
    bib_type = "article" if "article" in entry_type else "misc"

    lines = [f"@{bib_type}{{{key},"]
    lines.append(f"  author = {{{format_author_bibtex(authors)}}},")
    lines.append(f"  title = {{{title}}},")
    if journal:
        lines.append(f"  journal = {{{journal}}},")
    lines.append(f"  year = {{{year}}},")
    if volume:
        lines.append(f"  volume = {{{volume}}},")
    if issue:
        lines.append(f"  number = {{{issue}}},")
    if page:
        lines.append(f"  pages = {{{page}}},")
    lines.append(f"  doi = {{{doi}}},")
    lines.append(f"  url = {{https://doi.org/{doi}}},")
    lines.append(f"  annote = {{Why cited: }}")
    lines.append("}")

    return "\n".join(lines)


def item_to_readable(item):
    """Convert CrossRef item to human-readable citation."""
    authors = extract_authors(item)
    readable = format_author_readable(authors)
    year = get_year(item)
    title = item.get("title", [""])[0] if item.get("title") else ""
    journal = item.get("container-title", [""])[0] if item.get("container-title") else ""
    volume = item.get("volume", "")
    page = item.get("page", "")
    doi = item.get("DOI", "")

    parts = [f"{readable} ({year})."]
    parts.append(f'"{title}."')
    if journal:
        vol_str = f", {volume}" if volume else ""
        page_str = f", {page}" if page else ""
        parts.append(f"*{journal}*{vol_str}{page_str}.")
    parts.append(f"[DOI](https://doi.org/{doi})")

    return " ".join(parts)


def main():
    parser = argparse.ArgumentParser(description="DOI → verified BibTeX via CrossRef")
    parser.add_argument("doi", nargs="?", help="DOI to resolve (e.g. 10.1038/nature25181)")
    parser.add_argument("--search", "-s", help="Search CrossRef by bibliographic query")
    parser.add_argument("--top", "-n", type=int, default=3, help="Number of search results (default: 3)")
    parser.add_argument("--bibtex", "-b", action="store_true", help="Output BibTeX format (default)")
    parser.add_argument("--readable", "-r", action="store_true", help="Output human-readable citation")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON metadata")
    args = parser.parse_args()

    if args.search:
        # Search mode
        print(f"Searching CrossRef: '{args.search}'")
        print("=" * 60)
        items = search_crossref(args.search, args.top)
        if not items:
            print("No results found.", file=sys.stderr)
            sys.exit(1)
        for i, item in enumerate(items, 1):
            authors = extract_authors(item)
            year = get_year(item)
            title = item.get("title", ["?"])[0] if item.get("title") else "?"
            journal = item.get("container-title", ["?"])[0] if item.get("container-title") else "?"
            doi = item.get("DOI", "?")
            print(f"\n[{i}] {format_author_readable(authors)} ({year})")
            print(f"    Title: {title}")
            print(f"    Journal: {journal}")
            print(f"    DOI: https://doi.org/{doi}")
        print("\n" + "=" * 60)
        print(f"To resolve a DOI: python3 {sys.argv[0]} \"<DOI>\"")

    elif args.doi:
        # Resolve mode
        doi = args.doi.strip()
        print(f"Resolving DOI: {doi}", file=sys.stderr)
        item = resolve_doi(doi)
        if not item:
            print(f"FAILED: Could not resolve DOI '{doi}'", file=sys.stderr)
            sys.exit(1)

        # Verify: print what we found
        title = item.get("title", [""])[0] if item.get("title") else ""
        authors = extract_authors(item)
        year = get_year(item)
        print(f"VERIFIED: {format_author_readable(authors)} ({year})", file=sys.stderr)
        print(f"  Title: {title}", file=sys.stderr)

        if args.json:
            print(json.dumps(item, indent=2))
        elif args.readable:
            print(item_to_readable(item))
        else:
            print(item_to_bibtex(item))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
