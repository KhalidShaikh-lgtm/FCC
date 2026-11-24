"""Generic page builder for the SEO agents.

Every JSON file under site/content/ (any subfolder) becomes one static page. Agents add or edit JSON; they never
touch HTML templates. Schema (all strings plain text unless the key ends in _html):

{
  "path": "/fiber/az/phoenix",            # must start with an allowed prefix: /fiber /internet/<st>/<city> /guides /fees /save /bills
  "title": "Fiber Internet in Phoenix, AZ: Providers, Prices and Availability (2026)",
  "description": "150-160 chars",
  "h1": "Fiber internet in Phoenix, AZ",
  "lead": "One sentence under the H1",
  "short_answer": "40-60 word direct answer (AEO snippet)",
  "chips": ["Local guide", "Sources listed"],
  "crumbs": [["Home","/"],["Internet in Arizona","/internet/az"],["Fiber in Phoenix","/fiber/az/phoenix"]],
  "sections": [ {"h2": "Heading", "body_html": "<p>...</p>"} , {"h2": "Table", "table": {"head": ["A","B"], "rows": [["x","y"]]}} ],
  "faq": [["Question?","Answer."]],
  "sources": [["Title","https://..."]],
  "checked": "November 24, 2026",        # date facts were verified
  "date": "2026-11-24",
  "cta_provider": "internet"              # wording for the call box
}
"""
import glob, json, os, html
import ui, author
import build_bills as BB
import build_extra as BE

esc = lambda s: html.escape(str(s), quote=True)
SITE = "https://yourbillcheck.com"
HERE = os.path.dirname(os.path.abspath(__file__))
ALLOWED = ("/fiber/", "/internet/", "/guides/", "/fees/", "/save/", "/bills/")

def render(d):
    p = d["path"]
    assert p.startswith(ALLOWED) and p == p.lower() and " " not in p, "bad path " + p
    checked = d.get("checked", "November 24, 2026")
    body = author.box(checked)
    if d.get("short_answer"):
        body += f'<div class="call tip"><b>Short answer</b>{esc(d["short_answer"])}</div>'
    for s in d.get("sections", []):
        if s.get("h2"): body += f"<h2>{esc(s['h2'])}</h2>"
        if s.get("body_html"): body += s["body_html"]
        if s.get("table"):
            t = s["table"]; body += BE.table(t["head"], [[c for c in r] for r in t["rows"]])
    body += BB.call_cta(d.get("cta_provider", "internet"))
    if d.get("sources"): body += BE.srcs([tuple(x) for x in d["sources"]])
    crumbs = [(n, SITE + u) for n, u in d.get("crumbs", [["Home", "/"], [d["h1"], p]])]
    faq = [(q, esc(a)) for q, a in d.get("faq", [])] or None
    return ui.shell(p, d["title"], d["description"], d["h1"], esc(d.get("lead", "")), body, faq, crumbs,
                    d.get("chips", ["Sources listed"]), date=d.get("date", "2026-11-24"), checked=checked, author=author.PERSON)

def build(save):
    n = 0
    for f in sorted(glob.glob(os.path.join(HERE, "content", "**", "*.json"), recursive=True)):
        d = json.load(open(f))
        save(d["path"], render(d)); n += 1
    return n
