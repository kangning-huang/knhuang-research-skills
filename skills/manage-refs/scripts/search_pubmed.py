#!/usr/bin/env python3
"""
search_pubmed.py — Search PubMed via E-utilities API.

Usage:
    python3 search_pubmed.py "urban scaling laws"              # Basic search
    python3 search_pubmed.py "root ecology scaling" --max 10   # More results
    python3 search_pubmed.py "Lu M[Author] root" --max 5       # Author search

Part of manage-refs skill.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET


ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
# Set NCBI_EMAIL env var to your address (NCBI requests a contact for high-volume use).
_email = os.environ.get("NCBI_EMAIL", "lulab-research-skills@example.com")
USER_AGENT = f"CitationManager/1.0 (mailto:{_email})"


def fetch_url(url):
    """Fetch URL content."""
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8")
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return None


def search_pubmed(query, max_results=5):
    """Search PubMed and return list of summaries."""
    # Step 1: ESearch to get PMIDs
    params = urllib.parse.urlencode({
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance"
    })
    raw = fetch_url(f"{ESEARCH_URL}?{params}")
    if not raw:
        return []

    data = json.loads(raw)
    id_list = data.get("esearchresult", {}).get("idlist", [])
    total = data.get("esearchresult", {}).get("count", "0")

    if not id_list:
        return []

    print(f"Found {total} results, showing top {len(id_list)}", file=sys.stderr)

    # Step 2: ESummary to get metadata
    ids = ",".join(id_list)
    params2 = urllib.parse.urlencode({
        "db": "pubmed",
        "id": ids,
        "retmode": "json"
    })
    raw2 = fetch_url(f"{ESUMMARY_URL}?{params2}")
    if not raw2:
        return []

    data2 = json.loads(raw2)
    results = []

    for pmid in id_list:
        item = data2.get("result", {}).get(pmid, {})
        if not item or "error" in item:
            continue

        authors = []
        for a in item.get("authors", []):
            authors.append(a.get("name", ""))

        # Extract DOI from articleids
        doi = ""
        for aid in item.get("articleids", []):
            if aid.get("idtype") == "doi":
                doi = aid.get("value", "")
                break

        results.append({
            "pmid": pmid,
            "title": item.get("title", ""),
            "authors": authors,
            "journal": item.get("fulljournalname", item.get("source", "")),
            "year": item.get("pubdate", "")[:4],
            "volume": item.get("volume", ""),
            "issue": item.get("issue", ""),
            "pages": item.get("pages", ""),
            "doi": doi
        })

    return results


def format_result(i, r):
    """Format a single result for display."""
    author_str = r["authors"][0] if r["authors"] else "Unknown"
    if len(r["authors"]) > 2:
        author_str += " et al."
    elif len(r["authors"]) == 2:
        author_str += f" & {r['authors'][1]}"

    lines = [f"[{i}] {author_str} ({r['year']})"]
    lines.append(f"    {r['title']}")
    lines.append(f"    {r['journal']}")
    if r["doi"]:
        lines.append(f"    DOI: https://doi.org/{r['doi']}")
    lines.append(f"    PMID: {r['pmid']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Search PubMed")
    parser.add_argument("query", help="Search query (supports PubMed syntax)")
    parser.add_argument("--max", "-n", type=int, default=5, help="Max results (default: 5)")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON")
    args = parser.parse_args()

    print(f"Searching PubMed: '{args.query}'")
    print("=" * 60)

    results = search_pubmed(args.query, args.max)

    if not results:
        print("No results found.")
        sys.exit(1)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for i, r in enumerate(results, 1):
            print(format_result(i, r))
            print()

    print("=" * 60)
    print(f"To get full metadata: python3 extract_metadata.py --pmid <PMID>")
    print(f"To get BibTeX: python3 doi_to_bibtex.py \"<DOI>\"")


if __name__ == "__main__":
    main()
