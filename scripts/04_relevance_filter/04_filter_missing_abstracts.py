"""
Project: Theory Discourse Analysis

Remove article XML files that lack an abstract as part of corpus quality control.

Purpose:
- Enforce a minimum metadata/content standard for inclusion in the analytic corpus
- Exclude articles without abstracts, which cannot be reliably screened or classified

Inputs:
- Directory containing TEI XML files

Outputs:
- XML files without <abstract> elements are deleted in-place from the input directory

Notes:
- Assumes TEI-compliant XML structure with namespace http://www.tei-c.org/ns/1.0
- Intended as an early preprocessing step prior to relevance screening and text extraction
"""


import xml.etree.ElementTree as ET
import os

# assign directory
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_dir", required=True, help="Directory containing TEI XML files")
args = parser.parse_args()
articles_directory = args.input_dir

no_abstract_files = []
files = os.listdir(articles_directory)

# iterate over files in that directory
for filename in files:
  if filename.endswith(".xml"):
    # print(directory, filename)
    file = os.path.join(articles_directory, filename)
    # checking if it is a file
    tree = ET.parse(file)
    root = tree.getroot()
    abstract = root.find(".//{http://www.tei-c.org/ns/1.0}abstract")

    if abstract is None or abstract.text is None:
      no_abstract_files.append(filename)

for file in no_abstract_files:
    os.remove(os.path.join(articles_directory, file))
