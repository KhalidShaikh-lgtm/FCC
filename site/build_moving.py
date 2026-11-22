import html
esc = html.escape
SITE = "https://yourbillcheck.com"
ORDER = ["att", "xfinity", "spectrum", "verizon", "frontier", "cox", "optimum", "centurylink", "t-mobile"]

def crumbs(*items):
    return [("Home", SITE + "/"), ("Moving", SITE + "/moving")] + [(t, SITE + u) for t, u in items]

def zipcta():
    return ('<div class="cta"><h3>Moving? See who serves your new address</h3><p>Enter the ZIP code of your new home to compare providers, speeds and support numbers.</p>'
            '<form onsubmit="var z=this.z.value.trim();if(/^\\d{5}$/.test(z)){location.href=\'/internet/\'+z}else{alert(\'Enter a 5-digit ZIP code\')}return false">'
            '<input name="z" inputmode="numeric" maxlength="5" placeholder="New ZIP code" style="padding:12px 14px;border:0;border-radius:12px;font:600 16px inherit;width:170px"> '
            '<button class="btn alt" type="submit">See providers</button></form></div>')

TIMELINE = [
 ("4 to 6 weeks before", "Find out who serves the new address. Enter the new ZIP code on our site, then confirm the exact address on the provider's own site or by phone. Availability can differ from house to house."),
 ("2 to 4 weeks before", "Decide: transfer your current service if your provider serves the new address, or sign up with a different provider. Book the install or activation date, ideally on or just before move-in day."),
 ("1 to 2 weeks before", "Confirm the date and any equipment instructions: whether to bring your modem or gateway, return it, or use new gear. Ask about transfer, install or activation fees, and keep a note of the confirmation number."),
 ("Moving day", "Keep your old service on until the new connection works. Pack the modem, router and power cords in a clearly labelled box so they are the first thing you set up."),
 ("First day in the new home", "Plug in, wait for the lights to settle, and run a speed test. If something is wrong, use our troubleshooter to match your lights to what they mean."),
 ("After the move", "Cancel or finish the old service, return any equipment the provider asks for, and check that your final bill is prorated the way you were told."),
]

def tl_html():
    return '<ol class="steps">' + "".join(f"<li><b>{esc(a)}</b><br>{esc(b)}</li>" for a, b in TIMELINE) + "</ol>"

