"""Wave 1 of the 50-page SEO plan: bill-went-up pages, /save pages, guides, fee pillar and three new fee explainers.
Every page: named author, sources, checked date. Facts checked November 24, 2026. Where a source is a news report
rather than the provider, the page says "reported"."""
import html
import ui, author
import build_bills as BB
import build_extra as BE

esc = lambda s: html.escape(str(s), quote=True)
SITE = "https://yourbillcheck.com"
CHECKED = "November 24, 2026"
DATE = "2026-11-24"
TEL = BE.PHONE_TEL
TXT = BE.PHONE_TXT

# ---------------------------------------------------------------- new fee explainers (merged into build_extra.FEES)
BE.FEES["spectrum-wifi-fee"] = ("Spectrum Wi-Fi fee",
  "Spectrum includes the modem but charges a monthly fee when you use a Spectrum Wi-Fi router. Reports put the fee at $5 to $10 a month depending on the plan, and it is $0 if you use your own router.",
  "Spectrum's modem is included. If you also want Spectrum to supply the Wi-Fi router, it bills that as a Wi-Fi service fee. Some higher tiers include Advanced Wi-Fi in the plan price, while lower tiers charge for it, and Wi-Fi extenders (pods) are billed separately. If you connect your own router to Spectrum's modem, no Wi-Fi fee applies.",
  [("Standard Spectrum Wi-Fi router", "$5/mo reported (BroadbandNow, CableTV.com)"),
   ("Advanced Wi-Fi", "$10/mo on lower tiers; included on Spectrum's Gig and 2 Gig plans (WhistleOut, 2026)"),
   ("Wi-Fi extenders (pods)", "Reported at $3 to $5/mo each depending on the date and plan"),
   ("Your own router", "No Wi-Fi fee. The modem is included.")],
  ["Check your bill for a line named Wi-Fi, Advanced Wi-Fi or Wi-Fi service.",
   "If you stay more than a year, a router you own pays for itself: about $60 a year saved at $5 a month, $120 a year at $10 a month, against roughly $100 for a good router.",
   "Ask whether your tier includes Advanced Wi-Fi before you accept a charge for it.",
   "Remove pods you do not use. Each one adds its own monthly line."],
  [("Is the Spectrum Wi-Fi fee mandatory?", "No. It applies only if you use a Spectrum-supplied Wi-Fi router. With your own router there is no Wi-Fi fee, but Spectrum support can only help with equipment it supplies."),
   ("Why did a Wi-Fi fee appear on my bill?", "Usually because the plan changed, a promotion that covered it ended, or a router or pod was added. Look at the date it first appears and call to ask what triggered it.")],
  [("CableTV.com: hidden costs of Spectrum", "https://www.cabletv.com/spectrum/hidden-costs"),
   ("BroadbandNow: Spectrum Internet deals (Wi-Fi fee and own router)", "https://broadbandnow.com/Spectrum-Internet-deals"),
   ("WhistleOut: Spectrum Internet 500 Mbps (Advanced Wi-Fi by tier)", "https://www.whistleout.com/Internet/Providers/Charter-Spectrum/Fiber/Spectrum-Internet-500Mbps")])
BE.TITLES["spectrum-wifi-fee"] = "Spectrum WiFi Fee Explained: What It Is and How to Avoid It"

BE.FEES["xfinity-data-overage"] = ("Xfinity data cap and overage charge",
  "On Xfinity plans that still have a data allowance, going over 1.2 TB costs $10 for each extra 50 GB, up to $100 a month. Newer Xfinity internet plans come with unlimited data, and an unlimited add-on is sold for older ones.",
  "Some older Xfinity plans include 1.2 TB of data a month. If you use more, Xfinity automatically adds a 50 GB block and charges $10 plus tax for each, capped at $100 a month. Xfinity says you can avoid the charges by moving to a current plan with unlimited data or adding Unlimited Data (or xFi Complete where it is sold). Reviewers report the add-on at about $30 a month, so three overage blocks in a month already cost as much as unlimited.",
  [("Xfinity (legacy data plan)", "1.2 TB allowance, then $10 per 50 GB, maximum $100/mo"),
   ("Xfinity (current plans)", "Unlimited data (reported Jan 2026)"),
   ("Xfinity Unlimited Data add-on", "About $30/mo reported"),
   ("Cox", "Historically 1,280 GB with $10 per 50 GB"),
   ("AT&T Internet", "Some plans 1,024 GB with $10 per 50 GB; unlimited on faster plans"),
   ("Spectrum, Verizon Fios, Frontier, Optimum", "No data caps")],
  ["Look at the Internet section of your bill for a usage charge, and in the Xfinity app for data usage.",
   "If you went over once, ask about the courtesy month: Xfinity does not charge the first time you exceed the allowance.",
   "If you go over most months, compare three or more $10 blocks against the unlimited add-on or a current plan.",
   "Ask for a move to a current unlimited plan rather than paying for the add-on. It may cost the same or less."],
  [("Does Xfinity still have data caps?", "Reports in 2026 say current Xfinity internet plans include unlimited data, but older plans can still carry a 1.2 TB allowance. Your bill shows which you have."),
   ("What is the most Xfinity can charge for data overage?", "$100 a month, according to Xfinity's own support page."),
   ("How much data is 1.2 TB?", "Roughly 400 hours of HD streaming, but 4K video, game downloads and cloud backups can use it much faster in a large household.")],
  [("Xfinity: data usage and overage charges", "https://www.xfinity.com/support/internet/data-usage-exceed-usage"),
   ("Xfinity: data usage plan", "https://www.xfinity.com/support/articles/data-usage-plan"),
   ("CableTV.com: Xfinity data cap and unlimited add-on", "https://www.cabletv.com/xfinity/internet/data-cap"),
   ("HighSpeedInternet.com: what you actually pay for Xfinity (Jan 2026)", "https://highspeedinternet.com/resources/xfinity-real-costs")])
BE.TITLES["xfinity-data-overage"] = "Xfinity Data Cap and Overage Charges Explained"

BE.FEES["verizon-administrative-charge"] = ("Verizon Administrative and Telco Recovery Charge",
  "The Administrative and Telco Recovery Charge is a monthly per-line charge on Verizon wireless bills. Verizon says it is not a tax and not required by the government, and that it can change. It does not apply to Verizon Fios home internet bills as a separate item.",
  "Verizon describes this charge as recovering certain administrative and telco costs, including regulatory and industry compliance (such as E911 and number portability), property taxes, and network facilities, operations and maintenance. It was renamed from the Administrative Charge in June 2022 and is billed on each line. Verizon's own support page says it is not a governmental tax or government-imposed fee, and its page excludes 5G Home Internet and LTE Home Internet from the latest increase. Separately, Verizon lists a Regulatory Charge that rose from $0.21 to $0.26 per voice line on November 1, 2026.",
  [("Verizon Wireless phone lines", "Billed per line; rose from $1.95 in 2022 to $3.30 by 2024, then +$0.20 on Dec 18, 2024 (reported)"),
   ("Verizon data-only devices (tablets, hotspots)", "Also billed per device"),
   ("Verizon 5G / LTE Home Internet", "Excluded from the latest increase, per Verizon"),
   ("Verizon Fios", "Fios bills carry other lines, such as the Fios TV broadcast fee; this wireless charge is not part of Fios internet"),
   ("AT&T and T-Mobile (comparison)", "AT&T Administrative and Regulatory Cost Recovery Fee; T-Mobile Regulatory Programs and Telco Recovery Fee")],
  ["Find the line on your bill and multiply it by your number of lines to see the yearly cost.",
   "When comparing plans, count the per-line charge. It is not part of the advertised price.",
   "Ask whether a plan advertised as 'taxes and fees included' covers it.",
   "Remove lines or devices you do not use; the charge is per line."],
  [("Is the Administrative and Telco Recovery Charge a tax?", "No. Verizon says it is not a governmental tax or a government-imposed fee."),
   ("Can I get it removed?", "Not as a separate item. It applies to every line, so the practical way to lower it is to cancel lines you do not use or compare carriers' all-in prices."),
   ("Did Verizon settle a lawsuit over this charge?", "Verizon agreed to a settlement of a lawsuit over how the administrative fee was disclosed and said it denied wrongdoing. It also said it will keep charging the fee and may raise it.")],
  [("Verizon: about taxes, fees and mobile surcharges", "https://www.verizon.com/support/surcharges"),
   ("Android Authority: Verizon administrative charge rises $0.20 per line (Dec 2024)", "https://www.androidauthority.com/verizon-admin-fee-increase-3505347"),
   ("Android Authority: Verizon settlement and continued charge", "https://www.androidauthority.com/verizon-administrative-and-telco-recovery-charge-2024-3403672")])
