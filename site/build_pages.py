#!/usr/bin/env python3
import json, glob, os, collections, html, re
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")
SITE = "https://yourbillcheck.com"
CHECKED = "November 22, 2026"
os.makedirs(OUT, exist_ok=True)
esc = lambda s: html.escape(str(s), quote=True)

# ---------- FCC-derived stats ----------
TECH = {10: "DSL", 40: "cable", 50: "fiber", 60: "satellite", 61: "satellite", 70: "fixed wireless", 71: "fixed wireless", 72: "fixed wireless"}
FCCNAME = {"xfinity": "Xfinity", "spectrum": "Spectrum", "att": "AT&T", "verizon": "Verizon", "t-mobile": "T-Mobile",
           "frontier": "Frontier", "cox": "Cox Communications", "centurylink": "CenturyLink", "optimum": "Optimum", "starlink": "Starlink"}
Z = {k: set() for k in FCCNAME}
ST = {k: set() for k in FCCNAME}
TC = {k: collections.Counter() for k in FCCNAME}
DOWN = {k: 0 for k in FCCNAME}
allz = set()
for f in glob.glob("/home/claude/zd/*-zips.json"):
    st = os.path.basename(f)[:2].upper()
    d = json.load(open(f)); B = d["b"]
    inv = {v: k for k, v in FCCNAME.items()}
    for z, v in d["z"].items():
        allz.add(z); seen = set()
        for p in v["p"]:
            k = inv.get(B[p[0]])
            if not k: continue
            Z[k].add(z); ST[k].add(st); DOWN[k] = max(DOWN[k], p[2])
            if (k, z, p[1]) not in seen:
                TC[k][TECH.get(p[1], "other")] += 1; seen.add((k, z, p[1]))
TOTAL = len(allz)

def spd(m): return (f"{m/1000:g} Gbps" if m >= 1000 else f"{m} Mbps")

# ---------- provider facts (support numbers copied from each provider's own site, checked Nov 22, 2026) ----------
P = {
 "xfinity": dict(name="Xfinity", kind="cable and fiber", price="from $20/mo", promo="",
   plans=[], note="",
   support=[("Customer service, billing and technical support", "1-800-934-6489 (1-800-XFINITY)", "https://www.xfinity.com/support/contact-us/"),
            ("Xfinity Mobile support", "1-888-936-4968", "https://www.xfinity.com/support/articles/california-public-utilities-commission")],
   official="https://www.xfinity.com/support/contact-us/"),
 "spectrum": dict(name="Spectrum", kind="cable and fiber", price="from $30/mo", promo="300 Mbps for $30/mo with Auto Pay, plus free Advanced WiFi and a free mobile line for 1 year.",
   plans=[], note="",
   support=[("Customer service, billing and technical support (24/7)", "833-949-0036", "https://www.spectrum.com/contact-spectrum"),
            ("Order new service", "855-860-9068", "https://www.spectrum.com/contact-spectrum"),
            ("Spectrum Mobile support (24/7)", "866-782-2681", "https://www.spectrum.com/mobile/contact-spectrum-mobile")],
   official="https://www.spectrum.com/contact-spectrum"),
 "att": dict(name="AT&T", kind="fiber, DSL and fixed wireless", price="from $35/mo", promo="$100 reward card with AT&T Fiber 1 Gig or faster.",
   plans=[("Fiber 300", "300 Mbps", "$35"), ("Fiber 1 Gig", "1 Gbps", "$65")],
   note="Promo price for new customers with AutoPay and paperless billing, for 12 months. The regular price is higher.",
   support=[("Internet, TV and home phone: billing and technical support", "800-288-2020", "https://www.att.com/support/internet/"),
            ("Wireless (mobile) customer care", "800-331-0500, or 611 from an AT&T phone", "https://www.att.com/support/how-to/notice-of-dispute/"),
            ("Prepaid customer care", "800-901-9878", "https://www.att.com/support/how-to/notice-of-dispute/")],
   official="https://www.att.com/support/"),
 "verizon": dict(name="Verizon", kind="Fios fiber and 5G Home", price="from $50/mo", promo="5G Home $50/mo with Auto Pay; $30-$35 with a Verizon mobile plan.",
   plans=[("5G Home", "up to 300 Mbps", "$50"), ("Fios 300", "300 Mbps", "$49.99"), ("Fios 500", "500 Mbps", "$74.99"), ("Fios 1 Gig", "1 Gbps", "$89.99")],
   note="Verizon prices need Auto Pay. Fios or 5G Home depends on your address.",
   support=[("Fios internet and TV: billing and technical support", "800-837-4966 (800-VERIZON)", "https://www.verizon.com/support/residential/account/view-bill/online/")],
   official="https://www.verizon.com/support/contact-us"),
 "t-mobile": dict(name="T-Mobile", kind="5G Home Internet and fiber", price="from $50/mo", promo="From $30/mo with a voice line and AutoPay.",
   plans=[("Rely", "5G Home", "$50"), ("Amplified", "5G Home", "$60"), ("All-In", "5G Home", "$70")],
   note="Promo $30 with a qualifying voice line. 5G Home availability depends on your address.",
   support=[("Customer service", "611 from a T-Mobile phone, or 1-800-937-8997", "https://www.t-mobile.com/contact-us"),
            ("5G Home Internet technical support", "1-844-275-9310", "https://www.t-mobile.com/contact-us"),
            ("T-Mobile Fiber technical support", "1-844-783-4237", "https://www.t-mobile.com/contact-us")],
   official="https://www.t-mobile.com/contact-us"),
 "frontier": dict(name="Frontier", kind="fiber and DSL", price="from about $45/mo", promo="Fiber 1 Gig for $64.99/mo with a 5-year price guarantee, no contracts, free Whole-Home Wi-Fi and installation.",
   plans=[("Fiber 500", "500 Mbps", "~$45"), ("Fiber 1 Gig", "1 Gbps", "~$65"), ("Fiber 2 Gig", "2 Gbps", "~$80")], note="",
   support=[("Product sales and upgrades", "800-921-8101", "https://frontier.com/contact-us"),
            ("Pay your bill by phone (automated line)", "800-917-7489", "https://frontier.com/helpcenter/billing")],
   official="https://frontier.com/contact-us", extra="For technical help, Frontier points customers to its chat and Help Center on frontier.com."),
 "cox": dict(name="Cox", kind="cable", price="from $55/mo", promo="",
   plans=[("Fast", "about 250 Mbps", "$55"), ("Go Even Faster", "500 Mbps", "$85"), ("Go Super Fast", "1 Gbps", "$100"), ("Go Beyond Fast", "2 Gbps", "$115")],
   note="Cox plans include a 1.25 TB monthly data cap.",
   official="https://www.cox.com/residential/contactus.html",
   extra="Cox directs customers to its online support and chat rather than one published residential phone number, so use the official Cox contact page (chat and support options) or the number on your bill.",
   support=[("Online support, chat and contact options", "Open Cox's official contact page", "https://www.cox.com/residential/contactus.html")]),
 "centurylink": dict(name="CenturyLink", kind="DSL and fiber", price="from $50/mo", promo="",
   plans=[("Fiber", "fiber", "$50"), ("Fiber Gig", "fiber", "$75"), ("DSL", "DSL", "$55")], note="About $15/mo modem. Plans vary by address.",
   support=[("Account and technical support", "800-244-1111", "https://www.centurylink.com/home/help/contact.html"),
            ("Order new service", "855-263-9576", "https://www.centurylink.com/home/help/contact.html")],
   official="https://www.centurylink.com/home/help/contact.html"),
 "optimum": dict(name="Optimum", kind="cable and fiber", price="from about $30/mo", promo="Fiber from $25/mo with a 3-year price lock and up to a $200 gift card, through Dec 31, 2026.",
   plans=[], note="",
   support=[("General, billing and technical support", "877-694-9474", "https://www.optimum.com/contact-us")],
   official="https://www.optimum.com/contact-us"),
 "starlink": dict(name="Starlink", kind="satellite", price="from $55/mo", promo="",
   plans=[("Residential", "up to 400 Mbps", "$55")], note="Equipment is extra (about $349 to buy, or rent in some areas). Price can be lower or higher by area.",
   official="https://www.starlink.com/support",
   support=[("Help center, chat and support requests", "Open Starlink Support", "https://www.starlink.com/support")],
   extra="Starlink handles support through its app and the Support page rather than a phone line. Use the Support page or the Starlink app."),
}
PF = {k: P[k] for k in P}

