# Memory Decay Corpus

This file documents the analytic corpus used in the memory decay case study in the *Theory Discourse Analysis* project.

The corpus contains article-level metadata and expert coding variables for all articles included in the final analysis. It is intended to support transparency and reproducibility while respecting copyright restrictions. No full texts or substantial excerpts are included.

---

## Corpus Description

The corpus comprises peer-reviewed scientific articles that engage substantively with memory decay theory in human memory research. Articles were retrieved via EBSCOhost and processed as XML. All filtering, deduplication, relevance screening, and coding were performed on this corpus.

The goal is to document how memory decay theory is positioned in the literature, not to assess its empirical validity.

---

## Variables

Each row corresponds to one article. The dataset includes:

- `filename`: Internal article identifier  
- `title`: Article title  
- `DOI`: Digital Object Identifier  
- `date`: Publication date  
- `authors`: Article authors  
- `article_type`: Empirical (1), Review (2), Theoretical/Modeling (3)  
- `research_type`: Basic (0), Applied (1)  
- `expert1_categorization`: Expert-coded stance toward memory decay theory  
- `interaction_decay_interference`: No (0), Yes (1)  
- `new_theory_proposed`: No (0), Yes (1)  

---

## Notes

Only final categorical labels are included. Detailed coding rationales and full-text materials are retained privately and described in the accompanying manuscript.

This dataset is provided as a proof of concept for discourse-based analyses of theory reception.