BE.TITLES["verizon-administrative-charge"] = "Verizon Administrative and Telco Recovery Charge Explained"

# ---------------------------------------------------------------- helpers
def page(path, title, desc, h1, lead, body, faq, crumbs, chips):
    return ui.shell(path, title, desc, h1, lead, body, faq, crumbs, chips, date=DATE, checked=CHECKED, author=author.PERSON)

def faqs(lst):
    return [(q, esc(a)) for q, a in lst]

def steps(items):
    return '<ol class="steps">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"

def tbl(head, rows):
    return BE.table(head, [[c for c in r] for r in rows])

def a(href, text):
    return f'<a href="{href}">{esc(text)}</a>'

def src(lst):
    return BE.srcs(lst)

def short(txt):
    return f'<div class="call tip"><b>Short answer</b>{esc(txt)}</div>'

def warn(title, txt):
    return f'<div class="call warn"><b>{esc(title)}</b>{esc(txt)}</div>'

# ---------------------------------------------------------------- 1. "why did my X bill go up" pages
WENT = {
 "xfinity": dict(slug="xfinity-bill-went-up", name="Xfinity", kw="why did my xfinity bill go up", save="/save/lower-xfinity-bill", bill="/bills/xfinity",
   short="Xfinity bills usually go up because a promotion or price guarantee ended, a TV fee or equipment charge changed, or a discount such as Auto Pay was lost. Xfinity also says some prices will increase starting December 2026, without giving amounts yet.",
   rows=[("December 2026", "Xfinity says \"some of our prices will increase\" starting December 2026. The page gives no dollar amounts and says TV costs are tied to programmers' price increases.", "Some services; check your bill notice", "Xfinity"),
         ("When a promotion ends", "Reviewers report the bill can rise by about $20 to $55 a month when a 12-month promotion ends.", "Customers on 12-month promotions", "Reviewer report"),
         ("During a promotion", "Xfinity says the service price stays the same during a promotional rate or minimum-term agreement, but taxes, fees and equipment charges may change.", "Everyone on a promo or price guarantee", "Xfinity"),
         ("Early 2026 onward", "New all-inclusive TV packages fold the Broadcast TV and Regional Sports fees into one price. Legacy TV packages keep them as separate lines.", "TV customers", "Xfinity"),
         ("Paperless + Auto Pay", "Xfinity internet customers can save $10 a month with paperless billing and automatic payments from a bank account. Losing that setup raises the bill by the same amount.", "Internet customers", "Xfinity")],
   find=["Sign in to your Xfinity account, open the latest bill and read the important information section. Xfinity points customers there for what changed.",
         "Compare the last two bills line by line: internet, TV, equipment, Broadcast TV Fee, Regional Sports Fee, add-ons and taxes.",
         "Check the end date of your promotion or price guarantee in the app. A guarantee covers the base internet rate, not fees or equipment."],
   more=[("/fees/broadcast-tv-fee", "Broadcast TV fee"), ("/fees/regional-sports-fee", "Regional sports fee"), ("/fees/modem-router-rental-fee", "Modem and router rental"), ("/fees/xfinity-data-overage", "Xfinity data overage")],
   faq=[("Is Xfinity raising prices in 2026?", "Xfinity says some prices will increase starting in December 2026 and has not published amounts. Promotions and minimum-term agreements protect the service price but not taxes, fees or equipment."),
        ("Why did my Xfinity bill go up when my promotion has not ended?", "Fees, equipment charges, TV fees or add-ons can change during a promotion. A lost Auto Pay or paperless discount can also add $10 a month."),
        ("Does the 5-year price guarantee stop my bill from going up?", "It locks the qualifying base internet rate. Taxes, fees and equipment charges are not covered.")],
   src=[("Xfinity: price changes", "https://www.xfinity.com/pricechanges/"),
        ("Xfinity: broadcast TV and regional sports fees in new TV packages", "https://www.xfinity.com/pricechange/?linkId=110641971"),
        ("HighSpeedInternet.com: what you actually pay for Xfinity (Jan 2026)", "https://highspeedinternet.com/resources/xfinity-real-costs")]),
 "spectrum": dict(slug="spectrum-bill-went-up", name="Spectrum", kw="why did my spectrum bill go up", save="/save/lower-spectrum-bill", bill="/bills/spectrum",
   short="The most common reasons a Spectrum bill goes up are a $10 increase on legacy internet plans reported from June and July 2026, a promotion ending, and Wi-Fi equipment fees. Current Spectrum plans were not part of the 2026 increase.",
   rows=[("June to July 2026", "Spectrum confirmed a $10 monthly increase for customers on legacy Flagship, Ultra and Gig internet plans. Most of those customers also got faster speeds (Flagship 400 to 500 Mbps, Ultra 600 Mbps to Gig). Legacy TV Essentials rose $4, from $31 to $35.", "Legacy plan customers", "Cord Cutters News"),
         ("July 2024", "Spectrum raised internet prices about $3 a month, and about $4 on retired plans.", "Many internet customers", "The Desk"),
         ("Promotions", "Several Spectrum tiers are introductory rates that move to a standard rate later. Spectrum has also offered price guarantees of one to three years on some plans.", "Customers on promo plans", "WhistleOut, Yahoo Finance"),
         ("Wi-Fi equipment", "A Spectrum-supplied Wi-Fi router is billed monthly, reported at $5 to $10 depending on the plan, and Wi-Fi pods are billed separately.", "Customers using Spectrum Wi-Fi", "CableTV.com, WhistleOut")],
   find=["Check your plan name on the bill. If it says Flagship, Ultra or Gig rather than a current plan name, you are on a legacy plan.",
         "Look for a bill message or notice. The June 2026 changes were communicated to customers before they took effect.",
         "Look for lines named Wi-Fi, Advanced Wi-Fi or Wi-Fi pod and note when they first appeared."],
   more=[("/fees/spectrum-wifi-fee", "Spectrum Wi-Fi fee"), ("/fees/broadcast-tv-fee", "Broadcast TV fee"), ("/fees/modem-router-rental-fee", "Modem and router rental")],
   faq=[("Why did my Spectrum bill go up $10?", "If you are on a legacy Flagship, Ultra or Gig internet plan, Spectrum confirmed a $10 increase reported from June and July 2026. Check your plan name and bill notice."),
        ("Can I avoid the Spectrum increase?", "Reports say current Spectrum plans were not part of the 2026 increase, so ask the agent to price a current plan at your address and compare it with your legacy rate."),
        ("Does Spectrum charge for the modem?", "Spectrum's modem is included. The Wi-Fi router is billed separately if you use Spectrum's, and not at all if you use your own.")],
   src=[("Cord Cutters News: another big price hike for Spectrum customers", "https://cordcuttersnews.com/another-big-price-hike-is-coming-to-spectrum-customers/"),
        ("The Desk: Spectrum price adjustment, July 2024", "https://thedesk.net/2024/06/spectrum-tv-internet-fee-increase-july-2024/"),
        ("WhistleOut: Spectrum Internet 500 Mbps (introductory rates, Wi-Fi)", "https://www.whistleout.com/Internet/Providers/Charter-Spectrum/Fiber/Spectrum-Internet-500Mbps")]),
 "att": dict(slug="att-bill-went-up", name="AT&T", kw="at&t internet bill went up", save="/save/lower-att-internet-bill", bill="/bills/att",
   short="AT&T has raised home internet prices by $5 a month in several rounds, including a Dec 1, 2025 increase on AT&T Fiber and AT&T Internet and a reported August 16, 2026 increase on some plans, so a $5 jump on your bill is likely one of them.",
   rows=[("Late 2024", "A $5 monthly increase on home internet plans, reported by The Verge.", "Home internet customers", "Reported"),
         ("December 1, 2025", "AT&T's support page says the monthly price of AT&T Fiber and AT&T Internet goes up by $5.", "AT&T Fiber and AT&T Internet", "AT&T"),
         ("June 7, 2026", "New fiber plan tiers launched. Reports put the lowest tier at $35 a month and the 1 Gig plan at $80 alone or $60 with a wireless plan. The 5 Gig plan fell from $140 to $125.", "New and switching customers", "Broadband Breakfast, HighSpeedInternet.com"),
         ("August 16, 2026", "Reported from internal AT&T documents: another $5 increase for fiber and copper plans started between June 2024 and July 2025, and the $15 Access from AT&T copper plan rising to $20.", "Customers on those plans", "Reported, not confirmed by AT&T")],
   find=["Open your bill and look in the News You Can Use section for a note about a change to your monthly plan price.",
         "Check your Auto Pay discount: AT&T has offered up to $10 off a month for bank Auto Pay and $5 for debit, applied within two bill periods after enrollment.",
         "Compare your price with the plan names AT&T sells today. A newer tier can cost less than an older one for the same speed."],
   more=[("/fees/modem-router-rental-fee", "Modem and router rental"), ("/fees/xfinity-data-overage", "Data overage by provider")],
   faq=[("Why did my AT&T internet bill go up $5?", "AT&T raised Fiber and AT&T Internet prices by $5 starting December 1, 2025, and reports describe another $5 increase from August 16, 2026 for some plans."),
        ("Is AT&T Fiber price locked?", "AT&T has marketed price guarantees on some plans, but customers have reported increases anyway. Read the terms of the plan you signed up for and check what the guarantee covers."),
        ("Can I get a lower AT&T bill?", "Ask about Auto Pay and paperless discounts, check whether a newer plan tier costs less, and call the loyalty department with the new-customer price you see online.")],
   src=[("AT&T: details about your internet price change", "https://www.att.com/support/article/u-verse-high-speed-internet/KM1260426/"),
        ("Broadband Breakfast: AT&T launches new fiber plans (June 2026)", "https://broadbandbreakfast.com/at-t-launches-new-fiber-plans/"),
        ("HighSpeedInternet.com: AT&T changes fiber prices", "https://highspeedinternet.com/resources/att-changes-fiber-prices"),
        ("Android Authority: AT&T price hike, August 2026", "https://www.androidauthority.com/att-price-hike-august-2026-3689162/")]),
 "verizon": dict(slug="verizon-fios-bill-went-up", name="Verizon Fios", kw="verizon fios bill went up", save="/bills/verizon", bill="/bills/verizon",
   short="A Verizon Fios bill usually rises because a promotion, price guarantee or discount ended, an Auto Pay credit shrank, a miscellaneous charge increased, or TV fees such as the Fios TV broadcast fee changed. We did not find a confirmed 2026 Fios internet price increase.",
   rows=[("January 2025", "Fios customers reported a $5 increase labeled as a miscellaneous charges increase.", "Some Fios customers", "Reported"),
         ("Auto Pay credit", "A customer reported being told the Auto Pay credit dropped from $10 to $5 on older Fios 300 and lower plans, which raised the bill $5.", "Older low-tier plans", "Customer report"),
         ("Fios TV broadcast fee", "Verizon's glossary describes it as a monthly fee charged by local programming providers for basic channels, and says it is subject to change.", "Fios TV customers", "Verizon"),
         ("November 1, 2026", "Verizon's Regulatory Charge rose from $0.21 to $0.26 per voice line. This is a wireless-line item, not Fios internet.", "Verizon Wireless lines", "Verizon"),
         ("Bundles and discounts", "Discounts tied to Auto Pay or a mobile bundle disappear if you stop using the qualifying service, and the bill rises by that amount.", "Customers who changed mobile or payment setup", "General")],
   find=["Compare the last two bills and look for a changed Auto Pay or mobile-bundle credit.",
         "Check the Fios TV section for the broadcast fee and any sports fees.",
         "If your bill combines Fios and Verizon Wireless, separate the two. Wireless per-line charges are a different set of fees."],
   more=[("/fees/verizon-administrative-charge", "Verizon administrative charge"), ("/fees/broadcast-tv-fee", "Broadcast TV fee"), ("/fees/regional-sports-fee", "Regional sports fee")],
   faq=[("Why did my Verizon Fios bill go up?", "Common causes are an ended promotion or discount, a reduced Auto Pay credit, a miscellaneous charge increase reported in 2025, and TV fees. Compare the last two bills line by line."),
        ("Did Verizon raise Fios prices in 2026?", "We did not find a confirmed 2026 Fios internet price increase. Verizon did raise a wireless Regulatory Charge on November 1, 2026."),
        ("Is the Verizon administrative charge on my Fios bill?", "It is a per-line wireless charge. Fios internet does not carry it as a separate item.")],
   src=[("PhoneArena: Fios customers report a $5 increase (Jan 2025)", "https://www.phonearena.com/news/Second-Verizon-price-hike-announced-in-less-than-a-month_id166996"),
        ("Verizon: billing glossary (Fios TV broadcast fee)", "https://verizon.com/support/residential/account/understand-bill/billing-glossary"),
        ("Verizon: about taxes, fees and mobile surcharges", "https://www.verizon.com/support/surcharges")]),
 "cox": dict(slug="cox-bill-went-up", name="Cox", kw="why did my cox bill go up", save="/bills/cox", bill="/bills/cox",
   short="Cox bills have gone up in 2026 from reported $5 increases on 500 Mbps and 1 Gig plans, promotions ending, and equipment and data charges. Cox is also moving into Spectrum, and existing promotions are being honored.",
   rows=[("Early 2026", "Price trackers report a $5 monthly increase on Cox's 500 Mbps and 1 Gig plans. Sources disagree on the exact tiers and totals.", "500 Mbps and 1 Gig plans", "Reported"),
         ("2026 merger with Spectrum", "As reported in September 2026, Cox customers keep their current pricing and equipment for now, existing promotions are honored, and customers are not forced onto Spectrum plans.", "All Cox customers", "CableTV.com"),
         ("Promotions", "Cox promotions end into a standard rate. Compare your current rate with the new-customer price shown for your address.", "Customers on promo plans", "General"),
         ("Data cap", "Cox plans have historically carried a 1,280 GB allowance with $10 per extra 50 GB. Check your plan for a cap.", "Customers on capped plans", "CableTV.com")],
   find=["Read the notice that came with your bill. Cox customers have reported notices dated close to the billing date.",
         "Check for a Panoramic Wifi or equipment line, reported at about $13 to $15 a month after a promotion.",
         "Look for a data usage or overage line on your last few bills."],
   more=[("/fees/modem-router-rental-fee", "Modem and router rental"), ("/fees/xfinity-data-overage", "Data caps by provider")],
   faq=[("Why did my Cox bill go up?", "Common reasons are a promotion ending, a reported $5 increase on 500 Mbps and 1 Gig plans in early 2026, equipment rental and data overage charges."),
        ("Is Cox becoming Spectrum?", "Reports in September 2026 describe Cox becoming part of Spectrum. Cox customers keep current pricing and equipment for now, and existing promotions are honored."),
        ("Do I have to switch to Spectrum?", "Reports say customers are not forced onto Spectrum plans, and that those who want a Spectrum plan need to call Spectrum.")],
   src=[("CableTV.com: Cox-Spectrum merger and prices", "https://www.cabletv.com/news/cox-spectrum-merger-will-price-increase"),
        ("CompareInternet: internet price increase 2026 tracker", "https://www.compareinternet.com/blog/internet-price-increase-2026/"),
        ("CableTV.com: internet provider data caps", "https://www.cabletv.com/internet/brand-data-caps")]),
}

