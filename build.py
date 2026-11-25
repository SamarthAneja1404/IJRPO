"""Builds the IJRPO static website into ./site from templates below + site/papers.json.
Run:  python3 build.py
"""
import json, re, html, os

SITE = os.path.join(os.path.dirname(__file__), "site")
DATA = json.load(open(os.path.join(SITE, "papers.json"), encoding="utf-8"))
J = DATA["journal"]
PAPERS = [x for x in DATA["papers"] if x.get("live")]  # papers set aside until "live": true

NAME = "International Journal Research Paper Organization"
SHORT = "IJRPO"
DOMAIN = "ijrpo.in"
EMAIL = "editor@ijrpo.in"
ISSN = "ISSN: 2356-1068 (Online)"
FREQ = "Monthly"
FEE_IN = "[₹ amount]"
FEE_INT = "[US$ amount]"

def ph(text):
    """Wrap any [bracketed placeholder] in a highlighted span so it is easy to spot and replace."""
    return re.sub(r"\[([^\]]+)\]", lambda m: f'<span class="placeholder">[{m.group(1)}]</span>', text)

def esc(t):
    return html.escape(t, quote=True)

ORBIT = """<svg class="orbit" viewBox="0 0 600 600" aria-hidden="true">
  <circle cx="300" cy="300" r="190" fill="none" stroke="#ffffff" stroke-opacity=".10" stroke-width="2"/>
  <circle cx="300" cy="300" r="250" fill="none" stroke="#ffffff" stroke-opacity=".06" stroke-width="1.5"/>
  <ellipse cx="300" cy="300" rx="285" ry="88" transform="rotate(-18 300 300)" fill="none" stroke="#1f86d2" stroke-width="16" stroke-linecap="round" stroke-dasharray="1300 500"/>
  <ellipse cx="300" cy="300" rx="285" ry="88" transform="rotate(-18 300 300)" fill="none" stroke="#ddf1fe" stroke-opacity=".7" stroke-width="3" stroke-dasharray="900 900"/>
</svg>"""

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("editorial-board.html", "Editorial Board"),
    ("author-guidelines.html", "Author Guidelines"),
    ("current-issue.html", "Current Issue"),
    ("archives.html", "Archives"),
    ("publication-fee.html", "Publication Fee"),
    ("policies.html", "Policies"),
    ("contact.html", "Contact"),
]

def sidebar():
    return f"""<aside class="sidebar">
  <div class="box"><h4>Submit Your Paper</h4><div class="inner">
    <p style="margin-bottom:12px">Send your manuscript for the next issue. Review decision is usually given within 7–10 days.</p>
    <a class="btn accent" href="submit.html" style="width:100%;text-align:center">Submit Manuscript</a>
  </div></div>
  <div class="box"><h4>Journal Information</h4><div class="inner">
    <table class="tbl" style="margin:0;font-size:.9rem"><tbody>
      <tr><td><b>ISSN</b></td><td>2356-1068</td></tr>
      <tr><td><b>Frequency</b></td><td>{FREQ}</td></tr>
      <tr><td><b>Language</b></td><td>English</td></tr>
      <tr><td><b>Mode</b></td><td>Online, Open Access</td></tr>
      <tr><td><b>Started</b></td><td>2026</td></tr>
    </tbody></table>
  </div></div>
  <div class="box"><h4>For Authors</h4><ul>
    <li><a href="author-guidelines.html">Author Guidelines</a></li>
    <li><a href="author-guidelines.html#template">Paper Template</a></li>
    <li><a href="author-guidelines.html#process">Review Process</a></li>
    <li><a href="publication-fee.html">Publication Fee</a></li>
    <li><a href="policies.html#copyright">Copyright &amp; Licence</a></li>
  </ul></div>
  <div class="box"><h4>Call for Papers</h4><div class="inner">
    Volume {J['volume']}, Issue {J['issue'] + 1} — submissions open now.
  </div></div>
</aside>"""