# ---------- page shell ----------
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ui
def page(path, title, desc, h1, lead, body, faq=None, crumbs=None, chips=None, script=""):
    return ui.shell(path, title, desc, h1, lead, body, faq, crumbs, chips, script=script, checked=CHECKED)

manifest = []
def save(path, html_):
    fn = os.path.join(OUT, (path.strip("/") or "index") + ".html")
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    open(fn, "w").write(html_)
    manifest.append(path)

def tech_phrase(k):
    c = TC[k]
    parts = [f"{n:,} ZIP codes with {t}" for t, n in c.most_common(3) if n > 0]
    return ", ".join(parts)

# ---------- provider pages ----------
def provider_page(k):
    p = P[k]; n = p["name"]; zc = len(Z[k]); sc = len(ST[k])
    pct = round(100 * zc / TOTAL)
    body = f"<h2>Where {esc(n)} reports service</h2>"
    body += (f"<p>In the provider-reported FCC availability data behind our ZIP pages, {esc(n)} reports service in about {zc:,} of the {TOTAL:,} ZIP codes we cover ({pct}%), across {sc} states. "
             f"The most common connection types in that data are: {esc(tech_phrase(k))}. The fastest speed reported anywhere is {spd(DOWN[k])} download, but your address may get a lower tier or none at all.</p>")
    body += f"<p>Coverage is reported by ZIP code. Confirm your exact address with {esc(n)}. Start at our <a href=\"/internet\">internet by state</a> pages or enter your ZIP on the <a href=\"/\">home page</a>.</p>"
    body += f"<h2>{esc(n)} starting prices we track</h2><p>Typical starting price: {esc(p['price'])} for new customers.</p>"
    if p["promo"]: body += f"<p>Current offer we found: {esc(p['promo'])}</p>"
    if p["plans"]:
        body += "<table><tr><th>Plan</th><th>Speed</th><th>Starting price</th></tr>" + "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)}</td></tr>" for a, b, c in p["plans"]) + "</table>"
    if p["note"]: body += f"<p>{esc(p['note'])}</p>"
    body += "<p>These are starting prices for new customers as of November 2026 and may rise after a promotion ends. Equipment, taxes and fees can add to the monthly total.</p>"
    body += f"<h2>{esc(n)} customer service and support numbers</h2>"
    if p["support"]:
        body += "<table><tr><th>For</th><th>Number</th><th>Source</th></tr>" + "".join(
            f"<tr><td>{esc(a)}</td><td><strong>{esc(b)}</strong></td><td><a href=\"{esc(c)}\" rel=\"nofollow noopener\">{esc(n)} official page</a></td></tr>" for a, b, c in p["support"]) + "</table>"
        body += ("<p>We copied these numbers from the provider's own website on " + CHECKED + ". Providers change numbers and use different ones by region or product, so also check the number on your bill. "
                 "Only call numbers listed on the provider's own site or your bill, because look-alike support numbers and scam ads are common.</p>")
    if p.get("extra"): body += f"<p>{esc(p['extra'])}</p>"
    body += f"<p>Official contact page: <a href=\"{esc(p['official'])}\" rel=\"nofollow noopener\">{esc(p['official'])}</a></p>"
    body += (f"<h2>Common {esc(n)} problems and where to start</h2><ul>"
             "<li><a href=\"/help/internet-not-working\">Internet not working</a></li><li><a href=\"/help/slow-internet\">Slow internet</a></li>"
             "<li><a href=\"/help/wifi-keeps-disconnecting\">Wi-Fi keeps disconnecting</a></li><li><a href=\"/help/tv-not-working\">TV not working</a></li>"
             "<li><a href=\"/help/tv-channels-missing\">Channels missing (ESPN, Showtime, Starz)</a></li><li><a href=\"/help/lost-or-stolen-sim\">Lost or stolen SIM</a></li>"
             "<li><a href=\"/help/cancel-internet-service\">Cancel service</a></li><li><a href=\"/speed-test\">Run a speed test</a></li></ul>")
    others = [x for x in ("xfinity", "spectrum", "att", "verizon", "frontier", "cox", "t-mobile", "centurylink") if x != k][:4]
    body += "<h2>Compare " + esc(n) + "</h2><ul>" + "".join(f"<li><a href=\"/compare/{a}-vs-{b}\">{P[a]['name']} vs {P[b]['name']}</a></li>" for a, b in PAIRS if k in (a, b)) + "</ul>"
    faq = [(f"What is the {n} customer service number?", (f"{n} lists " + "; ".join(f"{a}: {b}" for a, b, c in p['support']) + f" on its own website (checked {CHECKED}). Confirm against your bill." if p["support"] else f"We could not confirm a single residential number on {n}'s own site. Use the contact page at {p['official']} or the number on your bill.")),
           (f"Where does {n} offer internet?", f"In FCC provider-reported data, {n} reports service in about {zc:,} ZIP codes across {sc} states. Enter your ZIP to see whether {n} is reported near you."),
           (f"How much does {n} internet cost?", f"We track starting prices {p['price']} for new customers. Equipment, fees and the price after a promotion can be higher, so confirm before ordering."),
           (f"How do I get faster help with {n}?", f"Have your account number ready, call from the number on file if the provider asks, and use the provider's app or chat for outage checks. See our help guides for step-by-step fixes.")]
    save(f"/providers/{k}", page(f"/providers/{k}", f"{n} Customer Service Number, Plans and Coverage ({CHECKED[-4:]})",
         f"{n} support phone numbers from the provider's own site, starting prices, and where {n} reports service. Facts checked {CHECKED}.",
         f"{n}: Support Numbers, Plans and Coverage", f"{esc(n)} is a {esc(p['kind'])} provider. Here are its support phone numbers from its own site, the starting prices we track, and where it reports service.",
         body, faq, [("Home", SITE + "/"), ("Providers", SITE + "/providers"), (n, SITE + f"/providers/{k}")]))