def LOCAL(n):
    st = [("tx","Texas"),("ca","California"),("fl","Florida"),("ny","New York"),("ga","Georgia"),("pa","Pennsylvania"),("il","Illinois"),("oh","Ohio")]
    return (f"<h2>Check if a cheaper provider serves you</h2><p>If {esc(n)} keeps raising your price, see who else offers internet at your address. "
            "Enter your ZIP code, or pick your state.</p>"
            '<form class="yf-zip" style="max-width:360px;margin:0 0 12px" onsubmit="var z=this.z.value.trim();if(/^\\d{5}$/.test(z)){location.href=\'/internet/\'+z}return false">'
            '<input name="z" inputmode="numeric" maxlength="5" placeholder="Enter ZIP code" aria-label="ZIP code"> <button type="submit">Check providers</button></form>'
            "<p>" + " · ".join(f'<a href="/internet/{c}">{s} internet providers</a>' for c, s in st) + ' · <a href="/internet">All states</a></p>')

def build_went(save):
    for k, d in WENT.items():
        n = d["name"]; path = "/bills/" + d["slug"]
        links = " · ".join(a(h, t) for h, t in d["more"])
        body = (author.box(CHECKED) + short(d["short"])
                + f"<h2>What changed on {esc(n)} bills</h2>"
                + tbl(["When", "What changed", "Who it affects", "Source"], [(f"<b>{esc(w)}</b>", esc(x), esc(y), esc(z)) for w, x, y, z in d["rows"]])
                + f"<h2>How to find out why your {esc(n)} bill went up</h2>" + steps([esc(s) for s in d["find"]])
                + f"<h2>What you can do about it</h2><ol class=\"steps\">" + "".join(f"<li>{esc(t)}</li>" for t in BB.B[k]["tips"]) + "</ol>"
                + f'<p>Ready to act? <a href="{d["save"]}">Step-by-step: lower your {esc(n)} bill</a> · <a href="{d["bill"]}">Full {esc(n)} fee guide</a> · <a href="/guides/internet-price-increases-2026">2026 price increase tracker</a></p>'
                + f"<h2>Related charges</h2><p>{links}</p>" + LOCAL(n) + BB.call_cta(n) + src(d["src"]))
        TITLE_OVERRIDE = {"spectrum": "Spectrum Bill Went Up? Why and How to Lower It (2026)",
                          "att": "AT&T Bill Went Up? Why and How to Lower It (2026)"}
        title = TITLE_OVERRIDE.get(k, f"Why Did My {n} Bill Go Up? What Changed in 2026")
        save(path, page(path, title, f"Why your {n} bill went up: price increases, promotions ending, fees and lost discounts, with dates and sources. Checked {CHECKED}.",
             f"Why did my {n} bill go up?", f"What changed on {esc(n)} bills, how to find the line that rose, and what to do about it.", body, faqs(d["faq"]),
             [("Home", SITE + "/"), ("Lower your bill", SITE + "/bills"), (f"{n} bill went up", SITE + path)], ["Bill increase", "Sources listed"]))