def page(fname, title, body, *, band=True, crumbs=True, side=True, desc=None, extra_head=""):
    nav = "\n".join(
        f'<li><a href="{h}"{" class=\"active\"" if h == fname else ""}>{t}</a></li>' for h, t in NAV)
    desc = desc or f"{NAME} ({SHORT}) — an open-access, peer-reviewed international journal publishing original research across engineering, technology, science, management and humanities."
    band_html = ""
    if band:
        crumb = f'<div class="crumbs"><a href="index.html">Home</a> / {title}</div>' if crumbs else ""
        band_html = f'<div class="page-band">{ORBIT}<div class="wrap">{crumb}<h1>{title}</h1></div></div>'
    main_inner = f'<div class="layout"><div class="content">{body}</div>{sidebar()}</div>' if side else body
    full_title = f"{title} | {SHORT}" if fname != "index.html" else f"{SHORT} — {NAME}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" type="image/png" href="assets/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
{extra_head}
</head>
<body>
<div class="topbar"><div class="wrap">
  <div><span>{ph(ISSN)}</span><span>Open Access · Peer Reviewed · {FREQ}</span></div>
  <div><span>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
</div></div>
<header class="site-header"><div class="wrap">
  <a class="brand" href="index.html"><img src="assets/logo.png" alt="IJRPO — International Journal Research Paper Organization"></a>
  <div class="header-cta">
    <a class="btn" href="author-guidelines.html">Author Guidelines</a>
    <a class="btn primary" href="submit.html">Submit Paper</a>
  </div>
</div></header>
<nav class="nav" id="nav"><div class="wrap">
  <button class="nav-toggle" onclick="document.getElementById('nav').classList.toggle('open')">☰ Menu</button>
  <ul>{nav}</ul>
</div></nav>
{band_html}
<main><div class="wrap">{main_inner}</div></main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <div class="foot-logo"><img src="assets/logo.png" alt="IJRPO"></div>
      <p>{NAME} is an open-access, peer-reviewed journal that publishes original research from students, scholars and professionals.</p>
    </div>
    <div><h4>Journal</h4><ul>
      <li><a href="about.html">About IJRPO</a></li>
      <li><a href="about.html#scope">Aims &amp; Scope</a></li>
      <li><a href="editorial-board.html">Editorial Board</a></li>
      <li><a href="current-issue.html">Current Issue</a></li>
      <li><a href="archives.html">Archives</a></li>
    </ul></div>
    <div><h4>Authors</h4><ul>
      <li><a href="submit.html">Submit Paper</a></li>
      <li><a href="author-guidelines.html">Author Guidelines</a></li>
      <li><a href="publication-fee.html">Publication Fee</a></li>
      <li><a href="policies.html">Ethics &amp; Policies</a></li>
    </ul></div>
    <div><h4>Contact</h4><ul>
      <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><a href="https://{DOMAIN}">www.{DOMAIN}</a></li>
      <li>New Delhi, Delhi, India</li>
    </ul></div>
  </div>
  <div class="copyright">© {J['year']} {NAME} ({SHORT}). Articles are published under the Creative Commons Attribution 4.0 (CC BY 4.0) licence.</div>
</footer>
</body>
</html>"""

def article_item(p):
    pdf = (f'<a class="pdf" href="{p["pdf"]}">Read Full Paper (PDF)</a>' if p["pdf"]
           else '<span>PDF: coming soon</span>')
    return f"""<div class="article-item">
  <div class="type">{p['type']} · {p['id']}</div>
  <h3><a href="{p['slug']}.html">{esc(p['title'])}</a></h3>
  <div class="authors">{esc(', '.join(p['authors']))}</div>
  <div class="meta"><span>Vol. {J['volume']}, Issue {J['issue']} ({J['month_year']})</span><span>Pages {p['pages'].replace('-','–')}</span><a href="{p['slug']}.html">View Paper</a>{pdf}</div>
