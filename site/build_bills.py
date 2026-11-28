"""Bill guides: /bills hub and /bills/<provider>.

Why is my bill high, what each fee is, what happens after the promo, and how to lower it.
Every provider fact carries a source link. Where sources disagree we say so instead of picking a number.
Facts checked November 24, 2026.
"""
import html
import ui
import author

esc = lambda s: html.escape(str(s), quote=True)
SITE = "https://yourbillcheck.com"
CHECKED = "November 24, 2026"
DATE = "2026-11-24"
PHONE_TXT = "(888) 491-5666"
PHONE_TEL = "+18884915666"

# Each provider: one-line answer, what happens after the promo, fee rows, provider-specific
# ways to lower the bill, and sources. Fee row = (charge, typical amount, can you avoid it?, note)
B = {
 "xfinity": dict(
  title='Xfinity Bill So High? Promo Cliffs, Gateway Rental and TV Fees Line by Line',
  desc='Where an Xfinity bill gets padded: the 12-month promo ending (reviewers report +$20 to $55), gateway rental, Broadcast TV and Regional Sports fees. A fee table and checks. Checked November 28, 2026.',
  lead='Xfinity bills are mostly a story of promotions ending and TV fees that sit outside promo pricing.',
  intro='Xfinity\'s price guarantees cover the base internet rate only, so the lines to inspect are the ones outside it: equipment (on plans that charge for it), Broadcast TV, Regional Sports and taxes. If the jump just happened, start with <a href="/bills/xfinity-bill-went-up">why your Xfinity bill went up</a>, then use the <a href="/save/xfinity-retention-department">Xfinity retention call script</a>.',
  short="Most Xfinity bills rise for three reasons: a promotional rate ending, equipment rental, and TV fees (Broadcast TV and Regional Sports) that are not covered by promotional pricing.",
  after=("Xfinity sells many plans with a 12-month promotional rate, and some newer plans with a 1-year or 5-year price guarantee. "
         "When a 12-month promo ends, reviewers report the bill can rise by roughly $20 to $55 a month. "
         "A price guarantee locks the base internet rate only: taxes, regulatory fees and equipment rental are not covered and can still go up."),
  fees=[("Promotional rate ending", "Often +$20 to $55/mo", "Partly", "Ask for a new promotion or a guaranteed-price plan before the promo ends."),
        ("Equipment (gateway) rental", "Separate or included, depends on plan", "Often", "Some plans include the gateway. Otherwise a compatible modem you own removes the rental line."),
        ("Broadcast TV Fee (TV customers)", "Varies by market", "Only by changing TV service", "Not government-mandated. Excluded from promo and contract pricing and can rise during a promotion, with notice."),
        ("Regional Sports Network Fee (TV)", "Varies by package", "Only by changing TV package", "Also excluded from promo pricing. Xfinity's newer 2026 TV packages fold these fees into one price."),
        ("Taxes and regulatory recovery fees", "Varies by area", "No", "Never covered by a price guarantee.")],
  tips=["Find your promo or guarantee end date in the Xfinity app or on your bill, and set a reminder 30 to 60 days before it.",
        "If you have legacy TV with separate Broadcast TV and Regional Sports fees, ask whether one of the 2026 all-inclusive TV packages costs less in total.",
        "Check whether your plan already includes the gateway before paying rental, or use a compatible modem you own.",
        "Compare the current new-customer price in your ZIP with what you pay, and quote it when you call."],
  src=[("Xfinity: most common taxes, fees and surcharges", "https://www.xfinity.com/support/articles/most-common-taxes-fees-surcharges-on-your-bill"),
       ("Xfinity: price changes and TV fees", "https://www.xfinity.com/pricechanges/"),
       ("HighSpeedInternet.com: what you actually pay for Xfinity (Jan 2026)", "https://highspeedinternet.com/resources/xfinity-real-costs")]),
 "spectrum": dict(
  title='Spectrum Bill Higher Than Expected? Advanced WiFi, Legacy Plans and the Promo End',
  desc='Why a Spectrum internet bill climbs: the promo ending (reported +$20 to $35), Advanced WiFi billed on some plans, and a reported $10 increase on legacy plans in 2026. Checked November 28, 2026.',
  lead='Three Spectrum-specific suspects: the end of the promotional rate, Advanced WiFi and an older legacy plan.',
  intro='Spectrum has no data caps on internet, so overage is not the cause. Check for an older plan name on your bill and an Advanced WiFi line first. For the sudden-jump version of this question see <a href="/bills/spectrum-bill-went-up">why your Spectrum bill went up</a> and the <a href="/save/spectrum-retention-department">Spectrum retention call script</a>.',
  short="Spectrum bills usually jump when the 12-month promotion ends, when Advanced WiFi is billed separately, and on TV accounts through the Broadcast TV surcharge. Spectrum internet has no data caps.",
  after=("Spectrum promotional prices typically last 12 months (some bundles 24). Reviewers report the smallest plan rises by about $20 a month afterwards and most other plans by about $35. "
         "Separately, Spectrum added a $10 monthly increase on many legacy internet plans in 2026, so older plans can rise even without a promo ending."),
  fees=[("Promotional rate ending", "About +$20 to $35/mo", "Partly", "Ask retention for a current offer before the promo ends."),
        ("Advanced WiFi (router)", "Billed monthly on some plans", "Yes on most plans", "The modem is included. Using your own Wi-Fi router can remove this line; some faster tiers include it."),
        ("Legacy plan increase (2026)", "+$10/mo reported on legacy plans", "By moving to a current plan", "Older plan names on your bill are a sign you may be paying legacy rates."),
        ("Broadcast TV surcharge (TV customers)", "Varies by market", "Only by changing TV service", "Excluded from promotional pricing."),
        ("Activation / installation", "One-time", "Sometimes", "Self-install is cheaper than a technician visit.")],
  tips=["Check your bill for an older plan name. If you are on a legacy plan, ask to move to a current plan at the same or higher speed.",
        "Replace the rented Wi-Fi router with your own if your plan charges for Advanced WiFi.",
        "Reviewers list unlimited data on Spectrum plans, so you should not need a bigger plan just to avoid overage charges.",
        "If you have Spectrum Mobile or could use it, ask what bundle discount applies to your internet line."],
  src=[("HighSpeedInternet.com: Spectrum cost after one year (Apr 2026)", "https://highspeedinternet.com/resources/spectrum-cost-after-one-year"),
       ("Cord Cutters News: Spectrum $10 internet price increase", "https://cordcuttersnews.com/?p=248449"),
       ("CableTV.com: hidden costs of Spectrum", "https://www.cabletv.com/spectrum/hidden-costs")]),
 "att": dict(
  title='AT&T Internet Bill Too High? The $5 Increases, Fiber Extras and What to Ask',
  desc="AT&T's listed $5 internet increases (Aug 16, Sep 28 and Dec 1, 2026, by plan and activation date), optional add-ons that inflate a bill, and how to ask for a cheaper plan. Checked November 28, 2026.",
  lead='Check whether your plan falls in one of the AT&T 2026 $5 increases, then look at add-ons and your plan tier.',
  intro='The AT&T price-change page lists $5 increases in 2026 that apply to groups of plans by the date they were activated, so a high AT&T bill often points to one of those or to an add-on you did not mean to keep. Read the line-by-line list below, then see <a href="/bills/att-bill-went-up">why your AT&amp;T bill went up</a> and the <a href="/save/att-retention-department">AT&amp;T retention call script</a>.',
  short="AT&T Fiber has no equipment fee, no data cap and no annual contract, so most AT&T increases come from company-wide price changes rather than a promo ending.",
  after=("AT&T raised the monthly price of AT&T Fiber and AT&T Internet plans by $5 from December 1, 2025, and a further $5 increase was reported for August 2026. "
         "These changes apply on top of the plan you already have, so an AT&T bill can rise even when nothing on your account changes."),
  fees=[("Company-wide price change", "+$5 (Dec 2025); +$5 more reported Aug 2026", "No", "Applies to existing plans. Ask whether a current plan or a mobile bundle lowers the total."),
        ("Equipment", "$0 for standard equipment", "n/a", "Watch for optional upgrades such as All-Fi Pro added at checkout."),
        ("Data overage", "None on fiber", "n/a", "AT&T Fiber includes unlimited data."),
        ("Taxes and cost recovery charges", "A few dollars, varies", "No", "AT&T lists a state cost recovery charge on its fee schedule.")],
  tips=["Remove optional add-ons (equipment upgrades, protection plans) you did not mean to keep.",
        "If anyone in the home has AT&T wireless, ask what the internet price is with the mobile bundle discount.",
        "Compare your plan's price with AT&T's current price for the same speed, and ask to switch if the new plan is cheaper.",
        "If a slower tier is enough for your household, moving down a tier is the simplest saving. Use our speed test to check what you actually use."],
  src=[("AT&T: internet price change details", "https://www.att.com/support/article/u-verse-high-speed-internet/KM1260426/"),
       ("Android Authority: AT&T home internet price hike, August 2026", "https://www.androidauthority.com/att-price-hike-august-2026-3689162/"),
       ("HighSpeedInternet.com: what you actually pay for AT&T", "https://www.highspeedinternet.com/resources/att-real-costs")]),
 "verizon": dict(
  title='Verizon Fios Bill Too High? What the Price Lock Does Not Cover',
  desc='Fios includes the router and offers 3- to 5-year price locks, but taxes, fees and a missing Auto Pay credit can still lift the bill. Fee table and checks. Checked November 28, 2026.',
  lead='A Fios price lock covers the base rate, so the extra dollars come from the lines it leaves out.',
  intro='With the router included, a Fios bill that looks high usually comes down to Auto Pay not being applied, TV add-ons or fees outside the lock. For a recent increase see <a href="/bills/verizon-fios-bill-went-up">why your Verizon Fios bill went up</a> and <a href="/guides/how-to-cancel-verizon-fios">how to cancel Fios</a>.',
  short="Verizon Fios includes the router and sells plans with 3- to 5-year price locks, but the lock covers the base rate only. Taxes, fees and add-ons can still rise.",
  after=("Current Fios plans come with a 3-, 4- or 5-year price lock depending on speed. The lock applies to the plan's base rate, not to taxes and fees, "
         "and Fios customers have previously seen a $5 'miscellaneous charges' increase. Paying without Auto Pay also costs more each month."),
  fees=[("Price-lock exclusions (taxes and fees)", "Varies", "No", "Read the fine print: the lock is on the base rate."),
        ("Auto Pay discount lost", "Higher monthly price without Auto Pay", "Yes", "Turn on Auto Pay if the discount applies to your plan."),
        ("Router", "Included", "n/a", "Fios includes the router at no extra cost on current plans."),
        ("Professional setup", "$99 one-time, often waived", "Usually", "Often waived online or with Mobile + Home."),
        ("Unreturned equipment", "Charged if not returned within 30 days of cancelling", "Yes", "Return the router after cancelling.")],
  tips=["Check that Auto Pay is on and that you are receiving the Auto Pay price.",
        "If you have Verizon mobile, ask about Mobile + Home pricing for your Fios line.",
        "Ask whether a current plan with a longer price lock costs less than your existing plan.",
        "Remove TV add-ons and extra set-top boxes you no longer use (Fios TV has its own broadcast and sports fees)."],
  src=[("Verizon: Fios plans and price lock", "https://www.verizon.com/home/internet/fios-fastest-internet"),
       ("Verizon: Fios equipment return terms", "https://www.verizon.com/info/fios-reviews-awards/"),
       ("PhoneArena: Verizon Fios $5 increase", "https://www.phonearena.com/news/Second-Verizon-price-hike-announced-in-less-than-a-month_id166996")]),
 "t-mobile": dict(
  short="T-Mobile 5G Home Internet has no equipment rental fee and plans carry a multi-year price guarantee, but the guarantee excludes taxes and fees, which T-Mobile has raised twice in 2026.",
  after=("T-Mobile's home internet price guarantee covers the base rate for the guarantee period; taxes and fees are excluded. "
         "In 2026 T-Mobile raised its Regulatory Programs and Telco Recovery Fee twice, most recently from October 12, 2026. That fee is charged per line, so it lands even on price-locked plans if your account pays it."),
  fees=[("Regulatory Programs & Telco Recovery Fee", "Per line; raised Oct 12, 2026", "No", "Not every plan pays it. Some plans were sold with taxes and fees included."),
        ("Equipment", "$0 for the 5G gateway", "n/a", "No rental fee for the standard gateway."),
        ("AutoPay / voice-line discount", "Lost if you change plans or drop the line", "Yes", "The lowest prices need AutoPay and sometimes a voice line."),
        ("Device connection charge", "One-time at signup", "No", "Shown on the first bill with prorated charges.")],
  tips=["Check your notice to see whether your plan pays the Telco Recovery Fee or includes taxes and fees.",
        "If you have a T-Mobile phone line, ask for the home internet price with a voice line.",
        "Before changing plans, ask whether the change ends your price guarantee.",
        "If coverage is weak at your address, a wired provider may give more speed for the same money. Compare providers in your ZIP code."],
  src=[("Droid Life: T-Mobile fees increasing for the second time in 2026", "https://www.droid-life.com/2026/09/28/t-mobile-fees-increasing-on-your-bill-for-2nd-time-this-year/"),
       ("Yahoo Tech: T-Mobile home internet rate lock covers base rates", "https://tech.yahoo.com/home/articles/t-mobile-tweaks-5g-home-194555478.html"),
       ("HighSpeedInternet.com: what you actually pay for T-Mobile Home Internet", "https://highspeedinternet.com/resources/t-mobile-real-costs")]),
 "frontier": dict(
  title='Frontier Bill Too High? Guarantee, Activation, Equipment',
  desc='Why a Frontier fiber bill can run high: a price guarantee ending, one-time activation charges and equipment not returned. Includes a call script.',
  lead='For Frontier, check three things first: whether your price guarantee is still active, any activation charge on the order, and equipment you have not returned.',
  intro='Frontier is now part of Verizon. If the jump was recent, see <a href="/bills/frontier-bill-went-up">why your Frontier bill went up</a>; to leave, see <a href="/guides/how-to-cancel-frontier">how to cancel Frontier</a>. You may not need to switch: if your plan is still inside its guarantee, the right move may be to leave it alone.',
  short="Frontier Fiber includes the router and sells plans with up to a 5-year price guarantee. The bill rises if a guarantee ends, if you change plans, or when equipment is not returned. Frontier is now part of Verizon.",
  after=("Frontier advertises fiber plans with up to a 5-year price guarantee and no annual contract. The guarantee can end if you change your plan or drop a service from a bundle, "
         "and Frontier reserves the right to add or change equipment fees. Some offers carry a one-time activation charge."),
  fees=[("Price guarantee ending or voided", "Varies by plan", "Partly", "Changing plans can end the guarantee, so ask first."),
        ("Activation", "One-time (e.g. $85 in some offers)", "Sometimes", "Check the order summary before you confirm."),
        ("Equipment", "Router included on fiber", "n/a", "Extra devices can be leased."),
        ("Restocking and unreturned equipment", "$50 restocking; up to $150 per unreturned device", "Yes", "Return equipment when you disconnect.")],
  tips=["Before upgrading or downgrading, ask whether the change ends your price guarantee.",
        "If you also have Verizon mobile, ask about the Frontier and Verizon mobile discount.",
        "On DSL? Ask whether Frontier Fiber now reaches your address; fiber often costs about the same for far more speed.",
        "When you cancel, return all equipment to avoid the restocking and non-return charges."],
  src=[("Frontier: offer terms (activation, restocking, unreturned equipment)", "https://go.frontier.com/id/mccall"),
       ("Frontier: multi-year price guarantees", "https://blog.frontier.com/2026/07/stop-bill-shock-eliminate-hidden-internet-fees-with-multi-year-price-guarantees/"),
       ("HighSpeedInternet.com: what you actually pay for Frontier", "https://www.highspeedinternet.com/resources/frontier-real-costs")]),
 "cox": dict(
  title='Cox Bill Too High? Price-Lock Endings, Panoramic Wifi Rental and Data Overage',
  desc='What inflates a Cox internet bill: a price lock or promotion ending, Panoramic Wifi gateway rental (reported), old data-cap overage and TV surcharges. Checked November 28, 2026.',
  lead='For Cox the main suspects are a price lock or promotion that ended and the Panoramic Wifi gateway being billed monthly.',
  intro='Charter closed its Cox purchase on August 20, 2026, so check which brand name appears on your bill. The charges below are the ones Cox and reviewers describe. For a recent jump see <a href="/bills/cox-bill-went-up">why your Cox bill went up</a> and <a href="/guides/how-to-cancel-cox">how to cancel Cox</a>.',
  short="Cox bills usually rise when a 12- or 24-month price lock ends and when the Panoramic Wifi gateway starts being billed. Cox has also had a 1.25 TB data cap with overage charges.",
  after=("Many Cox plans carry a price lock of up to 24 months, with the Panoramic Wifi gateway included for that period. After it ends, the plan moves to the standard rate and the gateway can be billed monthly (reported at about $13 to $15). "
         "Cox has had a 1.25 TB monthly data cap with $10 per extra 50 GB; a September 2026 report says caps were dropped, so check your bill for any overage line."),
  fees=[("Price lock ending", "Varies by plan", "Partly", "Ask for a loyalty offer; Cox publishes loyalty offers for existing customers."),
        ("Panoramic Wifi gateway rental", "About $13 to $15/mo after promo (reported)", "Yes", "Buy a compatible modem and router, or ask for a rental discount."),
        ("Data overage", "$10 per 50 GB over 1.25 TB (historical)", "Yes", "Check your plan: caps were reported dropped in Sept 2026."),
        ("TV broadcast and sports surcharges", "Varies", "Only by changing TV service", "Apply to TV customers.")],
  tips=["Sign in at Cox and look at the loyalty offers page for deals shown only to existing customers.",
        "If you rent Panoramic Wifi after the promo, compare 12 months of rental with the cost of your own modem.",
        "Look for a data overage line on recent bills; if it appears, ask whether an unlimited plan costs less in total.",
        "Quote the new-customer price in your ZIP when you ask for a better rate."],
  src=[("Cox: loyalty offers for existing customers", "https://cox.com/residential/special-offers/loyalty-my-speed.html"),
       ("HighSpeedInternet.com: Cox internet review (data cap and overage)", "https://highspeedinternet.com/providers/cox/internet"),
       ("Programming Insider: what changed when Cox became Spectrum (data caps)", "https://programminginsider.com/what-changed-when-cox-internet-became-spectrum/")]),
 "optimum": dict(
  title='Optimum Bill Too High? Old-Plan Step-Ups and $6 Fee',
  desc='Why an Optimum bill runs high: older plans that stepped up after 12 and 24 months, a $6.00 Network Enhancement Fee on its price list, and TV fees.',
  lead='For Optimum, the likely culprits are an older plan that stepped up after 12 and 24 months and a $6.00 Network Enhancement Fee line.',
  intro='In 2026 Optimum began offering a 5-year price lock on its internet plans (reported), so a bill that is still high may mean you signed up before it or are paying lines the lock does not cover. If it jumped recently, read <a href="/bills/optimum-bill-went-up">why your Optimum bill went up</a>; for a call script, see <a href="/save/lower-optimum-bill">how to lower your Optimum bill</a>. If you are already on a current locked plan, you may not need to change anything.',
  short="Optimum internet plans now carry a reported 5-year price lock and no internet equipment fee, but older plans rise after 12 and 24 months, and TV customers pay a broadcast fee and a regional sports fee.",
  after=("Optimum began offering a 5-year price lock on internet plans in 2026 (reported); after the lock, the monthly price can rise by up to $15 each year (reported). Older plans typically rose after 12 and again after 24 months. "
         "Optimum's own price list shows a $6.00 Network Enhancement Fee for customers with internet service (select offers excluded), while some review sites report it was dropped or lower, so check whether it appears on your bill."),
  fees=[("Older plan step-ups", "Rises after 12 and 24 months on older plans", "By moving to a current plan", "Ask about the current 5-year price lock."),
        ("Network Enhancement Fee", "$6.00/mo on Optimum's price list", "Check your bill", "Optimum's list says it applies to internet, select offers excluded; some reviewers disagree."),
        ("TV broadcast fee", "$9.99/mo (reported)", "Only by changing TV service", "TV customers only."),
        ("Regional sports network fee", "$10.47/mo (reported)", "Only by changing TV service", "TV customers only."),
        ("Equipment after promo", "Up to about $14/mo on some accounts", "Often", "New plans include equipment; ask if you are still renting.")],
  tips=["If you joined before 2026, ask to move to a current plan with the 5-year price lock.",
        "Look for a Network Enhancement Fee line on your bill and ask about it if it appears.",
        "If you rent an Optimum gateway after the promo ended, ask whether current plans include it at no charge.",
        "Drop TV boxes you no longer use; each box adds a monthly charge."],
  src=[("Optimum: standard pricing and packages", "https://optimum.com/pricing"),
       ("HighSpeedInternet.com: what you actually pay for Optimum", "https://highspeedinternet.com/resources/optimum-real-costs"),
       ("CableTV.com: Optimum price lock and fees", "https://www.cabletv.com/optimum/hidden-fees")]),
 "centurylink": dict(
  title='CenturyLink Bill Too High? Leased Modem and Other Fees',
  desc='Why a CenturyLink bill can run above your internet rate: leased modem and Wi-Fi equipment, phone features and other charges a price lock may not cover.',
  lead='For CenturyLink, the internet rate may be locked while leased equipment and phone features are not, so the total can still creep up (check your plan terms).',
  intro='The CenturyLink Price for Life notice says charges other than the internet rate, including leased equipment, are not protected. If your bill just jumped, see <a href="/bills/centurylink-bill-went-up">why your CenturyLink bill went up</a>; to leave, see <a href="/guides/how-to-cancel-centurylink">how to cancel CenturyLink</a>. If the equipment line is the only extra, your own compatible modem may fix it without switching.',
  short="CenturyLink internet is mostly priced month to month, but leased equipment and other charges are not price-protected and can rise. Its Quantum Fiber business was sold to AT&T in 2026.",
  after=("CenturyLink and Quantum Fiber have offered 'Price for Life' on the internet rate. CenturyLink says other rates, fees and charges on the account, including leased equipment, are not protected and may increase. "
         "Leased modem and Wi-Fi equipment has been billed at about $15 a month in Quantum Fiber offers."),
  fees=[("Leased modem / Wi-Fi", "About $15/mo when leased", "Yes", "You can use your own compatible modem and router."),
        ("Charges outside Price for Life", "Varies", "No", "Equipment and phone features are not protected."),
        ("Unreturned equipment", "Up to $200 per leased item", "Yes", "Return the old modem within 30 days when you switch or cancel."),
        ("Phone (voice) features", "Raised by up to $2 in some states, 2026", "Yes", "Remove phone features you do not use.")],
  tips=["Check whether you are leasing a modem; your own compatible modem removes that line.",
        "On DSL? Ask whether fiber is now available at your address. It is often similar money for far more speed.",
        "Remove home phone features you no longer use.",
        "If you switch, return leased equipment within 30 days."],
  src=[("CenturyLink: Fiber moved to Quantum Fiber FAQ (charges not protected)", "https://www.centurylink.com/home/help/notices/prepaid-fiber-to-quantum-fiber.html"),
       ("CenturyLink: switching to Quantum Fiber (unreturned equipment)", "https://www.centurylink.com/home/help/notices/move-to-quantum-fiber.html"),
       ("Utah PSC: CenturyLink voice feature increase notice, 2026", "https://pscdocs.utah.gov/telecom/26docs/26049P02/343967Att1CstmrNtc2-19-2026.pdf")]),
 "starlink": dict(
  title='Starlink Bill Too High? Plan Prices, Kit Fee, Area Pricing',
  desc='Why a Starlink bill runs high: 2026 plan price changes, a $10 kit fee reported removed in July, and area-based pricing, plus ways to cut it.',
  lead='For Starlink, the bill depends on your tier, any kit rental fee and the pricing for your address.',
  intro='Starlink prices were reported to change several times in 2026. For the sequence of changes, see <a href="/bills/starlink-bill-went-up">why your Starlink bill went up</a>. Compare any wired or 5G home internet that reaches your address, since it may cost less; if nothing else does, moving down a tier may be the only real saving.',
  short="Starlink prices changed several times in 2026: plan prices rose in June, a $10 monthly kit rental fee was added and then reported removed, and pricing now varies by area.",
  after=("After the June 2026 changes, US residential tiers were reported at about $55 (100 Mbps), $85 (200 Mbps) and $130 (Residential Max). "
         "A $10 monthly kit fee for rented dishes appeared in June and was reported removed for new orders in July. Starlink has also introduced area-based pricing, so the price depends on your address."),
  fees=[("Plan price changes", "+$5 to $10/mo reported in 2026", "No", "Starlink can change prices with notice."),
        ("Kit rental fee", "$10/mo (June 2026), reported removed July 2026", "Check your bill", "Compare with buying a dish outright from a retailer."),
        ("Area-based / demand pricing", "Varies by address", "No", "Enter your exact address on Starlink to see your price."),
        ("Shipping and one-time surcharges", "One-time", "No", "Shown at checkout.")],
  tips=["Check whether you are paying a kit rental fee and compare it with the price of buying a dish.",
        "If a lower tier covers your household's use, move down a tier.",
        "If wired or 5G home internet has reached your address, compare it; it may cost less.",
        "Use Standby Mode if you only need the connection part of the year (it was raised to $10/mo in 2026)."],
  src=[("Satelliteinternet.com: Starlink rentals back to $0 (Jul 2026)", "https://www.satelliteinternet.com/resources/starlink-rental/"),
       ("The Next Web: Starlink raises prices across consumer plans", "https://thenextweb.com/news/starlink-price-increase-standby-mode-roam-residential"),
       ("Notebookcheck: Starlink dynamic pricing by region", "https://notebookcheck.net/Starlink-intros-dynamic-prices-of-up-to-156-a-month.1440188.0.html")]),
}

