# IJRPO — International Journal Research Paper Organization

Website for [ijrpo.in](https://ijrpo.in). ISSN 2356-1068 (Online).

## Layout

| Path | What it is |
|---|---|
| `site/` | The live website (static HTML/CSS). This folder is what gets deployed. |
| `site/pdf/` | Published paper PDFs. |
| `site/papers.json` | Issue details and paper metadata (titles, authors, abstracts, pages). |
| `build.py` | Generates every HTML page in `site/` from the templates inside it and `papers.json`. |
| `papers/` | LaTeX sources for the paper PDFs in IJRPO journal format. |
| `netlify.toml` | Tells Netlify to publish the `site/` folder. |

## Updating

```bash
python3 papers/build_papers.py   # re-typeset paper PDFs (needs pdflatex), updates page numbers
python3 build.py                 # regenerate the website pages
```

Then commit and push; Netlify redeploys automatically when the repo is connected.

## Deploying on Netlify

Add new site → Import from Git → pick this repo. Publish directory is read from `netlify.toml` (`site`). Then add the custom domain `ijrpo.in` under Domain management.
