# Evaluate the Role, Not the Model

Draft manuscript for *ACM Transactions on Human-Robot Interaction* (THRI):
best practices for evaluating language, vision, and action models in HRI.

## Files

- `main.tex` — entry point (`acmart`, `manuscript,screen,review` options).
- `sections/` — one file per section; `fig_architecture.tex` is the TikZ figure.
- `references.bib` — only the entries cited in the text.
- `supplementary/precision_planning.py` — reproduces the two appendix tables
  (`pip install numpy scipy`, then `python3 supplementary/precision_planning.py`).
- `main.pdf` — compiled manuscript.

## Build

    latexmk -pdf main.tex

Requires a TeX distribution with `acmart` (TeX Live: `texlive-publishers`,
`texlive-latex-extra`, `texlive-fonts-extra`, `texlive-pictures`).

## Before submission

1. **Authors and acknowledgements.** Only one author is listed; add
   co-authors, the corresponding e-mail address, funding, and the
   generative-AI disclosure that ACM's authorship policy requires (the red
   note in the Acknowledgments marks the place).
2. **Article type and length.** The body is about 24,000 words. Confirm the
   intended THRI article type and trim if needed; Sections 5 and 6 are the
   easiest to shorten.
3. **Descriptions of your own studies.** Section 7 and parts of Sections 4-6
   describe what the RO-MAN 2025/2026 papers, the therapy-alignment preprint,
   DialogGuard, SPASM and the child wellbeing study did and did not report.
   These were written from the published texts and should be checked by the
   authors of those studies.
4. **Sources read only at abstract level.** Bibliographic details of every
   reference were checked against a primary record (publisher DOI metadata,
   ACL Anthology, PMLR, OpenReview or arXiv). For some references only the
   abstract was accessible, so statements about them are limited to what the
   abstract says. In particular: the item list of Matuszek et al. (2026) was
   not readable; Krippendorff's .800/.667 guidance was confirmed through
   secondary quotation, not the 4th-edition page; and Ollion et al. (2024),
   Palmer et al. (2024), Harding et al. (2024) and Skantze (2021) are cited
   for their general position only.
5. **Preprints.** A number of 2025-2026 references are arXiv preprints
   (marked as such in `references.bib`); check for published versions.
6. **Recommended defaults.** The numerical defaults in the text (five runs,
   thirty trials, 200 double-coded items) are reasoned from the appendix
   tables and are proposals, not established thresholds.