PAIRS = [("xfinity", "spectrum"), ("att", "xfinity"), ("att", "spectrum"), ("verizon", "xfinity"), ("verizon", "att"),
         ("spectrum", "cox"), ("frontier", "xfinity"), ("frontier", "att"), ("t-mobile", "verizon"), ("centurylink", "frontier")]

def compare_page(a, b):
    A, B_ = P[a], P[b]; na, nb = A["name"], B_["name"]
    both = len(Z[a] & Z[b]); oa = len(Z[a] - Z[b]); ob = len(Z[b] - Z[a])
    row = lambda lab, x, y: f"<tr><td>{lab}</td><td>{x}</td><td>{y}</td></tr>"
    body = "<h2>The quick comparison</h2><table><tr><th></th><th>" + esc(na) + "</th><th>" + esc(nb) + "</th></tr>"
    body += row("Connection types", esc(A["kind"]), esc(B_["kind"]))
    body += row("ZIP codes reporting service", f"{len(Z[a]):,} ({round(100*len(Z[a])/TOTAL)}%)", f"{len(Z[b]):,} ({round(100*len(Z[b])/TOTAL)}%)")
    body += row("States reporting service", len(ST[a]), len(ST[b]))
    body += row("Fastest speed reported", spd(DOWN[a]), spd(DOWN[b]))
    body += row("Typical starting price", esc(A["price"]), esc(B_["price"])) + "</table>"
    body += (f"<p>Source: provider-reported FCC data matched to ZIP codes (June 30, 2026) and provider offers (November 2026). Starting prices are for new customers and can rise after a promotion.</p>")
    body += f"<h2>Availability: who can you actually get?</h2>"
    body += (f"<p>Of the {TOTAL:,} ZIP codes in our data, {both:,} have both {esc(na)} and {esc(nb)} reporting service, {oa:,} have only {esc(na)}, and {ob:,} have only {esc(nb)}. "
             f"That means in many places you will only have one of the two, and the better choice is simply whichever one serves your address. "
             f"Enter your ZIP on the <a href=\"/\">home page</a> to see which of them report service where you live.</p>")
    body += f"<h2>Speed and connection type</h2><p>{esc(na)} is mostly {esc(A['kind'])}; {esc(nb)} is mostly {esc(B_['kind'])}. Fiber usually gives the most consistent speeds and upload performance, cable is widely available and fast on download, and DSL or fixed wireless can be slower and vary more by address. "
    body += f"In the data, {esc(na)}'s top reported speed is {spd(DOWN[a])} and {esc(nb)}'s is {spd(DOWN[b])}, but that is the best tier in the best place, not what every address gets.</p>"
    body += f"<h2>Price</h2><p>{esc(na)}: {esc(A['price'])}.{(' ' + esc(A['promo'])) if A['promo'] else ''} {esc(nb)}: {esc(B_['price'])}.{(' ' + esc(B_['promo'])) if B_['promo'] else ''} "
    body += "Watch for what happens when the promotional price ends, equipment fees, data caps and whether you need AutoPay or a bundle to get the low price.</p>"
    notes = []
    for p_ in (A, B_):
        if p_["note"]: notes.append(f"{p_['name']}: {p_['note']}")
    if notes: body += "<p>" + esc(" ".join(notes)) + "</p>"
    body += "<h2>How to choose</h2><ul>"
    body += f"<li>If only one of them serves your address, that decides it. Check both pages: <a href=\"/providers/{a}\">{esc(na)}</a> and <a href=\"/providers/{b}\">{esc(nb)}</a>.</li>"
    body += "<li>If both serve you, compare the total first-year cost including equipment and fees, not just the headline monthly price.</li>"
    body += "<li>Pick the faster tier only if you need it. Most homes do well with 300 to 500 Mbps; see <a href=\"/guides/how-much-internet-speed-do-you-need\">how much speed you need</a>.</li>"
    body += "<li>Ask for the price you will pay in month 13, and whether there is a contract or early termination fee.</li></ul>"
    body += "<h2>Support numbers</h2><p>Both providers list support numbers on their own sites; we collect them on each provider page: " + f"<a href=\"/providers/{a}\">{esc(na)} support</a> and <a href=\"/providers/{b}\">{esc(nb)} support</a>.</p>"
    faq = [(f"Is {na} or {nb} better?", f"It depends on which one serves your address and what you pay after the promotion. In our data both report service in {both:,} ZIP codes; elsewhere you may only have one."),
           (f"Which is cheaper, {na} or {nb}?", f"{na} lists {A['price']} and {nb} lists {B_['price']} for new customers. Compare the first-year total with equipment and fees."),
           (f"Can I get {na} and {nb} at the same address?", f"Sometimes. {both:,} ZIP codes in our data have both reporting service, but availability is by address, so check each provider."),
           (f"Which has faster internet, {na} or {nb}?", f"The top reported speeds are {spd(DOWN[a])} for {na} and {spd(DOWN[b])} for {nb}, but your address determines which speeds you can actually order.")]
    save(f"/compare/{a}-vs-{b}", page(f"/compare/{a}-vs-{b}", f"{na} vs {nb}: Internet Compared ({CHECKED[-4:]})",
         f"{na} vs {nb}: coverage, speeds, starting prices and support compared using FCC provider-reported data and November 2026 offers.",
         f"{na} vs {nb}: Which Internet Provider Is Better?", f"Both {esc(na)} and {esc(nb)} sell home internet, but they are not always available at the same address. Here is how they compare on coverage, speed and price.",
         body, faq, [("Home", SITE + "/"), ("Compare", SITE + "/compare"), (f"{na} vs {nb}", SITE + f"/compare/{a}-vs-{b}")]))