EXTRA = {"frontier": ' · <a href="/bills/frontier-bill-went-up">Why your Frontier bill went up</a> · <a href="/guides/how-to-cancel-frontier">Cancel Frontier</a>',
         "starlink": ' · <a href="/bills/starlink-bill-went-up">Why your Starlink bill went up</a>',
         "centurylink": ' · <a href="/bills/centurylink-bill-went-up">Why your CenturyLink bill went up</a> · <a href="/guides/how-to-cancel-centurylink">Cancel CenturyLink</a>',
         "optimum": ' · <a href="/save/lower-optimum-bill">Lower your Optimum bill</a> · <a href="/bills/optimum-bill-went-up">Why your Optimum bill went up</a>'}

ORDER = ["xfinity", "spectrum", "att", "verizon", "t-mobile", "frontier", "cox", "optimum", "centurylink", "starlink"]

SCRIPT = ("<div class=\"call tip\"><b>What to say when you call</b>"
          "\"Hi, my bill has gone up to $[your total]. I can see new customers in my area are offered [speed] for $[price]. "
          "I'd like to stay, but I need a lower rate. What can you offer? If there's nothing today, please transfer me to the cancellations or retention team.\"</div>"
          "<p>Ask for the retention or loyalty team. They usually have offers the first person you speak to does not. Be polite, be specific about the number you want, and write down the rep's name and the new price before you hang up.</p>")

