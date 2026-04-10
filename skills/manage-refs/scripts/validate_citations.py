#!/usr/bin/env python3
"""
validate_citations.py — Validate a BibTeX refs.bib file.

Usage:
    python3 validate_citations.py refs.bib                 # Basic validation
    python3 validate_citations.py refs.bib --check-dois    # + DOI resolution check
    python3 validate_citations.py refs.bib --check-dois --verbose

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


# Set CROSSREF_EMAIL env var to your address for CrossRef's polite pool.
_email = os.environ.get("CROSSREF_EMAIL", "lulab-research-skills@example.com")
USER_AGENT = f"CitationManager/1.0 (mailto:{_email})"


def parse_bibtex(filepath):
    """Simple BibTeX parser. Returns list of entries as dicts."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    entries = []
    # Match @type{key, ... }
    pattern = re.compile(r'@(\w+)\s*\{([^,]+),\s*(.*?)\n\}', re.DOTALL)
    for match in pattern.finditer(text):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        body = match.group(3)

        fields = {}
        # Match field = {value} or field = "value"
        field_pattern = re.compile(r'(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}')
        for fm in field_pattern.finditer(body):
            fields[fm.group(1).lower()] = fm.group(2).strip()

        entries.append({
            "type": entry_type,
            "key": key,
            "fields": fields
        })

    return entries


def check_doi_resolves(doi):
    """Check if a DOI resolves via CrossRef. Returns (ok, title_or_error)."""
    doi = doi.strip()
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}"
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("status") == "ok":
                title = data["message"].get("title", [""])[0] if data["message"].get("title") else ""
                return True, title
            return False, "status != ok"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, str(e.reason)
    except Exception as e:
        return False, str(e)


def validate(filepath, check_dois=False, verbose=False):
    """Validate BibTeX file. Returns (n_pass, n_fail, n_warn, results)."""
    entries = parse_bibtex(filepath)
    if not entries:
        print(f"WARNING: No BibTeX entries found in {filepath}")
        return 0, 0, 1, []

    required_fields = {"author", "title", "year"}
    recommended_fields = {"doi", "url"}

    results = []
    n_pass = 0
    n_fail = 0
    n_warn = 0

    for entry in entries:
        key = entry["key"]
        fields = entry["fields"]
        issues = []
        warnings = []

        # Check required fields
        for rf in required_fields:
            if rf not in fields or not fields[rf]:
                issues.append(f"missing required field: {rf}")

        # Check recommended fields
        for rf in recommended_fields:
            if rf not in fields or not fields[rf]:
                warnings.append(f"missing recommended field: {rf}")

        # Check DOI resolves
        doi_status = None
        if check_dois and "doi" in fields and fields["doi"]:
            ok, detail = check_doi_resolves(fields["doi"])
            if ok:
                doi_status = f"PASS (resolves to: {detail[:60]})"
            else:
                issues.append(f"DOI resolution FAILED: {detail}")
                doi_status = f"FAIL ({detail})"

        # Verdict
        if issues:
            status = "FAIL"
            n_fail += 1
        elif warnings:
            status = "WARN"
            n_warn += 1
        else:
            status = "PASS"
            n_pass += 1

        result = {
            "key": key,
            "status": status,
            "issues": issues,
            "warnings": warnings,
            "doi_status": doi_status
        }
        results.append(result)

        # Print
        if verbose or status != "PASS":
            icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}[status]
            print(f"{icon} {key}: {status}")
            for iss in issues:
                print(f"     ❌ {iss}")
            for w in warnings:
                print(f"     ⚠️  {w}")
            if doi_status and verbose:
                print(f"     DOI: {doi_status}")
        elif verbose:
            print(f"✅ {key}: PASS")

    return n_pass, n_fail, n_warn, results


def main():
    parser = argparse.ArgumentParser(description="Validate BibTeX refs.bib")
    parser.add_argument("bibfile", help="Path to .bib file")
    parser.add_argument("--check-dois", action="store_true", help="Verify each DOI resolves via CrossRef")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all entries, not just failures")
    args = parser.parse_args()

    print(f"Validating: {args.bibfile}")
    if args.check_dois:
        print("DOI resolution check: ENABLED (this may take a moment)")
    print("=" * 60)

    n_pass, n_fail, n_warn, results = validate(args.bibfile, args.check_dois, args.verbose)

    print("=" * 60)
    print(f"Results: {n_pass} PASS | {n_warn} WARN | {n_fail} FAIL | {len(results)} total")

    if n_fail > 0:
        print("\n❌ VALIDATION FAILED — fix issues before proceeding")
        sys.exit(1)
    elif n_warn > 0:
        print("\n⚠️  VALIDATION PASSED WITH WARNINGS")
        sys.exit(0)
    else:
        print("\n✅ ALL ENTRIES VALID")
        sys.exit(0)


if __name__ == "__main__":
    main()