# ---------------------------------------------------------------- 2. "lower your X bill" pages
SAVE = {
 "xfinity": dict(slug="lower-xfinity-bill", name="Xfinity", went="/bills/xfinity-bill-went-up", bill="/bills/xfinity",
   short="To lower an Xfinity bill, check your promotion end date, ask for a current plan with a price guarantee, turn on paperless billing plus bank Auto Pay for $10 a month, drop legacy TV fees, and use your own modem. If Xfinity will not move, compare other providers at your address.",
   asks=[("Move me to a current plan with a price guarantee", "Xfinity sells a 5-year price guarantee on eligible new internet plans. It locks the qualifying base monthly rate for 60 months. It does not cover taxes, fees or equipment."),
         ("Apply the Auto Pay and paperless credit", "Xfinity says internet customers save $10 a month with paperless billing and automatic payments from a bank account."),
         ("Price an all-inclusive TV package", "Xfinity's newer 2026 TV packages fold the Broadcast TV and Regional Sports fees into one price. Ask whether that costs less than your legacy package plus its separate fee lines."),
         ("Remove equipment rental", "If you rent a gateway, a compatible modem you own removes that line. Check your plan: some include the gateway."),
         ("Move me off a data allowance", "Legacy plans can have a 1.2 TB allowance with $10 per 50 GB overage. Ask for a current plan with unlimited data."),
         ("Ask about bundled mobile offers", "Xfinity has run offers with mobile lines included with internet. Ask what is available now, and what the price is when the offer ends.")],
   alt="If Xfinity will not match what new customers pay, check which fiber and 5G home internet providers report service at your ZIP code. Fiber providers often include equipment and have fewer separate fees.",
   src=[("Xfinity: price changes", "https://www.xfinity.com/pricechanges/"),
        ("Xfinity: data usage and overage", "https://www.xfinity.com/support/internet/data-usage-exceed-usage"),
        ("HighSpeedInternet.com: what you actually pay for Xfinity (Jan 2026)", "https://highspeedinternet.com/resources/xfinity-real-costs"),
        ("FindCheapBroadband: Xfinity 5-year price guarantee", "https://findcheapbroadband.com/blog/xfinity-internet-price-increase-2026/")]),
 "spectrum": dict(slug="lower-spectrum-bill", name="Spectrum", went="/bills/spectrum-bill-went-up", bill="/bills/spectrum",
   short="To lower a Spectrum bill, ask to move from a legacy plan to a current plan, use your own router to remove the Wi-Fi fee, check the price lock on the new plan, and mention fiber or 5G home internet if they are available at your address.",
   asks=[("Move me from a legacy plan to a current plan", "Reports say the 2026 $10 increase applied to legacy Flagship, Ultra and Gig plans and not to current plans. Ask the agent to price Internet 500 or 1 Gig at your address and compare it with your legacy rate."),
         ("Confirm the price guarantee", "Spectrum has offered one-year and three-year price guarantees depending on plan and date. Ask for the length in writing and what it excludes."),
         ("Remove the Wi-Fi fee", "A Spectrum router is billed monthly, reported at $5 to $10. A router you own removes the fee. The modem is included either way."),
         ("Apply Auto Pay credits", "Reviewers report a monthly credit for Auto Pay. Ask what your account qualifies for."),
         ("Price a mobile bundle", "Reports describe Spectrum internet starting at $30 a month for 500 Mbps when bundled with mobile or video. Ask whether that offer is available to existing customers and what it costs after the promotion."),
         ("Mention fiber or 5G home internet", "Customers who say they are considering switching to a fiber provider or 5G home internet have reported receiving temporary discounts.")],
   alt="If Spectrum will not move on price, compare the cheapest plans at your address from other providers, but check the price after the promotion ends and what is excluded from any price lock.",
   src=[("Cord Cutters News: Spectrum $10 increase (legacy plans)", "https://cordcuttersnews.com/another-big-price-hike-is-coming-to-spectrum-customers/"),
        ("Yahoo Finance: Spectrum revamps internet service (price lock, $30 bundle)", "https://finance.yahoo.com/news/spectrum-plans-3-major-changes-190300141.html"),
        ("BroadbandNow: Spectrum Internet deals (Wi-Fi fee, own router)", "https://broadbandnow.com/Spectrum-Internet-deals"),
        ("HighSpeedInternet.com: what you actually pay for Spectrum", "https://highspeedinternet.com/resources/spectrum-real-costs")]),
 "att": dict(slug="lower-att-internet-bill", name="AT&T Internet", went="/bills/att-bill-went-up", bill="/bills/att",
   short="To lower an AT&T internet bill, enroll in Auto Pay and paperless billing, check whether a newer fiber tier costs less than your current plan, ask the loyalty team about the new-customer price in your area, and compare wireless bundle pricing.",
   asks=[("Apply the Auto Pay discount", "AT&T has offered up to $10 a month off for bank Auto Pay, $5 for a debit card, and $5 with the AT&T Points Plus card from Citi. AT&T says it applies within two bill periods."),
         ("Move me to the cheapest current fiber tier that covers my use", "AT&T simplified its fiber plans on June 7, 2026. Reports put the lowest tier at $35 a month, so an older, faster-than-needed plan may cost more."),
         ("Price the wireless bundle", "Reports say the 1 Gig fiber plan is $80 alone and $60 with a qualifying wireless plan. Only worth it if you would keep the wireless plan anyway."),
         ("Ask the loyalty department", "Customers have reported that calling the loyalty team after a $5 increase sometimes produced a credit or lower rate."),
         ("Check data allowance", "Some AT&T Internet plans carry a 1,024 GB allowance with $10 per 50 GB overage; faster plans are unlimited.")],
   alt="If AT&T will not budge, check which other providers report service at your address. Cable providers often have lower first-year prices, so compare the price after the promotion too.",
   src=[("AT&T: details about your internet price change", "https://www.att.com/support/article/u-verse-high-speed-internet/KM1260426/"),
        ("Android Headlines: AT&T price increase and Auto Pay discounts", "https://www.androidheadlines.com/2025/10/att-home-internet-home-internet-price-rise-again.html"),
        ("HighSpeedInternet.com: AT&T changes fiber prices", "https://highspeedinternet.com/resources/att-changes-fiber-prices"),
        ("PhoneArena: AT&T hikes home internet price, loyalty call", "https://www.phonearena.com/news/at-t-hikes-home-internet-price-again_id174968")]),
 "cox": dict(slug="lower-cox-bill", name="Cox", went="/bills/cox-bill-went-up", bill="/bills/cox",
   short="To lower a Cox bill, compare your rate with the new-customer price for your address, ask about equipment and data charges, and ask what changes as Cox moves into Spectrum. Existing promotions are reported to be honored.",
   asks=[("Quote the new-customer price", "Cox, like most cable providers, offers lower prices to new customers. Look up the price for your address and quote it to the retention team."),
         ("Remove equipment rental", "Cox has billed its Panoramic Wifi gateway at about $13 to $15 a month after a promotion. A compatible modem and router you own can replace it."),
         ("Check the data allowance", "Cox plans have historically had a 1,280 GB allowance with $10 per extra 50 GB. Ask whether yours does, and what unlimited costs."),
         ("Ask about the Spectrum transition", "Reports in September 2026 say Cox customers keep current pricing and equipment for now, are not forced onto Spectrum plans, and can call Spectrum to switch. Ask for the price both ways before deciding."),
         ("Keep your promotion terms", "Reports say existing promotions and commitments will be honored. Ask for your end date in writing.")],
   alt="If Cox will not move on price, compare fiber and 5G home internet where available. Check each provider's price after the promotion ends.",
   src=[("CableTV.com: Cox-Spectrum merger and prices", "https://www.cabletv.com/news/cox-spectrum-merger-will-price-increase"),
        ("CableTV.com: internet provider data caps", "https://www.cabletv.com/internet/brand-data-caps"),
        ("CompareInternet: internet price increase 2026 tracker", "https://www.compareinternet.com/blog/internet-price-increase-2026/")]),
}