# ---------- help guides (hand written) ----------
HELP = {}
def H(slug, title, desc, h1, lead, steps_title, steps, extra_sections, faq):
    body = f"<h2>{steps_title}</h2><ol>" + "".join(f"<li>{s}</li>" for s in steps) + "</ol>" + extra_sections
    body += "<h2>Provider support numbers</h2><p>If these steps do not fix it, call your provider using the number on your bill or on its own site. We list official numbers for the largest providers on our <a href=\"/providers\">provider support page</a>.</p>"
    HELP[slug] = (title, h1, desc)
    save(f"/help/{slug}", page(f"/help/{slug}", title, desc, h1, lead, body, faq, [("Home", SITE + "/"), ("Help", SITE + "/help"), (h1, SITE + f"/help/{slug}")]))

H("internet-not-working", "Internet Not Working? 10 Steps to Fix It Fast", "Step-by-step fixes when your home internet is down: check outages, restart your modem and router, test cables, and know when to call your provider.",
  "Internet Not Working: What to Do", "When your internet goes down, most problems come from a stuck modem or router, a loose cable or a local outage. Work through these steps in order before you call.", "Fix it in 10 steps",
  ["<strong>Check whether it is just one device.</strong> Try another phone or computer. If only one device is offline, restart that device and forget and rejoin the Wi-Fi network.",
   "<strong>Look for an outage.</strong> Use your provider's app or website outage page, or ask a neighbor. If there is an outage, you may be owed a bill credit.",
   "<strong>Check the lights.</strong> Most modems show status lights. A light that is off, red or blinking for a long time usually points to a connection problem.",
   "<strong>Check the cables.</strong> Make sure the power cable, the coax or fiber cable and the Ethernet cable are firmly connected and not damaged.",
   "<strong>Restart your equipment.</strong> Unplug the modem and the router, wait 30 seconds, plug in the modem first, wait until its lights settle, then plug in the router.",
   "<strong>Test with a cable.</strong> Connect a computer to the router with an Ethernet cable. If that works, the problem is your Wi-Fi, not the internet connection.",
   "<strong>Check your account.</strong> A past-due bill or suspended account can cut service. Sign in to your provider's app to confirm the account is active.",
   "<strong>Reset only as a last resort.</strong> A factory reset erases your Wi-Fi name and password settings, so write them down first.",
   "<strong>Contact your provider.</strong> Have your account number ready, say what you already tried and ask for a ticket number.",
   "<strong>Ask for a technician if it keeps happening.</strong> Repeated drops often come from a faulty line, connector or old equipment, which a technician can fix."],
  "<h2>When it keeps happening</h2><p>Write down when the outages happen and for how long. A record helps you ask for a credit, a technician visit or a better plan. If the provider cannot fix it, check whether another provider serves your address on our <a href=\"/\">ZIP check</a>.</p><p>Related: <a href=\"/help/slow-internet\">slow internet</a>, <a href=\"/help/wifi-keeps-disconnecting\">Wi-Fi keeps disconnecting</a>, <a href=\"/speed-test\">speed test</a>.</p>",
  [("Why is my internet not working but the Wi-Fi shows connected?", "Your device can be connected to the router while the router has no connection to the internet. Restart the modem and router, then check the modem lights and your provider's outage page."),
   ("How long should I wait for an outage to end?", "Many outages clear within a few hours, but if it lasts longer, contact your provider and ask about a bill credit."),
   ("Should I restart my router or my modem?", "Restart both. Unplug the modem and router for 30 seconds, start the modem first and then the router."),
   ("Can bad weather knock out my internet?", "Yes. Storms can damage lines or interrupt service, and heavy rain or snow can weaken satellite and fixed wireless signals.")])

