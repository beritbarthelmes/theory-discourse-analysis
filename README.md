# Assessing Psychology’s Theory Crisis: A Disourse-Based Analysis
**Berit T. Barthelmes & Vencislav Popov**

This project examines how scientific articles position themselves with respect to a target theory, focusing on patterns in theoretical discourse rather than on assessing theoretical correctness.

---

## Project Overview

This repository contains a workflow for collecting, processing, and analyzing scientific articles
related to a user-defined theoretical construct. The pipeline transforms patterns of theoretical
engagement in the literature into structured data, enabling exploratory analyses of theory reception
and change over time.

The project is **explicitly exploratory**. As a proof of concept, the pipeline is applied to the
literature on **memory decay theory**, tracking how articles:

- argue *for* the theory,
- argue *against* the theory,
- rely on the theory without explicit justification (*tacit acceptance*), or
- mention the theory without clear commitment.

The goal is not to adjudicate the theory, but to demonstrate how discourse-based patterns of
theoretical engagement can be extracted, categorized, and analyzed over time.

---

## Repository Structure

```text
.
├── scripts/        # Stepwise analysis pipeline
├── data_raw/       # Local PDFs (not version-controlled)
├── data_xml/       # XML representations of articles (e.g., GROBID output)
├── manifests/      # Article-level corpus documentation
├── outputs/        # Generated results (not version-controlled)
├── .gitignore
└── README.md

```

## Directory Description

- **scripts/**  
  Stepwise analysis pipeline (search, XML parsing, metadata reconstruction, relevance screening,
  stance classification, visualization). Each subdirectory contains a README describing its role.

- **data_raw/**  
  Intended for local storage of PDF files.  
  Empty in the public repository due to copyright restrictions.

- **data_xml/**  
  Structured XML representations of articles (e.g., GROBID output).  
  Only directory structure and documentation are included publicly.

- **manifests/**  
  Curated, article-level documentation of the analytic corpus  
  (e.g., `memory_decay_corpus.xlsx`). Contains metadata and expert coding variables
  without full texts or substantial excerpts.

- **outputs/**  
  Analysis outputs (tables, figures) generated locally and not version-controlled.

---

## Data Availability and Reproducibility

Due to copyright restrictions, this repository prioritizes transparent documentation over redistribution of source materials.

- Full-text articles and PDFs are not included in this repository.
- Article-level metadata and expert coding decisions are documented in `manifests/`.
- Automated classification steps require user-provided API credentials.
- Scripts assume local paths as documented in subdirectory READMEs.

---

## Notes

- Outputs characterize how theories are discussed, not their empirical validity.
- Automated classifications should be interpreted cautiously and, where possible,
  validated against expert judgments.
- This repository serves as a methodological proof of concept for discourse-based
  analyses of theory reception in psychology.