def build_save(save):
    for k, d in SAVE.items():
        n = d["name"]; path = "/save/" + d["slug"]
        body = (author.box(CHECKED) + short(d["short"])
                + f"<h2>What to ask {esc(n)} for</h2>"
                + tbl(["Ask for", "Why it can work"], [(f"<b>{esc(x)}</b>", esc(y)) for x, y in d["asks"]])
                + "<h2>A 30-minute plan</h2>" + steps([
                    "Pull your last two bills and note the total, the plan name and every fee line.",
                    f"Look up what new customers pay for similar speed at your address, and write down the plan name and price.",
                    f"Call {esc(n)} and ask for the retention or loyalty team. Use the script below.",
                    "Write down the rep's name, the new price, the date it starts and how long it lasts.",
                    "Check the next bill to confirm the change appeared."])
                + "<h2>What to say</h2>" + BB.SCRIPT
                + "<h2>If they say no</h2>" + f"<p>{esc(d['alt'])}</p>"
                + f'<p><a href="{d["went"]}">Why did my {esc(n)} bill go up?</a> · <a href="{d["bill"]}">{esc(n)} fee guide</a> · <a href="/compare">Compare providers</a> · <a href="/guides/internet-promo-ended">When your promo ends</a></p>'
                + BB.call_cta(n) + src(d["src"]))
        title = f"How to Lower Your {n} Bill: What to Ask For and What to Say"
        save(path, page(path, title, f"How to lower your {n} bill: the discounts to ask for, a call script, and what to do if the answer is no. Sources listed, checked {CHECKED}.",
             f"How to lower your {n} bill", f"What to ask for, what to say, and what to do if {esc(n)} will not move on price.", body,
             faqs([(f"Can I really lower my {n} bill by calling?", f"Often. Ask for the retention or loyalty team and quote the new-customer price for your address. Offers vary, and you should confirm the price, the start date and the length in writing."),
                   (f"What is the best time to call {n}?", "Before your promotion or price guarantee ends. Set a reminder 30 to 60 days ahead."),
                   ("Is it worth switching instead?", "If another provider reports service at your address for less over the full term, including the price after any promotion, switching can save more than negotiating.")]),
             [("Home", SITE + "/"), ("Lower your bill", SITE + "/bills"), (f"Lower your {n} bill", SITE + path)], ["Lower my bill", "Sources listed"]))

