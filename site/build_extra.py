"""Batch 2: fee explainers (/bills/fees/<slug>) and speed-test topic pages (/speed-test/<topic>).
Facts checked November 24, 2026; every page lists its sources."""
import html
import ui, author

esc = lambda s: html.escape(str(s), quote=True)
SITE = "https://yourbillcheck.com"
CHECKED = "November 24, 2026"
DATE = "2026-11-24"
PHONE_TXT, PHONE_TEL = "(888) 491-5666", "+18884915666"

def lc(n):
    return n[0].lower() + n[1:]

def srcs(lst):
    return ("<h2>Sources</h2><ul>" + "".join(f'<li><a href="{esc(u)}" rel="nofollow noopener" target="_blank">{esc(t)}</a></li>' for t, u in lst)
            + f"</ul><p class=\"note\">Checked {CHECKED}. Amounts vary by area and change often; your bill and your provider's broadband label are the final word.</p>")

def table(head, rows):
    return ("<table><tr>" + "".join(f"<th>{esc(h)}</th>" for h in head) + "</tr>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</table>")

def cta():
    return ('<div class="cta"><div><h3>Not sure what you are paying for?</h3><p>Call us and we will go through your bill line by line and compare it with what is available at your address. '
            'Free. If you switch through us we may earn a commission, at no cost to you. <a href="/about" style="color:#fff">How we make money</a>.</p></div>'
            f'<a class="btn" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a></div>')

