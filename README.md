# Quantifying Knowledge Accumulation in Scientific Psychology  
Master’s Thesis — University of Zurich (2024)  
Authors: Berit T. Barthelmes & Vencislav Popov

A semi-automated, transparent pipeline for examining how psychological theories are discussed in the scientific literature.  
Note: This pipeline analyzes discourse patterns, not theoretical correctness.

---

## Overview

This repository provides a semi-automated workflow for collecting, processing, and analyzing scientific articles related to a user-defined theoretical construct. It combines structured search procedures, automated PDF processing, and large-language-model–based classification to support exploratory metascientific work.

The goal is methodological: to make theoretical discourse more transparent, traceable, and analyzable at scale.

---

## Pipeline Components

1) Literature Search  
   Retrieve scientific articles using a theory or concept query.

2) Full-Text Access and Download  
   Fetch PDFs and associated metadata where accessible.

3) PDF → XML Conversion  
   Convert PDFs to structured XML using GROBID.

4) Relevance Filtering  
   Screen articles for conceptual relevance (automated plus optional manual verification).

5) Text Extraction  
   Extract each article’s abstract and the three paragraphs most relevant to the query, identified via cosine similarity.

6) Stance Classification (GPT-4 Assisted)  
   Classify abstracts and paragraphs into:  
   - support  
   - opposition  
   - tacit acceptance  
   - ambiguous  
   using GPT-4 with low temperature settings for consistency.

7) Visualization  
   Plot distributions of stance categories and their changes over time.

---

## Detailed Component Descriptions

### 1. Literature Search  
Automated retrieval of scientific articles using a user-defined theoretical construct.  
Compatible with multi-source querying (e.g., Entrez, Crossref, EBSCOhost).

### 2. Full-Text Access and Download  
Fetches PDFs and metadata when available. Full access may require institutional credentials.

### 3. PDF → XML Conversion  
Uses GROBID to produce consistent XML output with extracted text, metadata, and document structure.

### 4. Relevance Filtering  
Performs automated filtering to exclude articles not conceptually related to the target theory.  
Manual review can be added for higher precision.

### 5. Text Extraction  
Extracts both the abstract and three paragraphs most closely related to the theory based on cosine similarity scores.

### 6. Stance Classification (GPT-4 Assisted)  
Assigns stance labels to abstract and paragraph text according to predefined categories.  
Classifications are performed using GPT-4 at low temperature to increase reproducibility.

### 7. Visualization  
Generates plots characterizing stance distributions across time, supporting exploratory analysis of theoretical convergence, disagreement, or fragmentation.

---

## Installation

Clone the repository and move into it:

git clone https://github.com/your-repo/theory-discourse-pipeline.git  
cd theory-discourse-pipeline

Install Python dependencies:

pip install -r requirements.txt

Install and launch GROBID (required for PDF-to-XML conversion):

./gradlew clean install  
./gradlew run

---

## Recommended Folder Structure

project/  
│  
├── data_raw/               (raw PDFs)  
├── data_xml/               (XML output from GROBID)  
├── data_processed/         (extracted abstracts and paragraphs)  
│  
├── scripts/  
│   ├── 01_search.py  
│   ├── 02_download.py  
│   ├── 03_pdf_to_xml.py  
│   ├── 04_relevance_filter.py  
│   ├── 05_extract_text.py  
│   ├── 06_gpt_classify.py  
│   └── 07_visualize.py  
│  
├── outputs/  
│   ├── stance_plots/  
│   └── classified_articles.csv  
│  
└── README.md

---

## Quickstart

Run the full pipeline:

python run_pipeline.py --query "memory decay theory" --gpt_model gpt-4 --temperature 0.3

Generate visualizations:

python scripts/07_visualize.py

---

## Example Outputs

1. Stance distribution line plots showing proportions of supportive, opposing, tacit acceptance, and ambiguous articles over time.  
2. Counts of theory-relevant articles per decade.  
3. Agreement metrics comparing GPT-4 classifications with expert ratings (e.g., Cohen’s kappa).

---

## Intended Use

This pipeline is designed for:

- examining theoretical discourse across large scientific corpora,  
- identifying patterns of support, opposition, and tacit acceptance,  
- supporting metascientific analyses of theory development,  
- enabling reproducible and transparent processing of large bodies of text.

It is theory-agnostic and adaptable to any conceptual query.

---

## Notes and Limitations

- GPT-4 classifications should be validated against expert judgments when possible.  
- PDF access varies by publisher and may require institutional credentials.  
- Cosine similarity extraction may overlook highly conceptual but low-frequency theoretical passages.  
- Outputs reflect discourse patterns, not empirical accuracy or theoretical correctness.