H("slow-internet", "Slow Internet? How to Find the Cause and Speed It Up", "Why your internet is slow and how to fix it: test your speed, move closer to the router, cut device load, upgrade old equipment, or change plans.",
  "Slow Internet: Causes and Fixes", "Slow internet is usually a Wi-Fi, equipment or plan problem, not always your provider. Test first, then fix the weakest link.", "Speed it up",
  ["<strong>Run a speed test.</strong> Use our <a href=\"/speed-test\">speed test</a>, ideally on a computer connected by Ethernet, and compare the result to the speed you pay for.",
   "<strong>Test both wired and Wi-Fi.</strong> If wired is fast and Wi-Fi is slow, the problem is your router placement or Wi-Fi setup.",
   "<strong>Move the router.</strong> Put it in a central, open spot, off the floor and away from thick walls, microwaves and cordless phones.",
   "<strong>Use the 5 GHz band</strong> for devices close to the router. It is faster than 2.4 GHz but covers less distance.",
   "<strong>Pause heavy downloads</strong> and cloud backups, and check how many devices are streaming or gaming at the same time.",
   "<strong>Restart the modem and router</strong> to clear temporary problems.",
   "<strong>Update or replace old equipment.</strong> A router that is more than five years old may not handle current speeds.",
   "<strong>Compare your plan to your needs.</strong> A 100 Mbps plan can struggle with several 4K streams. See <a href=\"/guides/how-much-internet-speed-do-you-need\">how much speed you need</a>.",
   "<strong>Try different times of day.</strong> If it is only slow in the evening, congestion may be the cause, which your provider can look into."],
  "<h2>Speed test results: what they mean</h2><ul><li>Under 25 Mbps download: fine for basic browsing and one video stream, tight for a family.</li><li>25 to 100 Mbps: good for HD streaming and video calls for a few people.</li><li>100 to 500 Mbps: comfortable for most households, including 4K and gaming.</li><li>500 Mbps and up: useful for large households and heavy uploads.</li></ul><p>If the result is far below your plan speed even on a wired connection, contact your provider. If a faster plan or a different provider is available, <a href=\"/\">check your ZIP code</a>.</p>",
  [("Why is my internet slow only on Wi-Fi?", "Distance, walls, interference and old routers slow Wi-Fi. Test with an Ethernet cable to confirm."),
   ("Is it normal to get less than the advertised speed?", "Some difference is normal, especially on Wi-Fi, but wired tests should be close to your plan speed. Large gaps are worth raising with your provider."),
   ("Will a new router make my internet faster?", "It can, if the router is the bottleneck. It cannot make your connection faster than your plan allows."),
   ("What internet speed do I need?", "Most households do well with 300 to 500 Mbps. See our guide for a breakdown by household size and use.")])

H("wifi-keeps-disconnecting", "Wi-Fi Keeps Disconnecting? Causes and Fixes", "Fix a Wi-Fi connection that keeps dropping: interference, router placement, channel settings, outdated firmware and when to use a mesh system.",
  "Wi-Fi Keeps Disconnecting", "If Wi-Fi drops every few minutes, the cause is usually interference, distance or settings, and you can often fix it yourself.", "Fix the drops",
  ["<strong>Check if all devices drop.</strong> If only one does, update or reset that device's network settings. If all drop, the router is the likely cause.",
   "<strong>Restart the router</strong> and the modem.",
   "<strong>Move the router</strong> away from walls, microwaves, baby monitors and metal objects, and place it higher in a central room.",
   "<strong>Switch bands.</strong> Use 5 GHz for nearby devices and 2.4 GHz for far ones. Giving each band a separate name can make this easier.",
   "<strong>Change the channel.</strong> Crowded neighborhoods can cause interference. Set the router to auto, or try channels 1, 6 or 11 on 2.4 GHz.",
   "<strong>Update the router firmware</strong> in its app or admin page.",
   "<strong>Reduce the load.</strong> Many devices on one old router can cause drops.",
   "<strong>Add coverage.</strong> A mesh system or a wired access point works better than a basic extender in larger homes.",
   "<strong>Replace aging equipment</strong> if the router is several years old or runs hot."],
  "<p>If the connection also drops on a device connected by Ethernet, the problem is the line or modem, not Wi-Fi. See <a href=\"/help/internet-not-working\">internet not working</a>.</p>",
  [("Why does my Wi-Fi disconnect every few minutes?", "Common causes are interference, a weak signal at that spot, an overloaded or old router, or a device that keeps switching networks."),
   ("Do Wi-Fi extenders help?", "They can, but they often cut speed in half. A mesh system or a wired access point is usually better for larger homes."),
   ("Should I call my internet provider?", "Yes, if wired devices also drop or the modem lights show errors. Otherwise start with the router settings."),
   ("Can a VPN cause disconnections?", "Sometimes. Turn it off briefly to see if the drops stop.")])

H("tv-not-working", "TV Not Working? Fix No Signal and Black Screen", "Fix a TV with no signal or a frozen cable or streaming box: check the input, restart the box, test HDMI and cables, and confirm your account is active.",
  "TV Not Working: No Signal or Black Screen", "A TV that shows no signal or a black screen usually points to the wrong input, a cable problem or a box that needs a restart.", "Fix it step by step",
  ["<strong>Check the input.</strong> Make sure the TV is set to the HDMI input your box is connected to.",
   "<strong>Check power.</strong> Confirm both the TV and the cable or streaming box are on and the lights are normal.",
   "<strong>Test the HDMI cable.</strong> Reseat it at both ends, or try another cable or another HDMI port.",
   "<strong>Restart the box.</strong> Unplug it for 30 seconds, plug it back in and wait a few minutes for it to start.",
   "<strong>Check the remote.</strong> Replace the batteries and make sure the remote is paired with the right device.",
   "<strong>Check the coax cable.</strong> Make sure the cable from the wall is tight at both ends. A loose connector can cause pixelation or lost channels.",
   "<strong>Check for an outage or account issue</strong> in your provider's app or website.",
   "<strong>Try a different TV or port</strong> to see whether the TV or the box is at fault.",
   "<strong>Contact your provider</strong> to ask them to refresh the box signal, replace the box or schedule a technician."],
  "<p>For missing channels on a working picture, see <a href=\"/help/tv-channels-missing\">channels missing</a>. If your internet is also down, see <a href=\"/help/internet-not-working\">internet not working</a>.</p>",
  [("Why does my TV say no signal?", "The TV may be on the wrong input, the cable may be loose, or the box may need a restart."),
   ("Why is my cable box frozen?", "A restart often fixes it. Unplug it for 30 seconds and plug it back in."),
   ("Can a bad HDMI cable cause a black screen?", "Yes. Try another cable or port."),
   ("Will my provider send a new box?", "Often, if a restart does not fix it. Ask your provider about replacement options.")])