def build(P, PROV, page, save):
    done = []
    # ---- provider move pages ----
    for k in ORDER:
        p = P.get(k); d = PROV.get(k)
        if not p: continue
        n = p["name"]
        rows = "".join(f'<tr><td>{esc(a)}</td><td><b>{esc(b)}</b></td><td><a href="{esc(c)}" rel="nofollow noopener">Official page</a></td></tr>' for a, b, c in p["support"])
        extra = ""
        if k == "att":
            extra = '<div class="call tip"><b>AT&amp;T tip</b>AT&amp;T says that in many cases moving its internet is as simple as taking your Wi-Fi Gateway to the new address and plugging it in. If you move without telling AT&amp;T, the service usually stays at the old address, so always report the move.</div>'
        body = f"""<p>You can usually move {esc(n)} service if your new address is inside {esc(n)}'s service area. If it isn't, you will need a different provider at the new home. Either way, start 2 to 4 weeks before you move.</p>
{extra}
<h2>How to move or transfer {esc(n)} service</h2>
<ol class="steps">
<li><b>Check the new address.</b> Enter the new ZIP code on our site to see if {esc(n)} is listed, then confirm the exact address with {esc(n)}. Coverage can change from street to street.</li>
<li><b>Contact {esc(n)}.</b> Use the official numbers below. Say that you are moving, give the new address and your move date.</li>
<li><b>Ask what applies to you.</b> Ask about any transfer, installation or activation fee, whether you can self-install, and whether your current plan and price carry over.</li>
<li><b>Ask about equipment.</b> Ask whether to bring your modem or gateway, return it, or use new equipment at the new address.</li>
<li><b>Book the date.</b> Pick an activation or install date close to move-in day and write down the confirmation number.</li>
<li><b>Set up and test.</b> Plug in at the new home, wait for the lights to settle, then <a href="/speed-test/{k}">run a speed test</a>. If a light looks wrong, see <a href="/help/{k}">{esc(n)} troubleshooting</a>.</li>
</ol>
<h2>{esc(n)} contact numbers for moving</h2>
<table><tr><th>For</th><th>Phone</th><th>Link</th></tr>{rows}</table>
<p class="note">Numbers and links come from {esc(n)}'s own support pages, last checked November 22, 2026. Policies and fees change, so confirm details with {esc(n)} before you book. YourBillCheck is independent and is not affiliated with {esc(n)}.</p>
<h2>If {esc(n)} does not serve your new address</h2>
<p>Compare the providers that do. See <a href="/compare">provider comparisons</a>, then check the new ZIP code below. Keep your old service until the new one is working, so you are never offline on moving day.</p>
<h2>Moving checklist</h2>{tl_html()}{zipcta()}"""
        faq = [(f"Can I transfer my {n} service to a new address?", f"Usually yes, if the new address is within {n}'s service area. If it is not, you will need a different provider. Contact {n} with your new address and move date to confirm."),
               (f"How far ahead should I contact {n} about moving?", "Two to four weeks before your move gives enough time to check availability and book an install or activation date."),
               (f"Should I take my {n} equipment with me?", f"It depends on the provider and your plan. Ask {n} whether to bring, return or replace your modem or gateway when you call."),
               (f"Who do I call to move {n} service?", f"Use the official {n} numbers listed on this page. They are taken from {n}'s support pages.")]
        save(f"/moving/{k}", page(f"/moving/{k}", f"How to Move or Transfer {n} Service to a New Address", f"Moving? Step-by-step guide to transferring {n} internet to a new address, who to call, what to ask and a moving checklist.",
             f"How to Move {n} Service", f"Step-by-step: transfer {n} service to your new address, who to call and what to ask.", body, faq,
             crumbs((n, f"/moving/{k}")), chips=[n, "Moving", "Checked Nov 2026"]))
        done.append(k)

    # ---- transfer guide ----
    body = f"""<p>Moving is the best time to review what you pay for internet. You can transfer service if your provider covers the new address, or switch to a better deal. Start early, because install slots can fill up around busy moving weekends.</p>
<h2>Transfer or switch?</h2>
<div class="grid"><div class="card"><h3>Transfer</h3><p>Best when your provider serves the new address and you like the price and speed. Often fastest. Ask about fees and equipment.</p></div>
<div class="card"><h3>Switch</h3><p>Best when your provider doesn't serve the new address, or a faster or cheaper option does. Compare providers by ZIP code first.</p></div></div>
<h2>Moving timeline</h2>{tl_html()}
<h2>Questions to ask the provider</h2>
<ul><li>Is my new address serviceable, and at what speed?</li><li>Is there an install, transfer or activation fee?</li><li>Does my current price carry over?</li><li>Should I bring, return or replace my equipment?</li><li>Can I self-install, or do I need a technician?</li><li>Will my final bill be prorated?</li></ul>
<h2>Find your provider</h2><div class="grid">{"".join(f'<a class="card" href="/moving/{k}"><h3>{esc(P[k]["name"])}</h3><p>Move or transfer {esc(P[k]["name"])} service.</p></a>' for k in ORDER if k in P)}</div>{zipcta()}"""
    faq = [("How do I transfer my internet when I move?", "Contact your provider 2 to 4 weeks ahead with your new address and move date, confirm service is available, book the activation date and ask about equipment and fees."),
           ("Can I keep the same internet provider when I move?", "Only if that provider serves your new address. Check by ZIP code and then confirm with the provider."),
           ("When should I set up internet before moving?", "Contact providers at least 2 weeks ahead, and 4 weeks if you are moving at a busy time or to a new state."),
           ("Should I cancel my old internet before I move?", "Keep it until the new service works, then cancel or end it and ask whether your final bill is prorated.")]
    save("/moving/transfer-internet-to-new-address", page("/moving/transfer-internet-to-new-address", "How to Transfer Internet Service to a New Address (2026 Guide)",
         "How to transfer or switch internet service when you move: a timeline, questions to ask, and provider-by-provider move guides.", "How to Transfer Internet to a New Address",
         "A simple timeline for moving your internet, plus what to ask your provider.", body, faq, crumbs(("Transfer internet", "/moving/transfer-internet-to-new-address")), chips=["Moving", "Timeline", "Checked Nov 2026"]))

    # ---- variants ----
    V = {
     "apartment-renters": ("Internet for Apartment and Renters: What to Know Before You Move", "Internet for Apartments and Renters",
        "Renting? Check these before you pick a provider.",
        "<p>Apartments can limit your choices. The building may have wiring from only some providers, and some buildings have a deal with one provider. Always check the exact unit address.</p><h2>Check before you sign</h2><ul><li>Ask the landlord or property manager which providers serve the building.</li><li>Ask whether the building has a bulk or preferred provider deal and whether it is included in rent.</li><li>Ask whether you may install equipment or drill, and who owns the wiring.</li><li>Check the exact unit address with each provider, not just the ZIP code.</li></ul><h2>Tips for renters</h2><ul><li>Pick a plan with no long contract if you may move again.</li><li>Ask about self-install, which is often faster for apartments.</li><li>Ask what happens with equipment when you move out.</li></ul>",
        [("Can I choose my own internet provider in an apartment?", "Often yes, but it depends on what is wired into the building. Ask your property manager and check your exact unit address."), ("Do I need landlord permission to install internet?", "Often, if the install needs drilling or outside work. Self-install kits usually don't. Ask your property manager."), ("Should I avoid contracts as a renter?", "If you may move within a year, look for a no-contract plan or ask about early termination and moving options.")]),
     "moving-to-new-state": ("Moving to a New State Checklist: Internet, Utilities and Mail", "Moving to a New State: Internet and Utilities Checklist",
        "Long-distance move? Don't forget internet and utilities.",
        "<p>A move to a new state usually means a new internet provider, new utility accounts and new service areas. Book early, as installs near move-in day fill up.</p><h2>Set up in this order</h2><ol class=\"steps\"><li><b>Internet.</b> Check your new ZIP code for providers and book the install for move-in day.</li><li><b>Electricity and gas.</b> Call each utility 1 to 2 weeks before the move. Rules vary by state.</li><li><b>Mail.</b> File a change of address with the postal service.</li><li><b>Old accounts.</b> End or transfer old internet, TV and utility accounts after the new ones work.</li></ol><p>Many states let you pick your electricity provider. Check the rules for your new state before you sign.</p>",
        [("Do I need a new internet provider in a new state?", "Often yes, because providers cover specific areas. Check your new ZIP code and confirm with the provider."), ("When should I book internet for a long-distance move?", "Four weeks ahead is ideal, and two weeks at the least."), ("Can I keep my email when I switch providers?", "If your email address is from your old provider, you may lose it. Move to a free address you control before you cancel.")]),
     "new-home-internet-setup": ("New Home Internet Setup: What to Do and in What Order", "New Home Internet Setup Guide",
        "Just bought or built a home? Here is how to get online fast.",
        "<p>A new or newly built home may not have service activated, and a new build might not be listed on a provider's map yet. Contact providers early.</p><h2>Steps</h2><ol class=\"steps\"><li><b>Check availability.</b> Enter your ZIP code, then confirm the exact address with each provider.</li><li><b>Ask about new construction.</b> If the address is new, ask whether service can be built out and how long it takes.</li><li><b>Book installation.</b> Technician slots can be weeks away. Book before closing day if you can.</li><li><b>Plan equipment placement.</b> Put the router in a central, open spot, not in a closet or basement corner.</li><li><b>Test and secure.</b> Run a speed test and set a strong Wi-Fi password.</li></ol>",
        [("Can I get internet at a brand-new home?", "Often yes, but a new address may not be on provider maps yet. Ask the provider directly about new construction."), ("How long does new home internet take?", "It can be days to weeks depending on whether the line is already in place. Book as early as you can."), ("Where should I put my router?", "A central, open, raised spot gives the best Wi-Fi coverage.")]),
    }
    for slug, (title, h1, lead, inner, faq) in V.items():
        save(f"/moving/{slug}", page(f"/moving/{slug}", title, lead + " Checklist, questions to ask and next steps.", h1, lead, inner + "<h2>Moving checklist</h2>" + tl_html() + zipcta(), faq,
             crumbs((h1, f"/moving/{slug}")), chips=["Moving", "Checklist", "Checked Nov 2026"]))

    # ---- hub ----
    cards = "".join(f'<a class="card" href="/moving/{k}"><h3>{esc(P[k]["name"])}</h3><p>Move or transfer service.</p></a>' for k in ORDER if k in P)
    body = f"""<p>Everything you need to get internet working at your new home, from a timeline to provider-specific move guides.</p>
<div class="grid"><a class="card" href="/moving/transfer-internet-to-new-address"><h3>Transfer internet to a new address</h3><p>The timeline and questions to ask.</p></a>
<a class="card" href="/moving/apartment-renters"><h3>Apartments and renters</h3><p>What to check before you sign.</p></a>
<a class="card" href="/moving/moving-to-new-state"><h3>Moving to a new state</h3><p>Internet, utilities and mail order.</p></a>
<a class="card" href="/moving/new-home-internet-setup"><h3>New home setup</h3><p>New builds and first-day steps.</p></a></div>
<h2>Move guides by provider</h2><div class="grid">{cards}</div>{zipcta()}"""
    faq = [("How early should I set up internet before moving?", "Two to four weeks ahead. Four weeks if you move in summer or to another state."), ("Is your site affiliated with internet providers?", "No. YourBillCheck is independent. Official numbers come from each provider's own support pages.")]
    save("/moving", page("/moving", "Moving Internet and Utilities Guides | YourBillCheck", "Moving soon? Guides to transfer internet, set up a new home, and move AT&T, Xfinity, Spectrum, Verizon and other providers.",
         "Moving? Get Your Internet Set Up", "Guides for transferring or switching internet when you move.", body, faq, [("Home", SITE + "/"), ("Moving", SITE + "/moving")], chips=["Movers", "Checked Nov 2026"]))
    return done