</div>"""

# ---------------- pages ----------------
GOALS = """<section class="goals-sec">
  <h2>Our indexing goals</h2>
  <p>IJRPO is a new journal. We are working toward the indexing listed below and will show each one under Journal Highlights only once it is in place.</p>
  <table class="tbl"><thead><tr><th>Goal</th><th>What it means for authors</th><th>Status</th></tr></thead><tbody>
    <tr><td><b>Google Scholar</b></td><td>Published papers become searchable and citable on Google Scholar.</td><td><span class="goal">Working toward</span></td></tr>
    <tr><td><b>Crossref DOI</b></td><td>Each paper gets a permanent DOI link.</td><td><span class="goal">Working toward</span></td></tr>
    <tr><td><b>DOAJ</b></td><td>Listing in the Directory of Open Access Journals, after a regular publishing record.</td><td><span class="goal">Working toward</span></td></tr>
  </tbody></table>
</section>
"""

pages = {}

articles_html = "\n".join(article_item(p) for p in PAPERS) or (
    '<div class="note">The first issue is being prepared. Accepted papers will appear here as soon as they are published. '
    '<a href="submit.html">Submit your paper</a> to be part of it.</div>')

pages["index.html"] = page("index.html", "Home", f"""
<div class="layout"><div class="content">
<section>
  <h2>Welcome to IJRPO</h2>
  <p><b>{NAME} ({SHORT})</b> is an open-access, double-blind peer-reviewed, {FREQ.lower()} journal. It publishes original research papers, review articles and case studies in engineering, technology, computer science, applied sciences, management and humanities.</p>
  <p>The journal is meant for students, research scholars, faculty and working professionals who want their work reviewed fairly, published quickly and read freely around the world.</p>
</section>
<section>
  <h2>Why publish with IJRPO</h2>
  <div class="grid-3">
    <div class="card"><div class="ic">1</div><h3>Peer review</h3><p>Every manuscript is checked for plagiarism and reviewed by subject experts before it is accepted.</p></div>
    <div class="card"><div class="ic">2</div><h3>Fast decisions</h3><p>First review decision usually within 7–10 days; accepted papers go online in the next issue.</p></div>
    <div class="card"><div class="ic">3</div><h3>Open access</h3><p>All papers are free to read and download, published under CC BY 4.0.</p></div>
    <div class="card"><div class="ic">4</div><h3>Certificates</h3><p>Every author on a published paper receives an e-certificate of publication.</p></div>
    <div class="card"><div class="ic">5</div><h3>Permanent record</h3><p>Each paper gets its own page, a paper ID and a ready-to-use citation.</p></div>
    <div class="card"><div class="ic">6</div><h3>Many fields</h3><p>Multidisciplinary scope, from AI and data science to commerce and social sciences.</p></div>
  </div>
</section>
<section>
  <h2>Current issue — Vol. {J['volume']}, Issue {J['issue']}</h2>
  {articles_html}
  
</section>
<section>
  <h2>Journal highlights</h2>
  <div class="hl">
    <div class="hl-item"><svg viewBox="0 0 24 24"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/></svg><b>ISSN 2356-1068</b><span>Online</span></div>
    <div class="hl-item"><svg viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 7.5-2"/></svg><b>Open Access</b><span>CC BY 4.0</span></div>
    <div class="hl-item"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5M8.5 11l2 2 3.5-4"/></svg><b>Plagiarism checked</b><span>Below 15% similarity</span></div>
    <div class="hl-item"><svg viewBox="0 0 24 24"><circle cx="8" cy="8" r="3"/><circle cx="16" cy="8" r="3"/><path d="M3 20c0-3 2.5-5 5-5s5 2 5 5M11 20c0-3 2.5-5 5-5s5 2 5 5"/></svg><b>Double-blind review</b><span>At least two reviewers</span></div>
  </div>
</section>
{GOALS}<section>
  <h2>How publishing works</h2>
  <ol class="steps">
    <li><strong>Submit</strong> your manuscript in the IJRPO template through the submission page or by email.</li>
    <li><strong>Review</strong>: plagiarism check and peer review; you receive a decision by email.</li>
    <li><strong>Acceptance</strong>: send the final paper and copyright form, and pay the publication fee.</li>
    <li><strong>Publication</strong>: your paper goes online with its own page, and you receive your certificate.</li>
  </ol>