# ---------------- fee explainers ----------------
# slug: (name, short answer, what it is, provider rows [(provider, amount/notes)], how to avoid [..], faq [(q,a)], sources)
FEES = {
 "broadcast-tv-fee": ("Broadcast TV fee",
  "The Broadcast TV fee is a monthly charge cable TV providers add for carrying local channels such as ABC, CBS, NBC and FOX. It is not a government fee or tax, it is usually left out of promotional prices, and providers can raise it during a promotion.",
  "Local stations charge TV providers for the right to carry them (retransmission fees). Instead of building that cost into the package price, many providers list it as a separate line. Xfinity says its Broadcast TV Fee is not government-mandated, is excluded from promotional and contract pricing, and can increase during a promotion with advance notice.",
  [("Xfinity", "Itemized on legacy TV packages; Xfinity's newer 2026 TV packages fold it into one price"),
   ("Spectrum", "Broadcast TV surcharge on TV accounts; Spectrum's offer terms have listed it at up to $21.00/mo"),
   ("Optimum", "TV broadcast fee of $9.99/mo (reported)"),
   ("Verizon Fios TV", "Broadcast TV fee on Fios TV bills")],
  ["Ask whether an all-inclusive TV package (no separate broadcast fee) costs less in total than your current package.",
   "If you mostly watch local channels, an over-the-air antenna gets them free in many areas.",
   "Streaming live-TV services include locals in their price, so compare the total, not the headline.",
   "Internet-only plans have no broadcast fee at all."],
  [("Is the Broadcast TV fee a government tax?", "No. It is a provider charge that recovers what local stations charge the provider. Taxes are listed separately."),
   ("Can the Broadcast TV fee go up during my promotion?", "Yes. Providers such as Xfinity exclude it from promotional pricing and can raise it with notice."),
   ("Can I get the Broadcast TV fee removed?", "Not while you keep a TV package that carries local channels. You can avoid it with internet-only service, an antenna, or a package that bundles the fee into one price.")],
  [("Xfinity: most common taxes, fees and surcharges", "https://www.xfinity.com/support/articles/most-common-taxes-fees-surcharges-on-your-bill"),
   ("CableTV.com: Spectrum internet and TV offer terms (broadcast surcharge)", "https://www.cabletv.com/charter/internet"),
   ("HighSpeedInternet.com: what you actually pay for Optimum", "https://highspeedinternet.com/resources/optimum-real-costs")]),
 "regional-sports-fee": ("Regional sports fee",
  "The regional sports network (RSN) fee is a monthly TV charge for carrying local sports channels. It depends on your TV package, is usually excluded from promotional pricing, and can rise with notice.",
  "Regional sports networks carry local pro and college games and charge TV providers a high price per subscriber. Providers pass that on as a separate line on packages that include those channels. Xfinity says the fee is excluded from promotional or minimum-term pricing and may increase with notice.",
  [("Xfinity", "Regional Sports Network Fee on legacy packages that include RSNs"),
   ("Optimum", "Regional sports network fee of $10.47/mo (reported)"),
   ("Verizon Fios TV", "Regional sports fees on some Fios TV packages")],
  ["Ask for a package without regional sports networks if you do not watch local teams.",
   "Compare all-inclusive TV packages, which fold the fee into the price.",
   "Check whether the team you follow streams elsewhere for less."],
  [("Why do I pay a sports fee if I don't watch sports?", "Because your TV package includes regional sports channels. A package without them removes the fee."),
   ("Is the regional sports fee part of my promotional price?", "Usually not. Providers list it separately and can change it during the promotion.")],
  [("Xfinity: price changes and TV fees", "https://www.xfinity.com/pricechanges/"),
   ("HighSpeedInternet.com: what you actually pay for Optimum", "https://highspeedinternet.com/resources/optimum-real-costs")]),
 "equipment-rental-fee": ("Modem and router rental fee",
  "An equipment rental fee is a monthly charge for the modem, gateway or Wi-Fi router your provider lends you. Fiber providers usually include it; cable providers often charge for it, especially after a promotion ends. A compatible device you own can remove it.",
  "Your connection needs a modem (or a fiber terminal) and a Wi-Fi router, often combined in one gateway. Some providers include the gateway in the plan price; others bill it as its own line, sometimes free for a promotional period and charged afterwards.",
  [("AT&T Fiber", "No charge for standard equipment"),
   ("Verizon Fios", "Router included at no extra cost on current plans"),
   ("Frontier Fiber", "Router included on fiber"),
   ("T-Mobile 5G Home", "No rental fee for the gateway"),
   ("Spectrum", "Modem included; Advanced WiFi router billed monthly on some plans"),
   ("Cox", "Panoramic Wifi gateway, about $13 to $15/mo after the promo (reported)"),
   ("Optimum", "New plans include equipment; up to about $14/mo on some accounts after a promo (reported)"),
   ("CenturyLink / Quantum Fiber", "Leased modem and Wi-Fi about $15/mo")],
  ["Check your bill for a rental line, and whether your plan was supposed to include equipment.",
   "Buy a modem from your provider's approved list. At $13 to $15 a month, it usually pays for itself within a year.",
   "If you only rent the Wi-Fi router, any good router of your own can replace it.",
   "When you switch providers, return rented equipment on time to avoid unreturned-equipment charges."],
  [("Can I use my own modem?", "Usually yes on cable and DSL, if the model is on your provider's approved list. Fiber and 5G gateways are normally provider equipment, included in the price."),
   ("Is the rental fee covered by a price lock?", "Often not. Several providers exclude equipment fees from price guarantees.")],
  [("HighSpeedInternet.com: what you actually pay for AT&T", "https://www.highspeedinternet.com/resources/att-real-costs"),
   ("Verizon: Fios plans (router included)", "https://www.verizon.com/home/internet/fios-fastest-internet"),
   ("CableTV.com: Cox internet (Panoramic Wifi fee)", "https://www.cabletv.com/cox/internet?kbid=88450"),
   ("Quantum Fiber offer terms (lease fee)", "https://bgtm-027.dx.commercecloud.salesforce.com/s/QFCC/homepage.html")]),
 "recovery-and-regulatory-fees": ("Recovery and regulatory fees",
  "Charges such as a 'Regulatory Programs & Telco Recovery Fee' or an 'Administrative & Regulatory Cost Recovery Fee' are set by the provider, not the government. Because they sit outside the plan price, they can rise even on price-locked plans.",
  "Providers say these fees recover costs such as regulatory programs and connecting to other networks. They have official-sounding names, but the provider decides the amount. In 2026 T-Mobile raised its fee twice, most recently from October 12, and AT&T raised its wireless administrative fee from $4 to $5 per line from August 5.",
  [("T-Mobile", "Regulatory Programs & Telco Recovery Fee per line; raised October 12, 2026"),
   ("AT&T (wireless)", "Administrative & Regulatory Cost Recovery Fee, $4 to $5 per line from August 5, 2026"),
   ("Verizon (wireless)", "Administrative and Telco Recovery Charge per line")],
  ["Check whether your plan was sold with taxes and fees included; some are.",
   "Count the per-line charge on every line when comparing plans.",
   "Read the price-lock terms: most exclude these fees."],
  [("Is a regulatory recovery fee a tax?", "No. It is a provider charge. Taxes and government fees are listed separately."),
   ("Why did my bill go up if I have a price lock?", "Price locks cover the plan's base rate. Provider fees outside the plan price can still increase.")],
  [("Droid Life: T-Mobile fees increasing for the second time in 2026", "https://www.droid-life.com/2026/09/28/t-mobile-fees-increasing-on-your-bill-for-2nd-time-this-year/"),
   ("Android Authority: AT&T administrative fee rises to $5 per line", "https://www.androidauthority.com/p-3680584/")]),
 "data-overage-fee": ("Data overage fee",
  "A data overage fee is charged when you use more data than your plan's monthly cap. Most large home internet providers now include unlimited data, but check your bill: Cox has had a 1.25 TB cap with $10 per extra 50 GB.",
  "A data cap is a monthly allowance. Go over it and the provider charges in blocks (often $10 per 50 GB), sometimes up to a monthly maximum, or sells an unlimited-data add-on instead.",
  [("Spectrum", "No data caps"), ("AT&T Fiber", "Unlimited data"), ("Verizon Fios and 5G Home", "Unlimited data"),
   ("Frontier Fiber", "No data caps"), ("Xfinity", "Unlimited data on current internet plans (reported)"),
   ("Cox", "1.25 TB cap with $10 per 50 GB historically; a September 2026 report says caps were dropped"),
   ("T-Mobile Home Internet Backup", "130 GB per month on that backup plan")],
  ["Look for an overage or 'additional data' line on your last few bills.",
   "If you go over regularly, compare an unlimited plan's total with what you pay in overages.",
   "4K streaming uses the most data; lowering video quality on secondary TVs helps."],
  [("Do most internet plans have data caps?", "Not any more for most large providers. Check your plan's broadband label, which must list any cap.")],
  [("HighSpeedInternet.com: Cox internet review (data cap and overage)", "https://highspeedinternet.com/providers/cox/internet"),
   ("Programming Insider: what changed when Cox became Spectrum", "https://programminginsider.com/what-changed-when-cox-internet-became-spectrum/"),
   ("HighSpeedInternet.com: what you actually pay for Xfinity", "https://highspeedinternet.com/resources/xfinity-real-costs")]),
 "unreturned-equipment-fee": ("Unreturned equipment fee",
  "If you cancel and do not return rented equipment on time, providers charge for it, often $150 to $200 or more per device. Returning everything within the stated window avoids the charge.",
  "Rented modems, gateways, routers and TV boxes stay the provider's property. When you cancel or switch, you have a set number of days to return them; otherwise the replacement cost appears on your final bill.",
  [("Verizon Fios", "Return within 30 days of disconnecting or pay unreturned equipment fees"),
   ("Frontier", "$50 restocking fee per household plus up to $150 per unreturned device"),
   ("CenturyLink", "Up to $200 per piece of leased equipment if not returned")],
  ["Ask for a return label or the nearest drop-off store when you cancel.",
   "Keep the tracking number or store receipt until the final bill is $0.",
   "Photograph the serial numbers before you ship."],
  [("How long do I have to return equipment?", "It varies; Verizon and CenturyLink give 30 days. Ask when you cancel and get it in writing.")],
  [("Verizon: Fios equipment return terms", "https://www.verizon.com/info/fios-reviews-awards/"),
   ("Frontier: offer terms (restocking, unreturned equipment)", "https://go.frontier.com/id/mccall"),
   ("CenturyLink: switching to Quantum Fiber (unreturned equipment)", "https://www.centurylink.com/home/help/notices/move-to-quantum-fiber.html")]),
 "installation-and-activation-fee": ("Installation and activation fees",
  "Installation and activation fees are one-time charges to set up service. They are often waived for online orders or self-install, so ask before you book a technician.",
  "Providers charge to activate an account and, if you want one, to send a technician. Many waive one or both for online orders, self-install kits or bundles.",
  [("Spectrum", "Professional installation and self-install activation fees (reported $65 and $30)"),
   ("Verizon Fios", "$99 professional setup, often waived online or with Mobile + Home"),
   ("Frontier", "Activation charge in some offers (e.g. $85)")],
  ["Choose self-install when your home is already wired for the service.",
   "Order online if the provider waives fees for online orders.",
   "Ask the agent to waive activation as part of signing up; it is often possible."],
  [("Is professional installation worth paying for?", "If the home has never had the service or needs new wiring, yes. If it is a straight swap, self-install usually works.")],
  [("CableTV.com: hidden costs of Spectrum", "https://www.cabletv.com/spectrum/hidden-costs"),
   ("Verizon: Fios deals (setup fee waived)", "https://www.verizon.com/deals/fios"),
   ("Frontier: offer terms (activation)", "https://go.frontier.com/id/mccall")]),
}

