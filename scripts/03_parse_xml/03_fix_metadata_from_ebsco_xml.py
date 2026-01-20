"""
Project: Theory Discourse Analysis

Reconstruct missing article metadata by matching records in a CSV
to an exported EBSCO XML file using DOI and/or title matching.

Purpose:
- Fill in missing publication dates, titles, and author lists
- Support corpus documentation when source metadata is incomplete

Inputs:
- CSV file with partial article metadata (e.g., DOI, title)
- EBSCO XML export containing full bibliographic records

Outputs:
- CSV file with reconstructed metadata fields populated where matches are found

Notes:
- Matching is heuristic (substring-based DOI/title matching)
- Assumes EBSCO XML structure used by standard exports
- Intended for corpus preparation, not authoritative bibliographic correction
"""


import pandas as pd
from lxml import etree
import argparse

parser = argparse.ArgumentParser(
    description="Reconstruct missing article metadata from EBSCO XML records"
)

parser.add_argument("--input_csv", type=str, required=True,
                    help="CSV file with article metadata (e.g., filenames, DOIs, titles)")
parser.add_argument("--ebsco_xml", type=str, required=True,
                    help="EBSCO XML file containing full metadata records")
parser.add_argument("--output_csv", type=str, required=True,
                    help="Output CSV with reconstructed metadata")


def get_infos_by_doi(root, doi):
    # Optional helper; safe because root is passed in
    doi_el = root.find(f".//ui[.='{doi}']")
    return doi_el


if __name__ == "__main__":
    args = parser.parse_args()

    print("Running metadata reconstruction with:")
    print(f"  Input CSV:   {args.input_csv}")
    print(f"  EBSCO XML:   {args.ebsco_xml}")
    print(f"  Output CSV:  {args.output_csv}")

    df = pd.read_csv(args.input_csv)
    tree = etree.parse(args.ebsco_xml)
    root = tree.getroot()

    if "date" not in df.columns:
        df["date"] = ""
    if "authors" not in df.columns:
        df["authors"] = ""

    missing_matches = 0

    for i, row in df.iterrows():
        doi = str(row.get("DOI", "")).lower()

        doiEle = root.xpath(
            f'.//ui[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{doi}")]'
        )
        doiEle = doiEle[0] if len(doiEle) == 1 else None

        title = str(row.get("title", "")).lower().replace('"', '')
        titleEle = root.xpath(
            f'.//btl[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{title}")]'
        )
        titleEle = titleEle[0] if len(titleEle) == 1 else None

        if doiEle is not None:
            control_info = doiEle.getparent().getparent()
        elif titleEle is not None:
            control_info = titleEle.getparent().getparent()
        else:
            missing_matches += 1
            continue

        title_el = control_info.find('.//atl')
        df.at[i, 'title'] = title_el.text if title_el is not None and title_el.text else df.at[i, 'title']

        author_els = control_info.findall('.//au')
        authors = [a.text for a in author_els if a is not None and a.text]
        if authors:
            df.at[i, 'authors'] = ', \n'.join(authors)

        dt_el = control_info.find('.//dt')
        if dt_el is not None and isinstance(dt_el.attrib, dict):
            year = dt_el.attrib.get("year")
            month = dt_el.attrib.get("month")
            day = dt_el.attrib.get("day")
            if year and month and day:
                df.at[i, 'date'] = f"{year}-{month}-{day}"

    print(f"Unmatched rows: {missing_matches}")
    df.to_csv(args.output_csv, index=False)
