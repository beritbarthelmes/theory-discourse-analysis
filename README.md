# Assessing Psychology’s Theory Crisis: A Discourse-Based Analysis
**Berit T. Barthelmes & Vencislav Popov**

**A pipeline for analyzing how scientific articles position themselves with respect to a target theory.**  
*The analysis concerns discourse patterns, not theoretical correctness.*

---

## Project overview

This repository contains a workflow for collecting, processing, and analyzing scientific articles related to a user-defined theoretical construct. The pipeline turns patterns of theoretical engagement in the literature into structured data, enabling exploratory analyses of theory reception and change over time.

The project is **explicitly exploratory**. As a proof of concept, the pipeline is applied to the literature on the **memory decay theory**, tracking how papers argue for the theory, argue against it, rely on it without additional justification, or mention it without clear commitment. The goal is not to adjudicate the theory, but to demonstrate how patterns of theoretical engagement can be extracted and examined over time.

---

## Repository overview

- `scripts/` – stepwise pipeline scripts (search, download, parsing, filtering, classification, visualization)  
- `data_raw/` – raw PDFs  
- `data_xml/` – structured XML files (GROBID output)  
- `data_processed/` – extracted abstracts and paragraphs  
- `outputs/` – plots and summary tables  

---

## Get started

### Install

```bash
git clone https://github.com/your-repo/theory-discourse-pipeline.git
cd theory-discourse-pipeline
pip install -r requirements.txt
```

### Run GROBID (required for PDF → XML conversion)

```bash
./gradlew clean install
./gradlew run
```

### Run the pipeline

```bash
python run_pipeline.py --query "memory decay theory" --gpt_model gpt-4 --temperature 0.3
```

### Generate visualizations

```bash
python scripts/07_visualize.py
```

---

## Notes

- Outputs characterize article-level stances toward a theory, not its empirical or theoretical validity.
- Automated classifications should be validated against expert judgments when possible.
