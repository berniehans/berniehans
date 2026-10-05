# Updating the professional profile

`profile.json` is the editable source for professional facts: experience, education, skills, links and project summaries. Public profile and career pages are derived from it.

1. Update the relevant facts in `profile.json`.
2. Run `python scripts/render_profile.py` (Python standard library only).
3. Review and commit `profile.json`, the generated Markdown pages and the generated SVG assets together.

Generated pages: `README.md`, `README.es.md`, `CAREER.md`, `CAREER.es.md`.

The original CV PDF is not part of this repository. Updating these pages does not change the original PDF or LinkedIn. Professional content is adapted from the CV supplied on 2026-10-05; project descriptions and demo links are grounded in their repositories.

Keep education status explicit: the UNI AI master's coursework is complete and the thesis is pending. Do not label it as an awarded MSc without an updated source.

Animated assets use SVG/CSS, include alternative text, and respect reduced-motion preferences. Demo images remain in their original project repositories; update preview URLs in `profile.json` if those assets move.
