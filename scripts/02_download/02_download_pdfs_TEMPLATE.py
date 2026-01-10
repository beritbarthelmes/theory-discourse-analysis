"""
Project: Theory Discourse Analysis
Template for full-text acquisition: given a list of DOIs, obtain PDFs via lawful access routes.
This public repository does not include automated downloading of copyrighted PDFs.
"""

from pathlib import Path
from typing import Iterable

def download_pdfs_from_dois(dois: Iterable[str], out_dir: str) -> None:
    """
    Given DOIs and an output directory, save PDFs as <doi_sanitized>.pdf.

    Implement this using lawful access routes (publisher APIs, OpenAthens/Library links,
    Unpaywall, institutional access, or manually downloaded PDFs).
    """
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    raise NotImplementedError("Implement PDF acquisition via lawful access routes.")