H("tv-channels-missing", "TV Channels Missing? ESPN, Showtime, Starz and More", "Why TV channels are missing or locked, and how premium channels like Showtime and Starz differ from ESPN: packages, add-ons, signal refresh and streaming options.",
  "TV Channels Missing: ESPN, Showtime, Starz and More", "Channels can disappear because of your package, an add-on that is not active, a signal issue or a lineup change. Here is how to tell which one it is.", "Find out why a channel is missing",
  ["<strong>Check your package.</strong> Sign in to your account and see which package and add-ons you have. Many channels only come with higher tiers.",
   "<strong>Check premium add-ons.</strong> Channels like Showtime, Starz and HBO are usually premium add-ons that cost extra, even if your base package includes many others.",
   "<strong>Check sports packages.</strong> Where ESPN and other sports channels appear depends on your provider and tier, and regional sports networks may be in separate packages.",
   "<strong>Look for a lineup change.</strong> Providers and networks sometimes lose or add channels after a contract dispute, which affects everyone in that area.",
   "<strong>Refresh the box.</strong> Restart it, or ask your provider to send a refresh signal to re-authorize your channels.",
   "<strong>Check the channel number.</strong> Channel numbers differ by area and provider, so use the guide on the box or the provider's channel lineup page.",
   "<strong>Contact your provider.</strong> If you pay for a channel that is not working, ask them to re-authorize it, and check your next bill for credits."],
  "<h2>Streaming apps and premium channels</h2><p>Several premium channels also sell their own streaming apps, which can work with any internet connection. Compare the cost of the add-on on your TV package with the standalone app price before deciding. Prices and bundles change often, so check each service's current price.</p><p>Related: <a href=\"/help/tv-not-working\">TV not working</a>, <a href=\"/guides/internet-for-streaming-and-gaming\">internet for streaming and gaming</a>.</p>",
  [("Why are some channels blocked on my TV?", "The channel may be in a package or add-on you do not have, or it may need to be re-authorized by your provider."),
   ("Is ESPN included in every TV package?", "No. Which tiers include ESPN and other sports channels varies by provider, so check your package or the provider's channel lineup."),
   ("Are Showtime and Starz included?", "Usually they are premium add-ons that cost extra, though some promotions include them for a period."),
   ("Can I watch premium channels without a cable package?", "Many premium channels offer their own streaming apps. Check each service's current pricing.")])

H("lost-or-stolen-sim", "Lost or Stolen SIM or Phone? What to Do Right Away", "Steps if your SIM card or phone is lost or stolen: suspend the line, protect your accounts, get a replacement SIM or eSIM, and set a port-out PIN.",
  "Lost or Stolen SIM: What to Do Right Away", "If your SIM or phone is lost or stolen, act quickly. Someone with your SIM can receive your calls and text messages, including verification codes.", "Do these in order",
  ["<strong>Call your carrier from another phone.</strong> Ask them to suspend or block the line and the SIM. You can also do this in your carrier's website or app from another device. Our <a href=\"/providers\">provider support page</a> lists official numbers.",
   "<strong>Use a find-my-phone tool.</strong> If the phone is lost, try your phone's find, lock and erase options before you give up on it.",
   "<strong>Request a replacement SIM or eSIM.</strong> Ask your carrier for a new SIM or an eSIM transfer, and confirm your number is moved to it.",
   "<strong>Add a port-out or account PIN.</strong> Ask your carrier to add a PIN to your account so no one can move your number to another carrier or SIM.",
   "<strong>Secure important accounts.</strong> Change passwords for email, banking and social accounts, and move two-factor codes to an authenticator app instead of text messages.",
   "<strong>Watch your bank and credit accounts.</strong> If your phone is stolen, tell your bank and watch for unfamiliar activity.",
   "<strong>Report a theft.</strong> If it was stolen, you can file a police report, which some carriers or insurers may ask for.",
   "<strong>Ask about insurance or a replacement phone</strong> if you have device protection."],
  "<p>Keep your account number and the last bill handy when you call, and ask the carrier to note on your account that the line was lost or stolen.</p>",
  [("Can someone use my phone number if they have my SIM?", "They may be able to receive calls and texts, including verification codes, until the line is suspended. Suspend it quickly."),
   ("Will I keep my phone number with a new SIM?", "Yes. Your carrier can move your number to a new SIM or eSIM after verifying your identity."),
   ("Is a SIM replacement free?", "It varies by carrier and situation. Ask when you contact them."),
   ("What is a port-out PIN?", "It is a security code on your mobile account that prevents your number from being transferred without it.")])

H("modem-router-setup", "How to Set Up a Modem and Router", "How to install and set up your own modem and router: connect cables, activate the modem, change the Wi-Fi name and password and place the router for the best signal.",
  "How to Set Up a Modem and Router", "Setting up your internet takes about 20 minutes with the right steps. Use the equipment from your provider or your own compatible modem and router.", "Set it up in order",
  ["<strong>Choose a spot.</strong> Put the modem where the cable or fiber line comes in, and place the router in a central, open area.",
   "<strong>Connect the line.</strong> Attach the coax or phone line to the modem, or connect the fiber terminal as your provider instructs.",
   "<strong>Connect the modem to the router</strong> with an Ethernet cable, then plug in power to the modem first and then the router.",
   "<strong>Wait for the lights.</strong> The modem can take several minutes to connect. Wait until the online light is steady.",
   "<strong>Activate service.</strong> Follow your provider's activation steps in its app, website or by phone, if the modem needs to be activated.",
   "<strong>Name your Wi-Fi and set a strong password.</strong> Use a long password that you do not use anywhere else.",
   "<strong>Update the firmware</strong> in the router app, and turn on automatic updates.",
   "<strong>Test your speed</strong> with our <a href=\"/speed-test\">speed test</a> and compare it with your plan."],
  "<p>Not sure whether to set it up yourself? See <a href=\"/help/self-install-vs-professional-install\">self-install vs professional install</a>.</p>",
  [("Do I need to buy my own modem?", "Not always. Many providers rent equipment for a monthly fee, but you can often use your own compatible equipment. Check your provider's approved list."),
   ("Why is my new modem not connecting?", "It may need to be activated, or the cable may be loose. Wait several minutes and check your provider's activation steps."),
   ("Where should I put the router?", "In a central, open spot, away from walls, metal and microwaves."),
   ("Should I change the default Wi-Fi password?", "Yes. A strong, unique password keeps others off your network.")])

