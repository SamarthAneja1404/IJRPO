"""Typesets IJRPO papers (LaTeX) from site/papers.json + <key>_body.tex, sets continuous
page numbers, and writes PDFs into site/pdf/. Run: python3 build_papers.py"""
import json, os, subprocess, shutil, re
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "site")
DATA_P = os.path.join(SITE, "papers.json")
data = json.load(open(DATA_P, encoding="utf-8"))
J = data["journal"]
tmpl = open(os.path.join(HERE, "ijrpo-paper.tex.in"), encoding="utf-8").read()

def tex(s):
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"), ("_", r"\_")]:
        s = s.replace(a, b)
    s = s.replace("—", "---").replace("–", "--").replace("×", r"$\times$")
    s = re.sub(r'"([^"]*)"', r"``\1''", s)
    return s

os.makedirs(os.path.join(SITE, "pdf"), exist_ok=True)
page = 1
for p in data["papers"]:
    if not p.get("live"):
        continue
    authors = ", ".join(p["authors"])
    first = page
    # two passes: first to learn page count, then final with correct LastPage
    cite_short = f'{authors}, IJRPO, Vol. {J["volume"]}, Issue {J["issue"]}, {J["month_year"]}'
    url = f'https://ijrpo.in/{p["slug"]}.html'
    t = (tmpl.replace("@@TITLE_PLAIN@@", p["title"]).replace("@@AUTHORS_PLAIN@@", authors)
         .replace("@@KEYWORDS_PLAIN@@", ", ".join(p["keywords"]))
         .replace("@@MONTH@@", J["month_year"]).replace("@@FIRSTPAGE@@", str(first))
         .replace("@@SHORTCITE@@", tex(cite_short))
         .replace("@@TYPE@@", p["type"]).replace("@@PAPERID@@", p["id"])
         .replace("@@TITLE@@", p["title_tex"])
         .replace("@@AUTHORS@@", p.get("authors_tex") or tex(authors))
         .replace("@@AFFIL@@", r"\\".join(p["affiliation_lines_tex"]) if p.get("affiliation_lines_tex") else r"\\".join(tex(a) for a in p["affiliation_lines"]))
         .replace("@@PUBDATE@@", p["published"]).replace("@@URL@@", url)
         .replace("@@ABSTRACT@@", tex(p["abstract"]))
         .replace("@@KEYWORDS@@", tex("; ".join(p["keywords"])))
         .replace("@@BODY@@", open(os.path.join(HERE, p["key"] + "_body.tex"), encoding="utf-8").read()))
    cite = (f'{tex(authors)}, ``{tex(p["title"])},\'\' \\textit{{International Journal Research Paper Organization (IJRPO)}}, '
            f'vol.~{J["volume"]}, no.~{J["issue"]}, pp.~{first}--\\pageref*{{LastPage}}, {J["month_year"]}.')
    t = t.replace("@@CITE@@", cite)
    name = p["id"]
    open(os.path.join(HERE, name + ".tex"), "w", encoding="utf-8").write(t)
    for _ in range(2):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", name + ".tex"],
                           cwd=HERE, capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-3000:]); raise SystemExit("LaTeX failed for " + name)
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", name + ".pdf"], cwd=HERE, capture_output=True, text=True).stdout).group(1))
    last = first + n - 1
    p["pages"] = f"{first}-{last}"
    p["pdf"] = f"pdf/{name}.pdf"
    shutil.copy(os.path.join(HERE, name + ".pdf"), os.path.join(SITE, "pdf", name + ".pdf"))
    print(f"{name}: pages {first}-{last}")
    page = last + 1

json.dump(data, open(DATA_P, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
