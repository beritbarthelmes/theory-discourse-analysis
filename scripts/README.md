# Scripts

This directory contains the analysis pipeline for the *Theory Discourse Analysis* project.
Scripts are organized sequentially to reflect the workflow from literature retrieval to
analysis and visualization.

Each subdirectory corresponds to one processing stage. Scripts are designed to be run
locally and may require non-public data, API keys, or licensed databases.

---

## Directory Structure

- `01_search/`  
  Query construction and literature retrieval metadata (e.g., PubMed, EBSCO exports).

- `02_download/` *(not included in public version)*  
  Helpers for downloading full texts (e.g., PDFs).  
  Omitted from the public repository due to copyright restrictions.

- `03_parse_xml/`  
  XML parsing and metadata reconstruction (e.g., fixing missing fields from EBSCO XML).

- `04_relevance_filter/`  
  Automated relevance screening using GPT-based classification.

- `05_extract_text/`  
  Extraction of article text and paragraph-level units from XML.

- `06_stance_classification/`  
  Paragraph-level stance classification and aggregation to article-level labels.

- `07_visualization/`  
  Statistical summaries and visualizations of discourse trends.

- `notebooks/`  
  Exploratory and legacy notebooks used during development.  
  These are not required for reproducing the main pipeline.

---

## Notes on Reproducibility

- Scripts assume local directory paths as documented in the main `README.md`
- Outputs are written to `outputs/` and are not version-controlled
- API-dependent steps (e.g., GPT-based classification) require user-provided credentials
- Full texts and PDFs are intentionally excluded from the public repository

For details on variables, coding schemes, and analytic decisions, see the manuscript
and the documentation in `manifests/`.