H("self-install-vs-professional-install", "Self-Install or Professional Install for Internet?", "Compare self-install and professional installation for home internet: cost, time, when each makes sense and a checklist for installation day.",
  "Self-Install vs Professional Install", "Many providers let you choose between a self-install kit and a technician. Here is how to decide.", "How to choose",
  ["<strong>Self-install</strong> fits when the line is already active at your address, such as cable or fiber that was used before. It is usually quicker and often free or low cost.",
   "<strong>Professional install</strong> fits when the address is new to the provider, wiring is damaged or missing, or you want help with fiber hookups and Wi-Fi coverage.",
   "<strong>Ask about the cost.</strong> Fees vary by provider and offer, and some waive installation with a promotion. Ask whether a self-install kit or a technician visit has a fee.",
   "<strong>Ask for the appointment window</strong> and whether someone over 18 must be home.",
   "<strong>Before the visit,</strong> clear a path to where the equipment will go, know where you want the router and ask where the technician will drill, if at all.",
   "<strong>After the visit,</strong> run a <a href=\"/speed-test\">speed test</a>, check Wi-Fi in each room and keep the work order number."],
  "<p>If you rent a home, check with your landlord before drilling or running new lines.</p>",
  [("Is self-install cheaper?", "Often yes, but it depends on the provider and offer."),
   ("How long does a technician install take?", "It commonly takes a few hours, depending on the address and the type of service."),
   ("Can I do a fiber install myself?", "Some providers allow it if the fiber line is already at your home. Others require a technician. Ask your provider."),
   ("What should I do if the speed is lower after the install?", "Test with Ethernet, restart the equipment, and ask the provider to recheck if the wired speed is far below your plan.")])

H("cancel-internet-service", "How to Cancel Internet Service Without Surprises", "Steps to cancel home internet or TV: check your contract, return equipment, get a confirmation and avoid extra charges on your final bill.",
  "How to Cancel Internet Service", "Canceling is easier when you check the contract first, return equipment properly and keep proof that you canceled.", "Cancel in order",
  ["<strong>Check for a contract.</strong> Look for an early termination fee or promotional credits you could lose.",
   "<strong>Line up the new service first.</strong> If you are switching, get the new provider installed before you cancel the old one, so you are never without internet.",
   "<strong>Ask about retention offers.</strong> Providers often offer lower prices to keep customers. If you only want a cheaper price, see <a href=\"/guides/how-to-lower-your-internet-bill\">how to lower your internet bill</a>.",
   "<strong>Cancel using the provider's official method</strong> and ask for a confirmation number and the cancellation date in writing.",
   "<strong>Return the equipment.</strong> Ask how and where, and keep the receipt or tracking number. Unreturned equipment is a common cause of extra charges.",
   "<strong>Check the final bill.</strong> Look for prorated charges and equipment fees, and dispute anything wrong.",
   "<strong>Stop automatic payments</strong> after the final bill is settled, and keep your records."],
  "<p>If you are moving, see <a href=\"/help/move-internet-service\">moving your internet</a>.</p>",
  [("Will I be charged an early termination fee?", "It depends on your contract. Many plans have no contract, but some promotions do."),
   ("What happens if I do not return the equipment?", "Providers may charge an equipment fee. Return it and keep proof."),
   ("How far ahead should I cancel?", "Cancel after the new service is working, and ask for the exact end date to avoid paying for extra days."),
   ("Can I cancel online?", "It depends on the provider. Use its official channels and keep a confirmation.")])

H("move-internet-service", "Moving? How to Transfer or Start Internet at a New Address", "Moving soon? How to transfer or start home internet at a new address: check availability by ZIP, book installation early and avoid a gap in service.",
  "Moving Your Internet Service", "Providers are not the same at every address, so check what is available at your new home before you move.", "Plan your move",
  ["<strong>Check availability at the new address.</strong> Enter the new ZIP on our <a href=\"/\">home page</a> to see which providers report service, then confirm the exact address with the provider.",
   "<strong>Start 2 to 3 weeks early.</strong> Installation appointments can book up, especially at the end of the month.",
   "<strong>Ask about transferring service</strong> if your current provider serves the new address. You may keep your plan or get a new offer.",
   "<strong>Compare new customer offers.</strong> A different provider may offer a lower price or faster speeds at the new address.",
   "<strong>Schedule the cancellation</strong> at the old address to match your move date.",
   "<strong>Return old equipment</strong> and keep the receipt.",
   "<strong>On move-in day,</strong> test the connection with our <a href=\"/speed-test\">speed test</a> and keep your order number handy."],
  "<p>See <a href=\"/help/cancel-internet-service\">how to cancel</a> and <a href=\"/help/self-install-vs-professional-install\">self-install vs professional install</a>.</p>",
  [("Can I take my internet provider with me when I move?", "Only if the provider serves your new address. Check by ZIP and confirm with the provider."),
   ("When should I order internet for a new home?", "Two to three weeks before you move is a good rule."),
   ("Is it better to switch providers when I move?", "It can be, since new customers often get lower promotional prices. Compare the options at the new address."),
   ("What if my new address has only one provider?", "You may have fewer choices, but you can still compare plans, speeds and price after the promotion.")])

# ---------- hubs ----------
def hub(path, title, desc, h1, lead, items, crumbs):
    body = "<ul>" + "".join(f"<li><a href=\"{u}\">{esc(t)}</a> - {esc(d)}</li>" for u, t, d in items) + "</ul>"
    save(path, page(path, title, desc, h1, lead, body, None, crumbs))

hub("/compare", "Compare Internet Providers: Head-to-Head Comparisons | YourBillCheck",
    "Head-to-head comparisons of major US internet providers using FCC provider-reported coverage data and current starting prices.", "Compare Internet Providers",
    "See how major providers compare on coverage, speeds and starting prices.",
    [(f"/compare/{a}-vs-{b}", f"{P[a]['name']} vs {P[b]['name']}", f"coverage, speed and price compared") for a, b in PAIRS], [("Home", SITE + "/"), ("Compare", SITE + "/compare")])