</section>
</div>{sidebar()}</div>
""", band=False, side=False)

# splice hero in before main for home page
hero = f"""<section class="hero">{ORBIT}<div class="wrap">
  <div>
    <span class="eyebrow">Open Access · Peer Reviewed · {FREQ}</span>
    <h1>{NAME}</h1>
    <p class="lead">Publishing original research from students, scholars and professionals, reviewed fairly and freely available to readers everywhere.</p>
    <div class="actions">
      <a class="btn accent" href="submit.html">Submit Your Paper</a>
      <a class="btn light" href="current-issue.html">Read Current Issue</a>
    </div>
  </div>
  <div class="hero-card">
    <h3>Call for Papers — Vol. {J['volume']}, Issue {J['issue'] + 1}</h3>
    <dl>
      <dt>Journal</dt><dd>{SHORT}</dd>
      <dt>ISSN</dt><dd>2356-1068 (Online)</dd>
      <dt>Frequency</dt><dd>{FREQ}</dd>
      <dt>Review</dt><dd>Double-blind peer review</dd>
      <dt>Decision</dt><dd>Within 7–10 days</dd>
      <dt>Email</dt><dd>{EMAIL}</dd>
    </dl>
  </div>
</div></section>"""
pages["index.html"] = pages["index.html"].replace("<main>", hero + "\n<main>", 1)

pages["about.html"] = page("about.html", "About the Journal", f"""
<section>
  <h2>About IJRPO</h2>
  <p><b>{NAME} ({SHORT})</b> is an international, open-access, peer-reviewed journal published online at <a href="https://{DOMAIN}">{DOMAIN}</a>. It was started in 2026 to give students, early-career researchers and professionals a dependable place to publish original work.</p>
  <p>All papers are free to read. Authors keep copyright, and published work is shared under the Creative Commons Attribution 4.0 licence.</p>
</section>
<section>
  <table class="tbl"><tbody>
    <tr><td><b>Journal title</b></td><td>{NAME}</td></tr>
    <tr><td><b>Abbreviation</b></td><td>{SHORT}</td></tr>
    <tr><td><b>ISSN (Online)</b></td><td>2356-1068</td></tr>
    <tr><td><b>Frequency</b></td><td>{FREQ} (12 issues a year)</td></tr>
    <tr><td><b>Publication mode</b></td><td>Online</td></tr>
    <tr><td><b>Language</b></td><td>English</td></tr>
    <tr><td><b>Review type</b></td><td>Double-blind peer review</td></tr>
    <tr><td><b>Access</b></td><td>Open access, CC BY 4.0</td></tr>
    <tr><td><b>Publisher</b></td><td>{ph("[Publisher name]")}</td></tr>
    <tr><td><b>Editor-in-Chief</b></td><td>Dr. Himesh Shetty</td></tr>
    <tr><td><b>Website</b></td><td>{DOMAIN}</td></tr>
  </tbody></table>
</section>
{GOALS}<section id="aims">
  <h2>Aims</h2>
  <ul>
    <li>Publish original, high-quality research that adds to knowledge in its field.</li>
    <li>Give students and young researchers a fair and quick route to publication.</li>
    <li>Keep every published paper free to read, cite and build on.</li>
    <li>Uphold honest research practice through plagiarism checks and peer review.</li>
  </ul>
</section>
<section id="scope">
  <h2>Scope</h2>
  <p>IJRPO is multidisciplinary. We welcome research papers, review papers, case studies and survey papers in areas including, but not limited to:</p>
  <div class="grid-2">
    <div class="card"><h3>Engineering &amp; Technology</h3><p>Computer science, AI &amp; machine learning, data science, IT, electronics, electrical, mechanical, civil and chemical engineering.</p></div>
    <div class="card"><h3>Applied &amp; Pure Sciences</h3><p>Physics, chemistry, mathematics, biotechnology, environmental science, agriculture.</p></div>
    <div class="card"><h3>Management &amp; Commerce</h3><p>Business management, finance, marketing, HR, economics, entrepreneurship.</p></div>
    <div class="card"><h3>Humanities &amp; Social Sciences</h3><p>Education, psychology, law, sociology, literature, media and public policy.</p></div>
  </div>