CHECKLIST = ["Find the date your promotion or price guarantee ends.",
             "Compare your plan price with the price new customers get in your ZIP code today.",
             "List every line on your bill: equipment rental, Wi-Fi, TV fees, add-ons, protection plans.",
             "Check whether you pay for speed you don't use. Run a speed test and look at how many people stream at once.",
             "Turn on Auto Pay and paperless billing if they lower your price.",
             "Call retention with a specific price in mind, or switch if another provider serves your address for less."]

def cl_html():
    return '<ol class="steps">' + "".join(f"<li>{esc(x)}</li>" for x in CHECKLIST) + "</ol>"

def fees_table(rows):
    return ("<table><tr><th>Charge</th><th>Typical amount</th><th>Can you avoid it?</th><th>What to know</th></tr>"
            + "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{esc(c)}</td><td>{esc(d)}</td></tr>" for a, b, c, d in rows) + "</table>")

def src_html(src):
    return ("<h2>Sources</h2><ul>" + "".join(f'<li><a href="{esc(u)}" rel="nofollow noopener" target="_blank">{esc(t)}</a></li>' for t, u in src)
            + f"</ul><p class=\"note\">We checked these sources on {CHECKED}. Fees and prices vary by area and change often. Your bill and your provider's broadband label are the final word for your account.</p>")