def build_fees(save):
    for slug, (name, short, what, rows, avoid, faq, src) in FEES.items():
        others = " · ".join(f'<a href="/bills/fees/{s}">{esc(v[0])}</a>' for s, v in FEES.items() if s != slug)
        body = (author.box(CHECKED) + f'<div class="call tip"><b>Short answer</b>{esc(short)}</div>'
                f"<h2>What the {esc(lc(name))} is</h2><p>{esc(what)}</p>"
                f"<h2>{esc(name)} by provider</h2>" + table(["Provider", "What we found"], [(f"<b>{esc(a)}</b>", esc(b)) for a, b in rows])
                + f"<h2>How to avoid or lower it</h2><ol class=\"steps\">" + "".join(f"<li>{esc(t)}</li>" for t in avoid) + "</ol>"
                + f'<h2>Other charges on your bill</h2><p>{others} · <a href="/bills/fees">All fees</a> · <a href="/bills">Provider bill guides</a></p>'
                + cta() + srcs(src))
        save(f"/bills/fees/{slug}", ui.shell(f"/bills/fees/{slug}", f"What Is the {name} on My Bill? Amounts by Provider and How to Avoid It",
             f"What the {lc(name)} is, what Xfinity, Spectrum, Cox, Verizon and others charge, and how to avoid it. Sources listed, checked {CHECKED}.",
             f"What is the {lc(name)}?", esc(f"What it is, what providers charge and how to avoid it."), body, faq,
             [("Home", SITE + "/"), ("Lower your bill", SITE + "/bills"), ("Fees", SITE + "/bills/fees"), (name, SITE + f"/bills/fees/{slug}")],
             ["Fee explainer", "Sources listed"], date=DATE, checked=CHECKED, author=author.PERSON))
    cards = "".join(f'<a class="card" href="/bills/fees/{s}"><b>{esc(v[0])}</b><span>{esc(v[1][:110].rsplit(" ", 1)[0])}…</span></a>' for s, v in FEES.items())
    body = (author.box(CHECKED) + '<div class="call tip"><b>Short answer</b>Most surprise charges on an internet or TV bill are provider fees, not taxes: TV broadcast and sports fees, equipment rental, recovery fees, overages and one-time setup or non-return charges. Most are avoidable or negotiable.</div>'
            "<h2>Charges explained</h2><div class=\"grid\">" + cards + "</div>"
            '<p><a href="/bills">Bill guides by provider</a> · <a href="/guides/how-to-lower-your-internet-bill">How to lower your internet bill</a></p>' + cta())
    save("/bills/fees", ui.shell("/bills/fees", "Internet and TV Bill Fees Explained | YourBillCheck",
         "Every common internet and TV bill fee explained: broadcast TV, regional sports, equipment rental, recovery fees, overages, installation and unreturned equipment.",
         "Internet and TV bill fees explained", "What each charge on your bill means and how to avoid it.", body,
         [("Which internet bill fees can I avoid?", "Equipment rental, overages, installation and unreturned-equipment charges are usually avoidable. TV broadcast and sports fees go away only with a different TV setup.")],
         [("Home", SITE + "/"), ("Lower your bill", SITE + "/bills"), ("Fees", SITE + "/bills/fees")], ["Fee explainers"], date=DATE, checked=CHECKED, author=author.PERSON))