# ---------------------------------------------------------------- 3. guides
def build_guides(save):
    # --- why did my internet bill go up
    reasons = [("Your promotion ended", "Most internet plans start at a discounted price for 12 or 24 months. When it ends the plan moves to the standard rate. Xfinity reviewers report a rise of about $20 to $55 a month."),
               ("Your provider raised prices", "Providers raise rates on existing customers, often on older plans. AT&T raised Fiber and Internet prices $5 on December 1, 2025, and Spectrum raised legacy internet plans $10 in mid-2026."),
               ("A price guarantee does not cover everything", "Price locks cover the base plan rate. Xfinity says taxes, fees and equipment charges may change during and after a promotion or minimum-term agreement."),
               ("Equipment or Wi-Fi fees started", "A modem, gateway, router or Wi-Fi pod is billed monthly by some providers. Spectrum bills its Wi-Fi router separately, reported at $5 to $10."),
               ("TV fees changed", "Broadcast TV and regional sports fees sit outside the package price on many TV plans and can change."),
               ("You lost a discount", "Auto Pay, paperless and bundle discounts disappear when you stop using the qualifying service. Xfinity offers $10 a month for paperless billing plus bank Auto Pay."),
               ("You went over a data cap", "Xfinity legacy plans charge $10 per 50 GB over 1.2 TB, up to $100 a month. Most large providers now offer unlimited data."),
               ("One-time charges", "Late fees, installation, activation, reconnection and unreturned equipment appear as single lines. Check whether the increase appears in one month only."),
               ("Taxes and recovery fees moved", "Provider recovery fees and local taxes change independently of the plan price.")]
    body = (author.box(CHECKED) + short("Internet bills usually go up for one of nine reasons: a promotion ended, the provider raised the price, a fee or equipment charge changed, a discount was lost, a data or one-time charge appeared, or taxes and recovery fees moved. Comparing your last two bills line by line shows which.")
            + "<h2>The 9 common reasons</h2>"
            + "".join(f"<h3>{i}. {esc(t)}</h3><p>{esc(x)}</p>" for i, (t, x) in enumerate(reasons, 1))
            + "<h2>Find your reason in 5 minutes</h2>" + steps(["Open your last two bills side by side.", "Compare the plan price first. If it is the same, the change is in fees or add-ons.",
                "Compare each fee line. Note any new line and the month it appeared.", "Check the bill message or notice for a rate change.", "Check the date your promotion or price guarantee ends."])
            + "<h2>Provider-specific guides</h2><div class=\"grid\">"
            + "".join(f'<a class="card" href="/bills/{d["slug"]}"><b>{esc(d["name"])} bill went up</b><span>What changed and how to check</span></a>' for d in WENT.values()) + "</div>"
            + f'<p><a href="/fees">All hidden fees explained</a> · <a href="/guides/internet-price-increases-2026">2026 price increase tracker</a> · <a href="/guides/internet-promo-ended">When your promo ends</a></p>'
            + BB.call_cta("internet") + src([("Xfinity: price changes", "https://www.xfinity.com/pricechanges/"),
                                           ("AT&T: details about your internet price change", "https://www.att.com/support/article/u-verse-high-speed-internet/KM1260426/"),
                                           ("Cord Cutters News: Spectrum $10 increase", "https://cordcuttersnews.com/another-big-price-hike-is-coming-to-spectrum-customers/"),
                                           ("HighSpeedInternet.com: what you actually pay for Xfinity", "https://highspeedinternet.com/resources/xfinity-real-costs"),
                                           ("Xfinity: data usage and overage", "https://www.xfinity.com/support/internet/data-usage-exceed-usage")]))
    p = "/guides/why-internet-bill-went-up"
    save(p, page(p, "Why Did My Internet Bill Go Up? 9 Common Reasons", f"Nine reasons your internet bill went up, how to tell which one applies to you, and what to do. Sources listed, checked {CHECKED}.",
         "Why did my internet bill go up?", "Nine common reasons, and a 5-minute way to find yours.", body,
         faqs([("Why did my internet bill go up for no reason?", "There is almost always a reason on the bill: an ended promotion, a rate increase, a new fee or a lost discount. Comparing the last two bills line by line shows it."),
               ("Can my provider raise my price during a contract?", "A promotional rate or minimum-term agreement usually protects the service price, but taxes, fees and equipment charges may still change. Read the terms of your agreement."),
               ("How much notice do providers give?", "Providers typically note changes on the bill. Check the bill message or important information section.")]),
         [("Home", SITE + "/"), ("Guides", SITE + "/guides"), ("Why did my internet bill go up?", SITE + p)], ["Pillar guide", "Sources listed"]))

    # --- 2026 price increase tracker
    trows = [("Xfinity", "Says some prices will increase starting December 2026; no amounts or services published. Newer TV packages fold TV fees into one price.", "Dec 2026 (announced)", "Provider page"),
             ("Spectrum", "$10 a month on legacy Flagship, Ultra and Gig internet plans; $4 on legacy TV Essentials ($31 to $35). Current plans not affected.", "June to July 2026", "Provider confirmed, per Cord Cutters News"),
             ("AT&T", "$5 a month on AT&T Fiber and AT&T Internet.", "Dec 1, 2025", "Provider page"),
             ("AT&T", "New fiber tiers (from $35); 1 Gig $80 alone or $60 with wireless; 5 Gig $140 to $125.", "June 7, 2026", "Reported by Broadband Breakfast and HighSpeedInternet.com"),
             ("AT&T", "Another $5 on fiber and copper plans started June 2024 to July 2025; Access from AT&T copper plan $15 to $20.", "Aug 16, 2026", "Reported from internal documents; not confirmed by AT&T"),
             ("Cox", "$5 a month on 500 Mbps and 1 Gig plans (sources disagree on exact tiers). Moving into Spectrum; existing promotions honored.", "Early 2026", "Reported"),
             ("Verizon Wireless", "Regulatory Charge $0.21 to $0.26 per voice line. We found no confirmed Fios internet increase in 2026.", "Nov 1, 2026", "Provider page"),
             ("Starlink", "Plan prices rose in June 2026; kit rental fee added and reported removed; area-based pricing.", "June to July 2026", "Reported"),
             ("CenturyLink", "Voice feature charges raised by up to $2 in some states.", "2026", "State filing")]
    body = (author.box(CHECKED) + short("In 2026 the clearest confirmed increases were Spectrum's $10 on legacy internet plans and AT&T's $5 on Fiber and Internet, and Xfinity says some prices will rise starting December 2026. Many other increases are reported rather than confirmed, and we label each one.")
            + "<h2>Provider-by-provider tracker</h2>"
            + tbl(["Provider", "What changed", "When", "How we know"], [(f"<b>{esc(w)}</b>", esc(x), esc(y), esc(z)) for w, x, y, z in trows])
            + warn("How to read this table", "Provider page means the provider states it. Reported means a news or review site reports it. Amounts vary by plan and area, and your bill is the final word.")
            + "<h2>What to do when your provider raises prices</h2>" + steps(["Find the notice on your bill and write down the amount and the date it starts.",
                "Check whether a newer plan from the same provider costs less than your current one.", "Call retention before the increase takes effect and ask for a credit or a current-plan rate.",
                "Compare other providers at your ZIP code, including the price after any promotion."])
            + '<p>Individual provider pages: ' + " · ".join(a("/bills/" + d["slug"], d["name"]) for d in WENT.values()) + "</p>"
            + f"<p class=\"note\">We re-check this page monthly. Last checked {CHECKED}.</p>"
            + BB.call_cta("internet") + src([("Xfinity: price changes", "https://www.xfinity.com/pricechanges/"), ("Cord Cutters News: Spectrum $10 increase", "https://cordcuttersnews.com/another-big-price-hike-is-coming-to-spectrum-customers/"),
                                           ("AT&T: details about your internet price change", "https://www.att.com/support/article/u-verse-high-speed-internet/KM1260426/"), ("HighSpeedInternet.com: AT&T changes fiber prices", "https://highspeedinternet.com/resources/att-changes-fiber-prices"),
                                           ("Android Authority: AT&T price hike, August 2026", "https://www.androidauthority.com/att-price-hike-august-2026-3689162/"), ("CableTV.com: Cox-Spectrum merger", "https://www.cabletv.com/news/cox-spectrum-merger-will-price-increase"),
                                           ("Verizon: about taxes, fees and mobile surcharges", "https://www.verizon.com/support/surcharges"), ("The Next Web: Starlink price changes", "https://thenextweb.com/news/starlink-price-increase-standby-mode-roam-residential"),
                                           ("Utah PSC: CenturyLink voice feature notice, 2026", "https://pscdocs.utah.gov/telecom/26docs/26049P02/343967Att1CstmrNtc2-19-2026.pdf")]))
    p = "/guides/internet-price-increases-2026"
    save(p, page(p, "Internet Price Increases 2026: Who Raised Rates and When", f"Which internet providers raised prices in 2026, by how much and when, with confirmed and reported changes labeled. Checked {CHECKED}.",
         "Internet price increases in 2026", "A provider-by-provider tracker, with confirmed and reported changes labeled.", body,
         faqs([("Which internet provider raised prices the most in 2026?", "It depends on the plan. Spectrum's $10 on legacy plans is the largest confirmed monthly increase we found among the big providers. Xfinity has said more increases start in December 2026."),
               ("Is Xfinity raising prices in December 2026?", "Xfinity says some prices will increase starting December 2026 and has not published amounts."),
               ("How often is this tracker updated?", "Monthly. The last check was " + CHECKED + ".")]),
         [("Home", SITE + "/"), ("Guides", SITE + "/guides"), ("Internet price increases 2026", SITE + p)], ["Pillar, refreshed monthly", "Sources listed"]))

    # --- average internet bill
    body = (author.box(CHECKED) + short("Surveys put the average US internet bill between about $69 and $81 a month in 2025 and 2026, depending on how it is measured. If you pay much more than that for a typical plan, check for fees, expired promotions or paying for more speed than you use.")
            + "<h2>What different studies found</h2>"
            + tbl(["Source", "Figure", "What it measures"], [
                ("BroadbandNow (Apr 2026)", "$81.16/mo", "Average across active internet-only plans from 2,100+ providers; $65.43 in New Jersey to $109.88 in Alaska"),
                ("Bureau of Labor Statistics (cited Feb 2026)", "About $75/mo", "Typical family internet spend, about 1% of average income"),
                ("CNET (cited by Mint Mobile)", "$78/mo", "Analysis of 150 plans from the biggest providers"),
                ("USTelecom index (via NerdWallet, 2025)", "$69.33 and $97.34", "Most popular plans, and the highest-speed (940 Mbps to 1 Gbps) plans"),
                ("doxo (2025 report)", "$121/mo median", "Cable and internet combined among households that pay for either")])
            + warn("Why the numbers differ", "Some figures are advertised plan prices, some include TV, and some are what households actually pay. None of them includes your exact fees, so use them as a range, not a target.")
            + "<h2>Is your internet bill too high?</h2>" + steps(["Find your plan price and speed, and the number of people and devices at home.",
                "Add every fee line: equipment, Wi-Fi, TV fees, add-ons, taxes.", "Compare the total with the range above and with new-customer prices at your ZIP code.",
                "If you pay for 1 Gig but mostly stream and browse, a mid-tier plan is often enough. Run a speed test to see what you get.", "If your total is well above, call and ask for a better rate or compare providers."])
            + '<p><a href="/speed-test">Run a speed test</a> · <a href="/guides/how-much-internet-speed-do-you-need">How much speed you need</a> · <a href="/fees">Hidden fees explained</a> · <a href="/guides/why-internet-bill-went-up">Why bills go up</a></p>'
            + BB.call_cta("internet") + src([("BroadbandNow: The cost of staying connected in 2026", "https://broadbandnow.com/research/home-internet-costs-by-state"),
                                           ("Benton Institute summary of the BroadbandNow report", "https://www.benton.org/headlines/cost-staying-connected-2026"),
                                           ("Washington Times: costs rise, internet price (BLS figure)", "https://www.washingtontimes.com/news/2026/feb/12/costs-rise-internet-price/"),
                                           ("Mint Mobile: how much is internet per month (CNET figure)", "https://www.mintmobile.com/blog/how-much-is-internet-per-month/"),
                                           ("NerdWallet: how much is internet per month (USTelecom index)", "https://www.nerdwallet.com/blog/utilities/understanding-difference-dsl-cable-fiberoptic-internet-service/"),
                                           ("Fox 5 Atlanta: doxoINSIGHTS cable and internet report", "https://www.fox5atlanta.com/news/cable-internet-costs-2025-report")]))
    p = "/guides/average-internet-bill"
    save(p, page(p, "Is My Internet Bill Too High? Average Internet Bill 2026", f"The average US internet bill in 2026 from several studies, why they differ, and how to tell whether yours is too high. Checked {CHECKED}.",
         "Is my internet bill too high?", "The average internet bill in 2026, why studies disagree, and a quick check for yours.", body,
         faqs([("What is the average internet bill in 2026?", "BroadbandNow put it at $81.16 a month. Other sources give about $69 to $78 depending on how they measure."),
               ("What is a normal internet bill with fees?", "Expect the plan price plus equipment, taxes and recovery fees. The total can run noticeably above the advertised price."),
               ("Which state has the cheapest internet?", "BroadbandNow found the lowest average in New Jersey at $65.43 a month and the highest in Alaska at $109.88.")]),
         [("Home", SITE + "/"), ("Guides", SITE + "/guides"), ("Average internet bill", SITE + p)], ["Pillar guide", "Sources listed"]))

    # --- promo ended
    body = (author.box(CHECKED) + short("When an internet promotion ends, the price moves to the standard rate, often $20 or more higher. Before it ends, check the date, price what new customers pay, and ask for a new promotion or a current plan with a price guarantee. If your provider will not match, compare other providers at your address.")
            + "<h2>What happens when a promo ends</h2><p>Promotional pricing is a discount for a set period, commonly 12 months. Afterwards the plan moves to the standard rate. Reviewers report Xfinity bills can rise by roughly $20 to $55 a month at that point. A price guarantee, such as Xfinity's 5-year guarantee, locks the base internet rate, but Xfinity says taxes, fees and equipment charges may still change.</p>"
            + "<h2>What to do, in order</h2>" + steps(["Find your end date in the provider app or on your bill. Set a reminder 30 to 60 days before.",
                "Look up what new customers pay for your speed at your ZIP code, and screenshot the plan and price.",
                "Call and ask for the retention team. Say what you pay, what new customers pay, and the price you want.",
                "Ask for a new promotion, or a move to a current plan with a price guarantee. Get the price, start date and length in writing.",
                "Check Auto Pay, paperless and bundle credits. Together they are often $10 or more a month.",
                "If the answer is no, compare other providers. Count the price after their promotion too."])
            + BB.SCRIPT
            + '<h2>Provider-specific plans</h2><p>' + " · ".join(a("/save/" + d["slug"], f"Lower your {d['name']} bill") for d in SAVE.values()) + '</p>'
            + '<p><a href="/guides/internet-price-increases-2026">2026 price increases</a> · <a href="/fees">Hidden fees explained</a> · <a href="/compare">Compare providers</a></p>'
            + BB.call_cta("internet") + src([("Xfinity: price changes", "https://www.xfinity.com/pricechanges/"), ("HighSpeedInternet.com: what you actually pay for Xfinity", "https://highspeedinternet.com/resources/xfinity-real-costs"),
                                           ("HighSpeedInternet.com: how much will Xfinity cost after a year", "https://www.highspeedinternet.com/resources/xfinity-cost-after-one-year"),
                                           ("WhistleOut: Spectrum Internet 500 Mbps (introductory rates)", "https://www.whistleout.com/Internet/Providers/Charter-Spectrum/Fiber/Spectrum-Internet-500Mbps")]))
    p = "/guides/internet-promo-ended"
    save(p, page(p, "What to Do When Your Internet Promo Price Ends", f"What happens when an internet promotion ends, and six steps to keep your price down: check the date, ask for a new promo, compare providers. Checked {CHECKED}.",
         "What to do when your internet promo ends", "Why the price jumps, and what to do before and after.", body,
         faqs([("What happens when my internet promotion ends?", "The plan moves to the provider's standard rate. Reviewers report increases of about $20 to $55 a month for Xfinity after a 12-month promotion."),
               ("Can I get a new promotion as an existing customer?", "Often, if you ask the retention team and have a competitor's price in hand. Offers vary."),
               ("Does a price guarantee cover fees?", "No. Xfinity says taxes, fees and equipment charges may change during and after a promotional period or contract term.")]),
         [("Home", SITE + "/"), ("Guides", SITE + "/guides"), ("Internet promo ended", SITE + p)], ["Lower my bill", "Sources listed"]))

    # --- /guides hub (replaces the old hub; lists existing + new)
    old = [("how-to-lower-your-internet-bill", "How to lower your internet bill", "Practical ways to cut what you pay."),
           ("fiber-vs-cable-internet", "Fiber vs cable internet", "Speed, price and reliability compared."),
           ("how-much-internet-speed-do-you-need", "How much internet speed do you need?", "Match speed to your household."),
           ("internet-for-streaming-and-gaming", "Internet for streaming and gaming", "What each activity needs."),
           ("satellite-internet-guide", "Satellite internet guide", "When satellite makes sense.")]
    new = [("why-internet-bill-went-up", "Why did my internet bill go up?", "Nine common reasons."),
           ("internet-price-increases-2026", "Internet price increases in 2026", "Provider-by-provider tracker."),
           ("average-internet-bill", "Average internet bill 2026", "Is yours too high?"),
           ("internet-promo-ended", "When your internet promo ends", "Six steps to keep your price down.")]
    cards = lambda L: '<div class="grid">' + "".join(f'<a class="card" href="/guides/{s}"><b>{esc(t)}</b><span>{esc(d)}</span></a>' for s, t, d in L) + "</div>"
    body = (author.box(CHECKED) + short("Plain-language guides on why bills go up, what each fee means, how to lower what you pay, and how to pick the right internet.")
            + "<h2>Lower your bill</h2>" + cards(new + old[:1]) + "<h2>Pick the right internet</h2>" + cards(old[1:])
            + '<p><a href="/fees">Hidden fees explained</a> · <a href="/bills">Provider bill guides</a> · <a href="/speed-test">Speed test</a></p>')
    save("/guides", page("/guides", "Internet and Bill Guides | YourBillCheck", "Guides on why internet bills go up, hidden fees, price increases, lowering your bill, and choosing the right internet.",
         "Internet and bill guides", "Plain-language guides to help you pay less and pick the right internet.", body, None,
         [("Home", SITE + "/"), ("Guides", SITE + "/guides")], ["Guides"]))