</section>
""")

def member(role, name, aff, initials):
    return f"""<div class="card member"><div class="av">{initials}</div><div>
      <div class="role">{role}</div><h3>{ph(name)}</h3>{f"<p>{ph(aff)}</p>" if aff else ""}</div></div>"""

pages["editorial-board.html"] = page("editorial-board.html", "Editorial Board", f"""
<section>
  <h2>Editor-in-Chief</h2>
  <div class="grid-2">{member("Editor-in-Chief", "Dr. Himesh Shetty", "", "HS")}</div>
</section>
<section>
  <h2>Associate Editors</h2>
  <div class="grid-2">
    {member("Associate Editor", "Dr. Manoj Rajwal", "", "MR")}
    {member("Associate Editor", "Dr. Salman Qureshi", "", "SQ")}
  </div>
</section>
<section>
  <h2>Editorial Board Members</h2>
  <div class="grid-2">
    {member("Board Member", "Dr. M. Shima Devi", "", "SD")}
    {member("Board Member", "Dr. Ranbir Singh", "", "RS")}
    {member("Board Member", "Dr. Nagashri J. K.", "", "NJ")}
    {member("Board Member", "Dr. Alia Gaurav", "", "AG")}
  </div>
</section>
<section>
  <h2>Join as a Reviewer</h2>
  <p>We invite faculty members and researchers with a postgraduate degree or above to review for IJRPO. Email your name, designation, institution, subject areas and CV to <a href="mailto:{EMAIL}?subject=Reviewer%20application">{EMAIL}</a>.</p>
</section>
""")

pages["author-guidelines.html"] = page("author-guidelines.html", "Author Guidelines", f"""
<section>
  <h2>Before you submit</h2>
  <ul>
    <li>The paper must be original and not published or under review anywhere else.</li>
    <li>Similarity (plagiarism) must be below <b>15%</b> excluding references.</li>
    <li>All authors must have agreed to the submission and the author order.</li>
    <li>The paper must be written in clear English and follow the IJRPO template.</li>
  </ul>
</section>
<section id="template">
  <h2>Paper format</h2>
  <table class="tbl"><tbody>
    <tr><td><b>File type</b></td><td>MS Word (.doc / .docx) for review; PDF is created by the journal</td></tr>
    <tr><td><b>Page size</b></td><td>A4, two-column layout, margins 0.75 inch</td></tr>
    <tr><td><b>Font</b></td><td>Times New Roman — title 18 pt bold, headings 11 pt bold, body 10 pt</td></tr>
    <tr><td><b>Length</b></td><td>6 to 15 pages including figures and references</td></tr>
    <tr><td><b>Title page</b></td><td>Title, author names, department, institution, city, country, email of corresponding author</td></tr>
    <tr><td><b>Abstract</b></td><td>150–250 words, followed by 4–6 keywords</td></tr>
    <tr><td><b>Sections</b></td><td>Introduction, Literature Review, Methodology, Results &amp; Discussion, Conclusion, References</td></tr>
    <tr><td><b>Figures &amp; tables</b></td><td>Numbered, with captions, and cited in the text</td></tr>
    <tr><td><b>References</b></td><td>IEEE style, numbered in order of citation, e.g. [1], [2]</td></tr>
  </tbody></table>
  <p>Paper template: {ph("[Upload IJRPO-Template.docx and link it here]")}</p>
</section>
<section id="process">
  <h2>Review and publication process</h2>
  <ol class="steps">
    <li><strong>Submission</strong> — author submits the manuscript and receives a paper ID.</li>
    <li><strong>Initial check</strong> — the editor checks scope, format and similarity (1–2 days).</li>
    <li><strong>Peer review</strong> — double-blind review by at least two reviewers (5–7 days).</li>
    <li><strong>Decision</strong> — accept, minor revision, major revision or reject, sent by email.</li>
    <li><strong>Final submission</strong> — revised paper, signed copyright form and publication fee.</li>
    <li><strong>Publication</strong> — paper published online in the next issue; e-certificates issued to all authors.</li>
  </ol>