def call_cta(n):
    return ('<div class="cta"><div><h3>Want someone to check for you?</h3>'
            f'<p>Our team can compare your {esc(n)} bill with what other providers offer at your address. The call is free. '
            'If you switch through us we may earn a commission, at no cost to you. <a href="/about" style="color:#fff">How we make money</a>.</p></div>'
            f'<a class="btn" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a></div>')

def build(P, page_unused, save):
    done = []
    for k in ORDER:
        d = B[k]; p = P.get(k, {}); n = p.get("name", k.title())
        price = p.get("price", "")
        body = (author.box(CHECKED) + f'<div class="call tip"><b>Short answer:</b> {esc(d["short"])}</div>'
                + (f"<p>{d['intro']}</p>" if d.get("intro") else "") + f"<h2>What happens to your {esc(n)} bill after the promotion</h2><p>{esc(d['after'])}</p>"
                + (f"<p>For comparison, {esc(n)}'s typical new-customer starting price we track is <b>{esc(price)}</b> (November 2026). If you pay a lot more for similar speed, you are probably on post-promotion pricing or paying add-ons.</p>" if price else "")
                + f"<h2>Charges that make a {esc(n)} bill higher</h2>" + fees_table(d["fees"])
                + f"<h2>How to lower your {esc(n)} bill</h2><ol class=\"steps\">" + "".join(f"<li>{esc(t)}</li>" for t in d["tips"]) + "</ol>"
                + "<h2>Before you call: 6-point bill check</h2>" + cl_html()
                + f"<h2>Asking {esc(n)} for a better rate</h2>" + SCRIPT
                + f'<h2>More {esc(n)} help</h2><p><a href="/providers/{k}">{esc(n)} customer service numbers</a> · <a href="/speed-test/{k}">{esc(n)} speed test</a> · <a href="/moving/{k}">Moving {esc(n)} service</a> · <a href="/bills">All bill guides</a>' + EXTRA.get(k, "") + '</p>'
                + call_cta(n) + src_html(d["src"]))
        faq = [(f"Why did my {n} bill go up?", d["short"]),
               (f"Can I get {n} to lower my bill?", f"Often, yes. Call {n}, ask for the retention or loyalty team, and quote the price new customers get in your area. If they will not match it, compare other providers at your address."),
               (f"Does a {n} price guarantee cover everything?", "No. Price guarantees and price locks cover the base plan rate. Taxes, regulatory fees and equipment charges are usually excluded and can still rise."),
               ("Is it worth buying my own modem?", "If your plan charges a monthly equipment rental, a compatible modem you own usually pays for itself within a year. Check your provider's approved device list first.")]
        title = d.get("title") or f"Why Is My {n} Bill So High? Fees, Price Increases and How to Lower It"
        desc = d.get("desc") or f"Why {n} bills go up: promo endings, equipment and TV fees, and 2026 price changes, with a fee table, a call script and sources. Checked {CHECKED}."
        h1 = f"Why is my {n} bill so high?"
        lead = esc(d["lead"]) if d.get("lead") else f"What pushes a {esc(n)} bill up, which charges you can remove, and what to say to get a lower rate."
        crumbs = [("Home", SITE + "/"), ("Lower your bill", SITE + "/bills"), (n, SITE + f"/bills/{k}")]
        save(f"/bills/{k}", ui.shell(f"/bills/{k}", title, desc, h1, lead, body, faq, crumbs, ["Bill guide", "Sources listed"], date=DATE, checked=CHECKED, author=author.PERSON))
        done.append(k)

    # ---- hub ----
    cards = "".join(f'<a class="card" href="/bills/{k}"><b>{esc(P.get(k, {}).get("name", k))} bill</b><span>{esc(B[k]["short"][:118].rsplit(" ", 1)[0])}…</span></a>' for k in ORDER)
    glossary = [("Promotional rate", "A discounted price for the first 12 or 24 months. When it ends, the plan moves to the provider's standard rate, often $20 to $50 more."),
                ("Price guarantee / price lock", "Locks the base plan price for a set time. Taxes, regulatory fees and equipment are usually excluded."),
                ("Equipment rental", "A monthly charge for the modem, gateway or Wi-Fi router. Often avoidable with a compatible device you own."),
                ("Broadcast TV fee", "A TV-only charge for carrying local channels. Not a government fee, and usually excluded from promo pricing."),
                ("Regional sports fee", "A TV-only charge for regional sports networks, depending on your package."),
                ("Recovery and regulatory fees", "Provider-set charges with official-sounding names. They can rise even on price-locked plans."),
                ("Data overage", "Extra charges for going over a data cap. Many providers have no caps; check yours.")]
    body = (author.box(CHECKED) + '<div class="call tip"><b>Short answer:</b> Most internet bills rise for the same few reasons: a promotional price ending, equipment rental, TV fees, provider-set "recovery" fees, and paying for speed you don\'t use. Most can be reduced with one phone call or by switching.</div>'
            "<h2>Pick your provider</h2><div class=\"grid\">" + cards + "</div>"
            "<h2>The 6-point bill check</h2>" + cl_html()
            + "<h2>What the charges on your bill mean</h2><table><tr><th>Charge</th><th>What it is</th></tr>"
            + "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td></tr>" for a, b in glossary) + "</table>"
            + "<h2>How to ask for a lower rate</h2>" + SCRIPT
            + "<h2>When switching beats negotiating</h2><p>If your provider will not get close to the price new customers pay, and another provider serves your address, switching is usually the bigger saving. "
              "Enter your ZIP code to see who reports service at your address, then compare starting prices. Keep the old service until the new one works.</p>"
            + '<p><a href="/compare">Compare providers</a> · <a href="/speed-test">Check the speed you actually get</a> · <a href="/guides/how-to-lower-your-internet-bill">How to lower your internet bill</a></p>'
            + call_cta("internet"))
    faq = [("Why does my internet bill keep going up?", "Usually a promotional price ending, equipment rental, or provider fees that are not covered by a price lock. Your bill lists each line, so compare it month to month."),
           ("Can I negotiate my internet bill?", "Yes. Ask for the retention or loyalty team and quote the price new customers get in your area. Many providers have offers for existing customers that they do not advertise."),
           ("Does a price lock mean my bill can't go up?", "No. Price locks cover the base plan rate. Taxes, regulatory and recovery fees, and equipment charges can still rise."),
           ("Is YourBillCheck free?", "Yes. The bill guides and checks are free. We may earn a commission if you switch providers through us, at no cost to you.")]
    save("/bills", ui.shell("/bills", "Why Is My Internet Bill So High? Fees Explained and How to Lower It",
         "Why internet bills go up and how to lower yours: promo endings, equipment and TV fees, price locks, a call script and provider-by-provider guides.",
         "Why is my internet bill so high?", "What pushes internet bills up, which charges you can remove, and provider-by-provider guides with sources.",
         body, faq, [("Home", SITE + "/"), ("Lower your bill", SITE + "/bills")], ["Bill guides", "10 providers"], date=DATE, checked=CHECKED, author=author.PERSON))
    author.build(save, ui.shell)
    return done
