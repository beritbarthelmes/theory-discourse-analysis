"""
Project: Theory Discourse Analysis

Identify and remove duplicate article XML files based on embedded MD5 identifiers
in TEI-encoded full-text documents.

Purpose:
- Detect duplicate articles produced during bulk XML ingestion (e.g., via GROBID or EBSCO exports)
- Ensure one-to-one correspondence between XML files and articles in the analytic corpus

Inputs:
- Directory containing TEI XML files with <idno type="MD5"> identifiers

Outputs:
- Duplicate XML files are deleted in-place from the input directory

Notes:
- Deduplication relies on the presence and correctness of MD5 identifiers in TEI headers
- Intended as a preprocessing step prior to text extraction and stance classification
"""


import xml.etree.ElementTree as ET
import os
from tqdm import tqdm

# assign directory
# adapt directories to your needs
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_dir", required=True, help="Directory containing TEI XML files")
args = parser.parse_args()
articles_directory = args.input_dir

def filter_duplicate_articles(directory):
  i = 0
  files = os.listdir(directory)
  seen = set()
  duplicate_files = []

  # iterate over files in that directory
  for filename in tqdm(files):
    if filename.endswith(".xml"):
      # print(directory, filename)
      file = os.path.join(directory, filename)
      # checking if it is a file
      tree = ET.parse(file)
      root = tree.getroot()
      # MD5 hash used as content-based article identifier
      article_hash = root.find(".//{http://www.tei-c.org/ns/1.0}idno[@type='MD5']").text
      i += 1
      if article_hash not in seen:
        seen.add(article_hash)
      else:
        duplicate_files.append(filename)

  print("Total files: ", i)
  print("Duplicate files: ", len(duplicate_files))
  return duplicate_files

def remove_duplicate_articles(duplicates):
  for duplicate in duplicates:
    os.remove(os.path.join(articles_directory, duplicate))

duplicates = filter_duplicate_articles(articles_directory)
remove_duplicate_articles(duplicates)