</section>
<section>
  <h2>Documents for accepted papers</h2>
  <ul>
    <li>Final camera-ready paper in the IJRPO template</li>
    <li>Signed copyright / licence agreement form {ph("[link to form]")}</li>
    <li>Proof of payment of the publication fee</li>
  </ul>
</section>
""")

pages["submit.html"] = page("submit.html", "Submit Manuscript", f"""
<p class="note">Fill in the form below and click <b>Prepare Email</b>. Your email app will open with the details filled in — <b>attach your paper (.doc/.docx)</b> and send. You can also email your paper directly to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<form id="subForm" onsubmit="return sendSub(event)">
  <label for="title">Paper title *</label>
  <input id="title" required>
  <div class="row">
    <div><label for="author">Corresponding author name *</label><input id="author" required></div>
    <div><label for="email">Author email *</label><input id="email" type="email" required></div>
  </div>
  <div class="row">
    <div><label for="phone">Mobile number</label><input id="phone" type="tel"></div>
    <div><label for="country">Country *</label><input id="country" value="India" required></div>
  </div>
  <label for="coauthors">Co-authors (names, comma separated)</label>
  <input id="coauthors">
  <label for="inst">Department &amp; institution *</label>
  <input id="inst" required>
  <div class="row">
    <div><label for="area">Subject area *</label>
      <select id="area" required>
        <option value="">Select…</option>
        <option>Computer Science / AI / Data Science</option>
        <option>Electronics / Electrical Engineering</option>
        <option>Mechanical / Civil Engineering</option>
        <option>Applied Sciences</option>
        <option>Management / Commerce</option>
        <option>Humanities / Social Sciences</option>
        <option>Other</option>
      </select></div>
    <div><label for="ptype">Paper type *</label>
      <select id="ptype" required>
        <option>Research Paper</option><option>Review Paper</option><option>Case Study</option><option>Survey Paper</option>
      </select></div>
  </div>
  <label for="abs">Abstract</label>
  <textarea id="abs"></textarea>
  <label style="font-weight:400;color:var(--ink)"><input type="checkbox" required style="width:auto;margin:0 8px 0 0">I confirm this paper is original and not under review elsewhere.</label>
  <p style="margin-top:14px"><button class="btn primary" type="submit">Prepare Email</button></p>
</form>
<script>
function sendSub(e){{
  e.preventDefault();
  const v=id=>document.getElementById(id).value.trim();
  const body=["Paper title: "+v('title'),"Paper type: "+v('ptype'),"Subject area: "+v('area'),
    "Corresponding author: "+v('author'),"Email: "+v('email'),"Mobile: "+v('phone'),
    "Co-authors: "+v('coauthors'),"Institution: "+v('inst'),"Country: "+v('country'),"",
    "Abstract:",v('abs'),"","[Please attach your manuscript file before sending]"].join("\\n");
  location.href="mailto:{EMAIL}?subject="+encodeURIComponent("Paper Submission: "+v('title'))+"&body="+encodeURIComponent(body);
  return false;
}}
</script>
""")

pages["current-issue.html"] = page("current-issue.html", f"Current Issue", f"""
<section>
  <h2>Volume {J['volume']}, Issue {J['issue']} — {J['month_year']}</h2>
    {articles_html}
</section>
""")

pages["archives.html"] = page("archives.html", "Archives", f"""
<section>
  <h2>{J['year']}</h2>
  <table class="tbl"><thead><tr><th>Volume / Issue</th><th>Month</th><th>Papers</th></tr></thead><tbody>
    <tr><td><a href="current-issue.html">Volume {J['volume']}, Issue {J['issue']}</a></td><td>{J['month_year']}</td><td>{len(PAPERS) or 'In preparation'}</td></tr>
  </tbody></table>
  <p>Earlier issues will be listed here as the journal grows.</p>