hub("/providers", "Provider Customer Service and Support Numbers | YourBillCheck",
    "Customer service numbers for major US internet, TV and mobile providers, copied from each provider's own site and checked Nov 22, 2026.", "Provider Support Numbers and Plans",
    "Official customer service numbers for major providers, copied from their own websites, plus coverage and starting prices.",
    [(f"/providers/{k}", f"{P[k]['name']}", f"support numbers, plans and coverage") for k in P], [("Home", SITE + "/"), ("Providers", SITE + "/providers")])

for k in P: provider_page(k)
for a, b in PAIRS: compare_page(a, b)

# ---------- speed test ----------
ST_BODY = """
<div id="st" class="card" style="padding:26px;max-width:760px">
<button id="go" class="btn" style="font-size:18px;padding:15px 30px">Start speed test</button>
<p id="stat" style="color:#445;margin:12px 0 0">Press the button. The test takes about 30 seconds. For the most accurate result, use a computer connected by Ethernet and pause other downloads.</p>
<div id="res" style="display:none;margin-top:14px"><table><tr><th>Download</th><th>Upload</th><th>Latency</th><th>Jitter</th></tr><tr><td id="d">-</td><td id="u">-</td><td id="l">-</td><td id="j">-</td></tr></table>
<p id="msg"></p>
<form id="zf" onsubmit="var z=document.getElementById('zi').value.trim();if(/^\\d{5}$/.test(z)){location.href='/internet/'+z}else{alert('Enter a 5-digit ZIP code')}return false"><p>Want a faster or cheaper plan? <input id="zi" inputmode="numeric" maxlength="5" placeholder="Your ZIP" style="padding:8px;border:1px solid #bbc;border-radius:6px"> <button class="btn" style="padding:9px 16px;font-size:15px">See providers</button></p></form></div>
<noscript><p>The speed test needs JavaScript.</p></noscript></div>
<script type="module">
const $=id=>document.getElementById(id);
$("go").addEventListener("click",async()=>{
 $("go").disabled=true;$("stat").textContent="Loading the test...";$("res").style.display="none";
 try{
  const {default:SpeedTest}=await import("https://esm.sh/@cloudflare/speedtest@1.5.0");
  const t=new SpeedTest({autoStart:false});
  t.onResultsChange=()=>{$("stat").textContent="Testing... "+(t.results&&t.results.getSummary&&t.results.getSummary().download?(t.results.getSummary().download/1e6).toFixed(0)+" Mbps so far":"")};
  t.onFinish=r=>{
   const s=r.getSummary();const dn=s.download/1e6,up=s.upload/1e6;
   $("d").textContent=dn.toFixed(1)+" Mbps";$("u").textContent=up.toFixed(1)+" Mbps";$("l").textContent=(s.latency||0).toFixed(0)+" ms";$("j").textContent=(s.jitter||0).toFixed(0)+" ms";
   let m;if(dn<25)m="That is slow for most households. Try the fixes in our slow internet guide, and check whether a faster provider reports service at your address.";
   else if(dn<100)m="That works for HD streaming and video calls for a few people. Heavy households may want more.";
   else if(dn<500)m="That is a comfortable speed for most homes, including 4K streaming and gaming.";
   else m="That is a very fast connection.";
   $("msg").innerHTML=m+' <a href="/help/slow-internet">Slow internet guide</a>';
   $("res").style.display="block";$("stat").textContent="Done.";$("go").disabled=false;$("go").textContent="Run again";
  };
  t.onError=()=>{$("stat").textContent="The test could not run. Check your connection and try again.";$("go").disabled=false};
  t.play();
 }catch(e){$("stat").textContent="The test could not load. Check your connection or ad blocker and try again.";$("go").disabled=false}
});
</script>
"""
ST_EXTRA = ("<h2>How to read your results</h2><ul><li><strong>Download</strong> is how fast data reaches you: streaming, browsing, downloads.</li>"
            "<li><strong>Upload</strong> is how fast you send data: video calls, cloud backups, posting video.</li>"
            "<li><strong>Latency</strong> is the delay in milliseconds. Lower is better for gaming and calls.</li>"
            "<li><strong>Jitter</strong> is how much latency varies. High jitter makes calls and games choppy.</li></ul>"
            "<h2>How to get an accurate test</h2><ol><li>Use a computer connected by Ethernet if you can.</li><li>Close streaming, downloads and cloud backups.</li><li>Run it two or three times and at different times of day.</li><li>Compare the result with the speed on your bill. Wi-Fi results are usually lower than wired.</li></ol>"
            "<p>This test runs in your browser using Cloudflare's open speed test and does not need an account. Results depend on your device, Wi-Fi and the time of day.</p>"
            "<p>Results far below your plan? See <a href=\"/help/slow-internet\">slow internet fixes</a> and <a href=\"/help/internet-not-working\">internet not working</a>.</p>")
faq = [("What is a good internet speed?", "For most homes, 100 to 500 Mbps download is comfortable. Basic use works with 25 to 100 Mbps. See our guide on how much speed you need."),
       ("Why is my speed test lower than my plan?", "Wi-Fi, old equipment, other devices and time of day all lower results. Test with Ethernet to see your true connection speed."),
       ("Is this speed test free?", "Yes, it is free and needs no account."),
       ("How often should I test my internet speed?", "Test when you notice slowdowns, after changing equipment and before calling your provider.")]
save("/speed-test", page("/speed-test", "Free Internet Speed Test | YourBillCheck",
     "Run a free internet speed test to measure download, upload, latency and jitter, then see what the results mean and how to fix slow internet.", "Free Internet Speed Test",
     "Test your download and upload speed, latency and jitter in about 30 seconds, then compare the result with the plan you pay for.",
     ST_BODY + ST_EXTRA, faq, [("Home", SITE + "/"), ("Speed test", SITE + "/speed-test")]))

import build_help
build_help.build(P, page, save)
MD = build_help.build_models(P, page, save)
json.dump(sorted(set(manifest)), open(os.path.join(OUT, "manifest.json"), "w"), indent=0)
print(len(manifest), "pages;", TOTAL, "zips")