# ---------------- speed-test topic pages ----------------
NETFLIX = ("Netflix: recommended internet speeds", "https://help.netflix.com/en/node/306")
ZOOM = ("Zoom: calculating bandwidth usage for meetings", "https://library.zoom.com/admin-corner/network-management/quality-of-service-and-network-best-practices-explainer/calculating-bandwidth-usage-for-zoom-meetings-and-phone")
FCC = ("Benton Institute: FCC raises broadband benchmark to 100/20 Mbps", "https://www.benton.org/headlines/federal-communications-commission-increases-broadband-speed-benchmark")

TOPICS = {
 "streaming": ("Streaming Speed Test", "Is your internet fast enough to stream?",
  "Run the test, then compare your download speed with what Netflix recommends for HD and 4K.",
  table(["Video quality", "Netflix recommends"], [("HD (720p)", "3 Mbps or higher"), ("Full HD (1080p)", "5 Mbps or higher"), ("4K Ultra HD", "15 Mbps or higher")])
  + "<p>Those figures are per stream. Add them up for every TV, phone and tablet streaming at the same time, then leave room for everything else on the network. A home with three 4K TVs needs about 45 Mbps for video alone.</p>"
  "<h2>Buffering even though the test looks fine?</h2><ol class=\"steps\"><li>Test from the streaming device itself, or as close to it as possible.</li><li>Move the router into the open, or use a wired connection for the main TV.</li><li>Check whether others are downloading or backing up at the same time.</li><li>Restart the streaming device and the router.</li></ol>",
  [("How much speed do I need to stream 4K?", "Netflix recommends 15 Mbps or higher per 4K stream."), ("Why does Netflix buffer when my speed test is fast?", "Wi-Fi to the TV is often slower than the test device's connection. Test near the TV or use Ethernet.")],
  [NETFLIX]),
 "zoom": ("Zoom and Video Call Speed Test", "Is your internet good enough for Zoom and video calls?",
  "Video calls depend on upload speed and stable ping as much as download. Run the test and compare with Zoom's numbers.",
  table(["Zoom meeting", "Upload", "Download"], [("1080p HD video", "3.8 Mbps", "3.0 Mbps")])
  + "<p>Those are per person on the call from your home. Two people working from home on HD calls need about 8 Mbps upload. Ping under 50 ms and low jitter keep audio from cutting out.</p>"
  "<h2>Calls freezing or robotic audio?</h2><ol class=\"steps\"><li>Check upload speed and jitter in the result, not only download.</li><li>Plug the laptop into the router with a cable for important calls.</li><li>Pause cloud backups and large uploads during calls.</li><li>Turn off your video for a moment to see if audio improves; if it does, upload is the bottleneck.</li></ol>",
  [("What internet speed do I need for Zoom?", "Zoom estimates 3.8 Mbps upload and 3.0 Mbps download for 1080p HD meetings."), ("Why is my upload so much slower than download?", "Cable and 5G plans usually have far less upload than download. Fiber plans normally have matching upload.")],
  [ZOOM]),
 "gaming": ("Gaming Ping Test", "Ping test for gaming: is your connection good enough?",
  "For online games, ping (latency) and jitter matter more than raw download speed. Run the test and check the ping and jitter figures.",
  table(["Ping", "What it feels like"], [("Under 20 ms", "Excellent; ideal for competitive shooters"), ("20 to 50 ms", "Good for almost every game"), ("50 to 100 ms", "Playable, but you may notice lag in fast games"), ("Over 100 ms", "Noticeable lag; check Wi-Fi and network load")])
  + "<p>These bands are general guidance, not a game publisher's requirement. Downloads of new games and updates are where download speed matters, so a faster plan shortens update times.</p>"
  "<h2>Lowering ping</h2><ol class=\"steps\"><li>Use a wired connection for the console or PC.</li><li>Stop large downloads and streams while you play.</li><li>Choose the game server region closest to you.</li><li>If ping is high even on a cable, fiber usually gives lower latency than cable, 5G or satellite.</li></ol>",
  [("What is a good ping for gaming?", "Under 50 ms works well for most games; under 20 ms is ideal for competitive play."), ("Is satellite internet good for gaming?", "Usually not for fast games, because latency is higher than on wired connections.")],
  []),
 "upload": ("Upload Speed Test", "Upload speed test: how fast can you send data?",
  "Upload speed affects video calls, cloud backups, posting videos and working from home. Run the test and compare your upload with the broadband benchmark.",
  "<p>The FCC's benchmark for fixed broadband is 100 Mbps download and 20 Mbps upload. If your upload is well under 20 Mbps, video calls and backups will compete with each other.</p>"
  + table(["Connection type", "Typical upload"], [("Fiber", "Usually matches download (symmetrical)"), ("Cable", "Much lower than download"), ("5G home internet", "Lower than download, varies by signal"), ("DSL and satellite", "Lowest")])
  + "<h2>Need more upload?</h2><p>Upload is mostly set by the connection type. If you work from home or create content, fiber is the biggest upgrade. Enter your ZIP code to see whether fiber is reported at your address.</p>",
  [("What is a good upload speed?", "The FCC's broadband benchmark is 20 Mbps upload. Working from home with video calls is comfortable at 20 Mbps or more."), ("Why is my upload speed slow?", "Most cable and 5G plans give much less upload than download. Fiber plans usually have matching upload and download.")],
  [FCC]),
 "wifi": ("Wi-Fi Speed Test", "Wi-Fi speed test: is it your Wi-Fi or your internet?",
  "Run the test twice: once on Wi-Fi where the problem happens, and once next to the router (or plugged in with a cable). The difference tells you where the problem is.",
  table(["Result", "What it means"], [("Slow on Wi-Fi, fast on cable", "Your internet is fine; the Wi-Fi is the bottleneck"), ("Slow on both", "The connection or plan is the problem"), ("Fast near the router, slow far away", "Coverage problem: move the router or add a mesh point")])
  + "<h2>Fixing slow Wi-Fi</h2><ol class=\"steps\"><li>Put the router up high, in the open, near the middle of the home.</li><li>Use the 5 GHz or 6 GHz band for devices close to the router.</li><li>Restart the router and update its firmware.</li><li>For larger homes, a mesh system covers far better than one router.</li></ol>",
  [("Why is Wi-Fi slower than my plan?", "Walls, distance, older devices and neighbours' networks all reduce Wi-Fi speed. A wired test shows the real line speed.")],
  []),
 "is-my-internet-slow": ("Is My Internet Slow?", "Is my internet slow, or am I paying for speed I don't get?",
  "Run the test and compare the download result with the speed on your bill. If it is consistently far below, you may be paying for speed you are not getting.",
  "<h2>Compare with your plan</h2><ol class=\"steps\"><li>Find your plan speed on your bill or in your provider's app.</li><li>Run this test three times with a computer plugged in by cable.</li><li>If wired results are consistently below 70 to 80 percent of the plan, restart the modem and test again.</li><li>Still low? Contact your provider with the results, or ask for a credit.</li></ol>"
  "<p>The FCC benchmark for fixed broadband is 100 Mbps download and 20 Mbps upload. If you pay for a faster plan but get less than that, it is worth a call to your provider, or a look at other providers at your address.</p>"
  '<div class="call tip"><b>Paying for speed you don\'t get?</b>See <a href="/bills">why bills go up and how to get a lower rate</a>, or <a href="/help/slow-internet">fix slow internet</a> step by step.</div>',
  [("How do I know if my internet is slow?", "Compare a wired speed test with the speed on your bill. Consistently far below means a problem with the line, the equipment or the plan."), ("Can I get a credit for slow internet?", "Sometimes. Contact your provider with dated speed test results and ask.")],
  [FCC]),
}

def build_speed(ST_BODY, save):
    for slug, (name, h1, lead, extra, faq, src) in TOPICS.items():
        others = " · ".join(f'<a href="/speed-test/{s}">{esc(v[0])}</a>' for s, v in TOPICS.items() if s != slug)
        body = (ST_BODY + f"<h2>{esc(h1)}</h2>" + extra
                + f'<h2>More speed tests</h2><p><a href="/speed-test">Main speed test</a> · {others} · <a href="/speed-test/xfinity">Xfinity</a> · <a href="/speed-test/spectrum">Spectrum</a> · <a href="/speed-test/att">AT&amp;T</a></p>'
                + (srcs(src) if src else ""))
        save(f"/speed-test/{slug}", ui.shell(f"/speed-test/{slug}", f"{name}: Free Online Test | YourBillCheck",
             esc(lead)[:155], h1, esc(lead), body, faq,
             [("Home", SITE + "/"), ("Speed test", SITE + "/speed-test"), (name, SITE + f"/speed-test/{slug}")],
             ["Free test", "No app needed"], date=DATE, checked=CHECKED))