</section>
""")

pages["publication-fee.html"] = page("publication-fee.html", "Publication Fee", f"""
<p>IJRPO is open access, so readers never pay. A one-time publication fee is charged <b>only after a paper is accepted</b>. It covers peer review handling, formatting, online hosting and certificates.</p>
<table class="tbl"><thead><tr><th>Author category</th><th>Fee</th><th>Includes</th></tr></thead><tbody>
  <tr><td>Indian authors</td><td>{ph(FEE_IN)}</td><td>Online publication, e-certificate for every author</td></tr>
  <tr><td>International authors</td><td>{ph(FEE_INT)}</td><td>Online publication, e-certificate for every author</td></tr>
</tbody></table>
<p>There is no charge for submission or review. Payment details are sent with the acceptance email.</p>
<h3>Payment methods</h3>
<p>{ph("[UPI ID / bank transfer details — shared privately in the acceptance email]")}</p>
<h3>Refunds</h3>
<p>Once a paper is published, the fee is not refundable. If a paper is withdrawn by the journal before publication, the full fee is returned.</p>
""")

pages["policies.html"] = page("policies.html", "Ethics & Policies", f"""
<section id="ethics"><h2>Publication ethics</h2>
<p>IJRPO follows the general principles of the Committee on Publication Ethics (COPE). Authors, reviewers and editors are expected to act honestly and fairly.</p>
<ul><li><b>Authors</b> must submit original work, cite sources properly and declare any conflicts of interest.</li>
<li><b>Reviewers</b> must keep manuscripts confidential and give objective, timely feedback.</li>
<li><b>Editors</b> decide only on the merit of the work, regardless of the author's background or institution.</li></ul></section>
<section id="plagiarism"><h2>Plagiarism policy</h2>
<p>Every manuscript is checked with similarity-detection software. Papers with more than 15% similarity (excluding references) are returned to authors for revision. Copied or fabricated work is rejected, and if found after publication the paper is retracted.</p></section>
<section id="review"><h2>Peer review policy</h2>
<p>IJRPO uses double-blind peer review: reviewers do not know the authors' identities, and authors do not know the reviewers'. Each paper is reviewed by at least two reviewers, and the editor makes the final decision.</p></section>
<section id="copyright"><h2>Copyright and licence</h2>
<p>Authors keep copyright of their work. By publishing with IJRPO, authors grant the journal the right to publish the paper first and license it under the <a href="https://creativecommons.org/licenses/by/4.0/" rel="noopener">Creative Commons Attribution 4.0 International (CC BY 4.0)</a> licence, which lets anyone share and adapt the work with proper credit.</p></section>
<section id="open-access"><h2>Open access policy</h2>
<p>All content is freely available without charge to readers or their institutions.</p></section>
<section id="retraction"><h2>Corrections and retractions</h2>
<p>Errors found after publication are corrected through a notice linked to the original paper. Papers with serious misconduct are retracted, and the retraction notice stays online.</p></section>
""")

pages["contact.html"] = page("contact.html", "Contact Us", f"""
<div class="grid-2">
  <div class="card"><h3>Editorial office</h3><p>{NAME}<br>Uttam Nagar, New Delhi<br>Delhi, India</p></div>
  <div class="card"><h3>Email &amp; phone</h3><p>Submissions &amp; queries: <a href="mailto:{EMAIL}">{EMAIL}</a><br>Phone / WhatsApp: +91 87502 50560<br>Hours: Mon–Sat, 10 am – 6 pm IST</p></div>
</div>
<section style="margin-top:32px"><h2>Send a message</h2>
<form onsubmit="event.preventDefault();const f=this;location.href='mailto:{EMAIL}?subject='+encodeURIComponent(f.s.value)+'&body='+encodeURIComponent(f.m.value+'\\n\\n— '+f.n.value+' ('+f.e.value+')');">
  <div class="row"><div><label>Name</label><input name="n" required></div><div><label>Email</label><input name="e" type="email" required></div></div>
  <label>Subject</label><input name="s" required>
  <label>Message</label><textarea name="m" required></textarea>
  <button class="btn primary">Send Message</button>
