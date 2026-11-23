"""Author identity used on guides (E-E-A-T). Facts here were confirmed by the author."""
import html
esc = lambda s: html.escape(str(s), quote=True)
SITE = "https://yourbillcheck.com"

NAME = "Khalid Shaikh"
TITLE = "Director, YourBillCheck"
PATH = "/authors/khalid-shaikh"
LINKEDIN = "https://www.linkedin.com/in/khalid-shaikh-73826627/"
PHOTO = ""  # set to "/khalid.jpg" once a headshot is uploaded; initials badge is shown until then
BIO = ("Khalid leads a team that helps thousands of US households a month compare and switch home internet, TV and phone service. "
       "He works in US telecom sales and compliance, including FCC and TCPA rules, and started YourBillCheck to show people what they actually pay and where they are overpaying.")

PERSON = {"@type": "Person", "name": NAME, "jobTitle": "Director", "url": SITE + PATH,
          "sameAs": [LINKEDIN], "worksFor": {"@type": "Organization", "name": "YourBillCheck", "url": SITE}}

CSS = ('<style>.auth{display:flex;gap:14px;align-items:center;border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:0 0 26px;max-width:760px;background:#fff}'
       '.auth .av{width:52px;height:52px;border-radius:50%;flex:none;display:grid;place-items:center;background:var(--mint);color:#fff;font:800 20px var(--fd);object-fit:cover}'
       '.auth b{font:700 16px var(--fd)}.auth span{display:block;font-size:14px;color:var(--muted)}.auth a{font-size:14px}</style>')

def avatar(size=52):
    if PHOTO:
        return f'<img class="av" src="{PHOTO}" width="{size}" height="{size}" alt="{esc(NAME)}">'
    return '<span class="av" aria-hidden="true">KS</span>'

def box(checked):
    return (CSS + f'<div class="auth">{avatar()}<div><b>By <a href="{PATH}">{esc(NAME)}</a></b>'
            f'<span>{esc(TITLE)} · Checked {esc(checked)}</span>'
            f'<a href="{LINKEDIN}" rel="noopener me" target="_blank">LinkedIn</a></div></div>')

def build(save, shell):
    body = (CSS + f'<div class="auth">{avatar()}<div><b>{esc(NAME)}</b><span>{esc(TITLE)}</span>'
            f'<a href="{LINKEDIN}" rel="noopener me" target="_blank">LinkedIn profile</a></div></div>'
            f"<h2>About Khalid</h2><p>{esc(BIO)}</p>"
            "<h2>What Khalid writes and reviews</h2><p>Khalid writes and reviews our bill guides: why bills go up, what each fee means, and how to get a lower rate. "
            'Each guide lists its sources and the date it was checked. Read <a href="/methodology">how we get our data</a>.</p>'
            '<ul><li><a href="/bills">Why is my internet bill so high?</a></li><li><a href="/bills/xfinity">Xfinity bill guide</a></li>'
            '<li><a href="/bills/spectrum">Spectrum bill guide</a></li><li><a href="/bills/att">AT&amp;T bill guide</a></li></ul>'
            "<h2>Independence</h2><p>YourBillCheck may earn a commission when you switch through us, at no cost to you. That never changes what a guide says about a provider. "
            '<a href="/about">How we make money</a>.</p>')
    ld = [dict(PERSON, **{"@type": "Person", "description": BIO})]
    save(PATH, shell(PATH, f"{NAME}, {TITLE}", f"{NAME} is Director of YourBillCheck and writes its internet bill guides. " + BIO[:90],
                     NAME, esc(TITLE), body, None,
                     [("Home", SITE + "/"), ("Authors", SITE + "/about"), (NAME, SITE + PATH)], ["Author"],
                     jsonld_extra=ld, date="2026-11-24", checked="November 24, 2026"))
