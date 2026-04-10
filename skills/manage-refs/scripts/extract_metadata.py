#!/usr/bin/env python3
"""
extract_metadata.py — Extract structured metadata from DOI, PMID, or arXiv ID.

Usage:
    python3 extract_metadata.py "10.1038/nature25181"          # DOI
    python3 extract_metadata.py --pmid 29320477                # PubMed ID
    python3 extract_metadata.py --arxiv 2301.12345             # arXiv ID

Outputs structured metadata (JSON or readable).

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


# Set CROSSREF_EMAIL env var to your address for CrossRef's polite pool.
_email = os.environ.get("CROSSREF_EMAIL", "lulab-research-skills@example.com")
USER_AGENT = f"CitationManager/1.0 (mailto:{_email})"


def fetch_url(url, accept="application/json"):
    """Fetch URL with polite headers."""
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": accept
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8")
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return None


def from_doi(doi):
    """Extract metadata from DOI via CrossRef."""
    doi = doi.strip().replace("https://doi.org/", "")
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}"
    raw = fetch_url(url)
    if not raw:
        return None
    data = json.loads(raw)
    if data.get("status") != "ok":
        return None

    item = data["message"]
    authors = []
    for a in item.get("author", []):
        authors.append({"given": a.get("given", ""), "family": a.get("family", "")})

    year = None
    for field in ["published-print", "published-online", "created"]:
        dp = item.get(field, {}).get("date-parts", [[]])
        if dp and dp[0] and dp[0][0]:
            year = dp[0][0]
            break

    return {
        "source": "crossref",
        "doi": item.get("DOI", ""),
        "title": item.get("title", [""])[0] if item.get("title") else "",
        "authors": authors,
        "year": year,
        "journal": item.get("container-title", [""])[0] if item.get("container-title") else "",
        "volume": item.get("volume", ""),
        "issue": item.get("issue", ""),
        "pages": item.get("page", ""),
        "type": item.get("type", ""),
        "url": f"https://doi.org/{item.get('DOI', '')}",
        "abstract": item.get("abstract", "")[:500] if item.get("abstract") else ""
    }


def from_pmid(pmid):
    """Extract metadata from PubMed ID via E-utilities."""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&rettype=xml"
    raw = fetch_url(url, accept="text/xml")
    if not raw:
        return None

    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        print("ERROR: Failed to parse PubMed XML", file=sys.stderr)
        return None

    article = root.find(".//Article")
    if article is None:
        return None

    title_el = article.find(".//ArticleTitle")
    title = title_el.text if title_el is not None else ""

    authors = []
    for author in article.findall(".//Author"):
        last = author.find("LastName")
        first = author.find("ForeName")
        if last is not None:
            authors.append({
                "given": first.text if first is not None else "",
                "family": last.text
            })

    journal_el = article.find(".//Journal/Title")
    journal = journal_el.text if journal_el is not None else ""

    year_el = article.find(".//PubDate/Year")
    year = int(year_el.text) if year_el is not None else None

    volume_el = article.find(".//Volume")
    volume = volume_el.text if volume_el is not None else ""

    issue_el = article.find(".//Issue")
    issue = issue_el.text if issue_el is not None else ""

    pages_el = article.find(".//MedlinePgn")
    pages = pages_el.text if pages_el is not None else ""

    # Try to find DOI
    doi = ""
    for eid in root.findall(".//ArticleId"):
        if eid.get("IdType") == "doi":
            doi = eid.text
            break

    abstract_el = article.find(".//AbstractText")
    abstract = abstract_el.text[:500] if abstract_el is not None and abstract_el.text else ""

    return {
        "source": "pubmed",
        "pmid": str(pmid),
        "doi": doi,
        "title": title,
        "authors": authors,
        "year": year,
        "journal": journal,
        "volume": volume,
        "issue": issue,
        "pages": pages,
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        "abstract": abstract
    }


def from_arxiv(arxiv_id):
    """Extract metadata from arXiv ID via arXiv API."""
    arxiv_id = arxiv_id.strip().replace("https://arxiv.org/abs/", "")
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    raw = fetch_url(url, accept="application/xml")
    if not raw:
        return None

    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        print("ERROR: Failed to parse arXiv XML", file=sys.stderr)
        return None

    entry = root.find("atom:entry", ns)
    if entry is None:
        return None

    title = entry.find("atom:title", ns)
    title = title.text.strip().replace("\n", " ") if title is not None else ""

    authors = []
    for author in entry.findall("atom:author", ns):
        name = author.find("atom:name", ns)
        if name is not None:
            parts = name.text.strip().rsplit(" ", 1)
            if len(parts) == 2:
                authors.append({"given": parts[0], "family": parts[1]})
            else:
                authors.append({"given": "", "family": parts[0]})

    published = entry.find("atom:published", ns)
    year = int(published.text[:4]) if published is not None else None

    summary = entry.find("atom:summary", ns)
    abstract = summary.text.strip()[:500] if summary is not None and summary.text else ""

    # Check for DOI link
    doi = ""
    for link in entry.findall("atom:link", ns):
        if link.get("title") == "doi":
            doi = link.get("href", "").replace("http://dx.doi.org/", "")

    return {
        "source": "arxiv",
        "arxiv_id": arxiv_id,
        "doi": doi,
        "title": title,
        "authors": authors,
        "year": year,
        "journal": "arXiv preprint",
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "abstract": abstract
    }


def format_readable(meta):
    """Format metadata as readable citation."""
    if not meta:
        return "No metadata found."

    authors = meta.get("authors", [])
    if len(authors) <= 2:
        author_str = " & ".join(f"{a['family']}, {a['given']}" for a in authors)
    else:
        author_str = f"{authors[0]['family']}, {authors[0]['given']} et al."

    year = meta.get("year", "n.d.")
    title = meta.get("title", "")
    journal = meta.get("journal", "")
    volume = meta.get("volume", "")
    pages = meta.get("pages", "")
    url = meta.get("url", "")

    parts = [f"{author_str} ({year})."]
    parts.append(f'"{title}."')
    if journal:
        extras = []
        if volume:
            extras.append(volume)
        if pages:
            extras.append(pages)
        extra_str = ", ".join(extras)
        parts.append(f"*{journal}*" + (f", {extra_str}." if extra_str else "."))
    if url:
        parts.append(f"[Link]({url})")

    return " ".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Extract metadata from DOI/PMID/arXiv")
    parser.add_argument("identifier", nargs="?", help="DOI (default identifier type)")
    parser.add_argument("--pmid", help="PubMed ID")
    parser.add_argument("--arxiv", help="arXiv ID")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON (default: readable)")
    args = parser.parse_args()

    meta = None
    if args.pmid:
        meta = from_pmid(args.pmid)
    elif args.arxiv:
        meta = from_arxiv(args.arxiv)
    elif args.identifier:
        meta = from_doi(args.identifier)
    else:
        parser.print_help()
        sys.exit(1)

    if not meta:
        print("ERROR: Could not extract metadata.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(meta, indent=2))
    else:
        print(format_readable(meta))
        if meta.get("doi"):
            print(f"\nDOI: https://doi.org/{meta['doi']}")
        if meta.get("abstract"):
            print(f"\nAbstract: {meta['abstract']}...")


if __name__ == "__main__":
    main()