</form></section>
""")

# ---- individual paper pages (with Google Scholar meta tags) ----
import datetime
for p in PAPERS:
    pub = datetime.datetime.strptime(p["published"], "%d %B %Y")
    first, last = p["pages"].split("-")
    meta = [f'<meta name="citation_title" content="{esc(p["title"])}">']
    for a in p["authors"]:
        meta.append(f'<meta name="citation_author" content="{esc(a)}">')
        for aff in p["affiliations"]:
            meta.append(f'<meta name="citation_author_institution" content="{esc(aff)}">')
    meta += [
        f'<meta name="citation_journal_title" content="{NAME}">',
        f'<meta name="citation_journal_abbrev" content="{SHORT}">',
        '<meta name="citation_issn" content="2356-1068">',
        f'<meta name="citation_volume" content="{J["volume"]}">',
        f'<meta name="citation_issue" content="{J["issue"]}">',
        f'<meta name="citation_firstpage" content="{first}">',
        f'<meta name="citation_lastpage" content="{last}">',
        f'<meta name="citation_publication_date" content="{pub:%Y/%m/%d}">',
        f'<meta name="citation_publisher" content="{NAME}">',
        f'<meta name="citation_language" content="en">',
        f'<meta name="citation_keywords" content="{esc("; ".join(p["keywords"]))}">',
        f'<meta name="citation_abstract_html_url" content="https://{DOMAIN}/{p["slug"]}.html">',
        f'<meta name="citation_pdf_url" content="https://{DOMAIN}/{p["pdf"]}">',
        f'<link rel="canonical" href="https://{DOMAIN}/{p["slug"]}.html">',
    ]
    authors = ", ".join(p["authors"])
    cite = f'{esc(authors)}, &ldquo;{esc(p["title"])},&rdquo; <i>{NAME} ({SHORT})</i>, vol. {J["volume"]}, no. {J["issue"]}, pp. {first}&ndash;{last}, {J["month_year"]}.'
    email = f'<div class="aff">Email: <a href="mailto:{p["email"]}">{p["email"]}</a></div>' if p.get("email") else ""
    body = f"""
<div class="paper-head">
  <div class="article-item" style="border:0;padding:0;margin:0;background:none"><div class="type">{p['type']} · Paper ID: {p['id']}</div></div>
  <h2 style="margin-top:6px">{esc(p['title'])}</h2>
  <div class="authors"><b>{esc(authors)}</b></div>
  <div class="aff">{esc('; '.join(p['affiliations']))}</div>
  {email}
</div>
<p style="display:flex;gap:10px;flex-wrap:wrap">
  <a class="btn primary" href="{p['pdf']}">Read Full Paper (PDF)</a>
  <a class="btn" href="{p['pdf']}" download="{p['id']}.pdf">⬇ Download PDF</a>
</p>
<table class="tbl"><tbody>
  <tr><td><b>Published in</b></td><td><a href="current-issue.html">Volume {J['volume']}, Issue {J['issue']} ({J['month_year']})</a></td></tr>
  <tr><td><b>Pages</b></td><td>{first}&ndash;{last}</td></tr>
  <tr><td><b>Published on</b></td><td>{p['published']}</td></tr>
  <tr><td><b>Paper ID</b></td><td>{p['id']}</td></tr>
  <tr><td><b>Licence</b></td><td>CC BY 4.0 (open access)</td></tr>
</tbody></table>
<section><h3>Abstract</h3><p>{esc(p['abstract'])}</p></section>
<section><h3>Keywords</h3><div class="kw">{''.join(f'<span>{esc(k)}</span>' for k in p['keywords'])}</div></section>
<section><h3>How to cite</h3><div class="cite">{cite}</div></section>
"""
    pages[f"{p['slug']}.html"] = page(f"{p['slug']}.html", "Research Paper", body,
        desc=p["abstract"][:155] + "…", extra_head="\n".join(meta))

for name, content in pages.items():
    with open(os.path.join(SITE, name), "w", encoding="utf-8") as f:
        f.write(content)
print("built", len(pages), "pages:", ", ".join(pages))