# ---------------------------------------------------------------- 4. /fees pillar
def build_fees_hub(save):
    F = BE.FEES
    rows = [("Broadcast TV fee", "TV package", "Carrying local channels. Provider-set, not a tax.", "Only by changing TV service", "broadcast-tv-fee"),
            ("Regional sports fee", "TV package", "Regional sports channels in your package.", "By dropping the sports package", "regional-sports-fee"),
            ("Modem and router rental", "Internet", "Monthly rental of the gateway or router.", "Often, with your own device", "modem-router-rental-fee"),
            ("Spectrum Wi-Fi fee", "Spectrum", "Spectrum's Wi-Fi router, reported $5 to $10/mo.", "Yes, with your own router", "spectrum-wifi-fee"),
            ("Xfinity data overage", "Xfinity legacy plans", "$10 per 50 GB over 1.2 TB, maximum $100/mo.", "Yes, with unlimited data", "xfinity-data-overage"),
            ("Data overage (all providers)", "Capped plans", "Charges for going over a data allowance.", "Usually", "data-overage-fee"),
            ("Verizon administrative and telco recovery charge", "Verizon Wireless", "Per-line provider charge, not a tax.", "Only by removing lines", "verizon-administrative-charge"),
            ("Recovery and regulatory fees", "Wireless and others", "Provider-set recovery charges outside the plan price.", "Rarely", "recovery-and-regulatory-fees"),
            ("Installation and activation", "New service", "One-time setup charges.", "Often waived", "installation-and-activation-fee"),
            ("Unreturned equipment", "After cancelling", "Charged if rented gear is not returned on time.", "Yes, by returning it", "unreturned-equipment-fee")]
    extra = [("Late payment fee", "Reported at $8.95 for Spectrum and $13 for Xfinity (CableTV.com).", "Yes, with Auto Pay or a reminder"),
             ("Paper bill fee", "Some providers charge or withhold a discount for paper billing.", "Yes, go paperless")]
    body = (author.box(CHECKED) + short("Most surprise charges on an internet or TV bill are provider fees, not taxes: TV broadcast and sports fees, equipment and Wi-Fi rental, recovery fees, data overages, and one-time setup or non-return charges. Many can be avoided or negotiated, and a few cannot.")
            + "<h2>The complete list</h2>"
            + tbl(["Fee", "Applies to", "What it is", "Can you avoid it?"], [(f'<a href="/fees/{s}"><b>{esc(n)}</b></a>', esc(ap), esc(w), esc(av)) for n, ap, w, av, s in rows]
                  + [(f"<b>{esc(n)}</b>", "Varies", esc(w), esc(av)) for n, w, av in extra])
            + "<h2>Fees by provider</h2><p>Provider-specific breakdowns: " + " · ".join(a("/bills/" + k, n) for k, n in [("xfinity", "Xfinity"), ("spectrum", "Spectrum"), ("att", "AT&T"), ("verizon", "Verizon"), ("cox", "Cox"), ("optimum", "Optimum"), ("frontier", "Frontier"), ("centurylink", "CenturyLink")]) + ".</p>"
            + "<h2>How to check your own bill</h2>" + steps(["Put your last bill next to the plan price you were quoted.", "Circle every line that is not the plan price or a tax.",
                "Look each one up above. Note whether it is avoidable.", "Call and ask about each avoidable line, using our <a href=\"/bills\">call script</a>."])
            + '<p><a href="/guides/why-internet-bill-went-up">Why did my bill go up?</a> · <a href="/guides/internet-price-increases-2026">2026 price increases</a></p>'
            + BE.cta())
    save("/fees", page("/fees", "Hidden Fees on Internet & TV Bills: The Complete List", f"Every common hidden fee on internet and TV bills, what it is, which providers charge it and whether you can avoid it. Checked {CHECKED}.",
         "Hidden fees on internet and TV bills", "The complete list, what each fee is and which can be avoided.", body,
         faqs([("What are hidden fees on an internet bill?", "Charges outside the advertised plan price: equipment and Wi-Fi rental, TV broadcast and sports fees, recovery fees, data overages, and one-time setup or non-return charges."),
               ("Which internet bill fees can I avoid?", "Equipment rental, Wi-Fi fees, overages, installation and unreturned-equipment charges are usually avoidable. TV broadcast and sports fees go away only with a different TV setup."),
               ("Are these fees taxes?", "No. Verizon, for example, says its Administrative and Telco Recovery Charge is not a governmental tax or a government-imposed fee.")]),
         [("Home", SITE + "/"), ("Fees", SITE + "/fees")], ["Pillar guide", "Sources listed"]))

def build(save):
    BE.build_fees(save)
    build_fees_hub(save)
    build_went(save)
    build_save(save)
    build_guides(save)
