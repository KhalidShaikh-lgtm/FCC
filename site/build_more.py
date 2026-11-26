"""Batch 4 tools: low-income internet checker, new-mover setup tool, bundle savings calculator, promo-end reminder (callback lead)."""
import html, json
import ui, author
import build_finders as BF

esc = lambda s: html.escape(str(s), quote=True)
SITE = "https://yourbillcheck.com"
DATE = "2026-11-26"
CHECKED = "November 26, 2026"
PHONE = '<a href="tel:+18884915666">(888) 491-5666</a>'
CSS = BF.CSS + ('<style>.tool label.chk{display:flex;gap:8px;align-items:center;margin:6px 0;font-weight:400}.tool label.chk input{width:auto}'
                '.prog{border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:10px 0}.prog h3{margin:0 0 4px}.tool .fld{display:block;font-weight:700;margin:12px 0 6px}'
                '.tool .fld+input,.tool input.w{width:100%;max-width:320px}</style>')

def page(save, path, title, desc, h1, lead, body, faq, script, name, sources):
    ld = [{"@type": "WebApplication", "name": name, "url": SITE + path, "description": desc, "applicationCategory": "UtilitiesApplication",
           "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "isAccessibleForFree": True}]
    save(path, ui.shell(path, title, desc, h1, lead, CSS + author.box(CHECKED) + body + (BF.src(sources) if sources else ""), faq,
                        [("Home", SITE + "/"), ("Tools", SITE + "/tools"), (name, SITE + path)], ["Free tool", "Sources listed"],
                        jsonld_extra=ld, date=DATE, script=script, checked=CHECKED, author=author.PERSON))

# Low-income programs: facts verified Nov 26, 2026 from the listed sources.
PROGS = [
    {"id": "lifeline", "name": "Lifeline (FCC)", "who": "any", "price": "Up to $9.25 off a month (up to $34.25 on Tribal lands)",
     "detail": "A federal discount you add to a phone or internet plan from a participating company. One per household.",
     "q": ["snap", "medicaid", "ssi", "housing", "vets", "tribal", "inc135"], "apply": "https://www.lifelinesupport.org/", "applyt": "Apply through the National Verifier (lifelinesupport.org) or call (800) 234-9473"},
    {"id": "xfinity", "name": "Xfinity Internet Essentials", "who": "Xfinity", "price": "$14.95/month for up to 75 Mbps, or Internet Essentials Plus $29.95/month for up to 100 Mbps",
     "detail": "For new Xfinity internet customers (none in the last 90 days) with no Comcast debt under a year old. Equipment included.",
     "q": ["snap", "medicaid", "nslp"], "apply": "https://apply.internetessentials.com/", "applyt": "Apply at apply.internetessentials.com"},
    {"id": "spectrum", "name": "Spectrum Internet Assist", "who": "Spectrum", "price": "$25/month for 50 Mbps; a discounted version is $15/month for qualifying households",
     "detail": "Qualify through the National School Lunch Program (including CEP schools) or Supplemental Security Income for those 65 and older, among others.",
     "q": ["nslp", "ssi"], "apply": "https://www.spectrum.com/internet/spectrum-internet-assist", "applyt": "Details at spectrum.com/internet/spectrum-internet-assist"},
    {"id": "att", "name": "Access from AT&T", "who": "AT&T", "price": "Discounted AT&T Fiber or Internet Air; AT&T Internet Air is $25 off for qualifying homes. Price depends on the speed at your address.",
     "detail": "Qualify through one of 18 federal programs (including SNAP, school lunch, public housing and Veterans Pension) or household income below 200% of federal poverty guidelines. Recertify yearly.",
     "q": ["snap", "nslp", "housing", "vets", "inc200"], "apply": "https://www.att.com/internet/access/", "applyt": "Apply at att.com/access or call 855-220-5211"},
    {"id": "cox", "name": "Cox ConnectAssist / Connect2Compete", "who": "Cox", "price": "ConnectAssist $30/month for up to 100 Mbps; Connect2Compete $9.95/month for families with K-12 students",
     "detail": "ConnectAssist: a government assistance program such as SNAP, Medicaid or Veterans Pension. Connect2Compete: a K-12 student plus a program such as SNAP or school lunch. No annual contract.",
     "q": ["snap", "medicaid", "vets", "nslp", "housing", "ssi", "tribal"], "apply": "https://www.cox.com/residential/internet/low-cost-internet-plans.html", "applyt": "Check eligibility at cox.com low-cost internet plans"},
    {"id": "optimum", "name": "Optimum Advantage Internet", "who": "Optimum", "price": "As low as $14.99/month for 50 Mbps",
     "detail": "For eligible households, including seniors 65+ receiving SSI; other routes include school lunch, public housing or low household income. Rules vary by state.",
     "q": ["ssi", "nslp", "housing", "inc200"], "apply": "https://www.optimum.com/articles/internet/cheap-internet-service", "applyt": "Details from Optimum"},
]
SOURCES_LI = [("FCC: Lifeline program for low-income consumers", "https://www.fcc.gov/lifeline-consumers"),
              ("Comcast: All about Internet Essentials (Aug 2025)", "https://florida.comcast.com/2025/08/12/internet-essentials"),
              ("Spectrum: Residential broadband services and pricing disclosure", "https://www.spectrum.com/policies/spectrum-broadband-disclosure"),
              ("AT&T: Learn about Access from AT&T", "https://www.att.com/support/article/dsl-high-speed/KM1399655/"),
              ("AT&T newsroom: Access discount on Internet Air (Apr 27, 2026)", "https://about.att.com/story/2026/access-aia-discount.html"),
              ("Cox: Low-cost internet plans", "https://www.cox.com/residential/internet/low-cost-internet-plans.html"),
              ("Optimum: How to get affordable internet", "https://www.optimum.com/articles/internet/cheap-internet-service"),
              ("HHS: Poverty guidelines", "https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines")]
Q = [("snap", "SNAP (food stamps)"), ("medicaid", "Medicaid"), ("ssi", "Supplemental Security Income (SSI)"), ("nslp", "Free or reduced-price school lunch (NSLP / CEP school)"),
     ("housing", "Federal public housing assistance"), ("vets", "Veterans or Survivors Pension"), ("tribal", "Tribal assistance program"),
     ("inc135", "Household income at or below 135% of federal poverty guidelines"), ("inc200", "Household income below 200% of federal poverty guidelines")]

def build(save):
    # 1 low-income checker
    p = "/tools/low-income-internet-checker"
    chks = "".join(f'<label class="chk"><input type="checkbox" value="{k}"> {esc(v)}</label>' for k, v in Q)
    provs = '<option value="">Not sure / any</option>' + "".join(f'<option>{w}</option>' for w in ["Xfinity", "Spectrum", "AT&T", "Cox", "Optimum"])
    body = ('<div class="tool"><b>Does anyone in your home get any of these?</b>' + chks +
            '<span class="fld">Which provider serves you (if you know)?</span><select id="pv">' + provs + '</select>'
            '<p><button class="btn" id="go" type="button">Show programs I may qualify for</button></p><div class="res" id="out"></div></div>'
            '<p class="hint">Programs and prices change. Each provider confirms eligibility and may ask for documents. If you are 65 or older, many programs accept SSI. '
            'Not sure which providers serve you? Use the <a href="/tools/internet-availability-checker">availability checker</a>.</p>'
            '<div class="cta"><div><h3>Want help applying or choosing?</h3><p>Call ' + PHONE + '. We can check which low-cost plans reach your address.</p></div><a class="btn alt" href="tel:+18884915666">Call (888) 491-5666</a></div>')
    js = ('<script>(function(){var P=' + json.dumps(PROGS) + ';document.getElementById("go").onclick=function(){'
          'var s=[].slice.call(document.querySelectorAll(".tool input[type=checkbox]:checked")).map(function(c){return c.value}),pv=document.getElementById("pv").value,o=document.getElementById("out");'
          'if(!s.length){o.innerHTML="<p>Tick at least one box. If none apply, ask providers about their cheapest regular plan, or see <a href=\\"/guides/how-to-lower-your-internet-bill\\">how to lower your bill</a>.</p>";return}'
          'var m=P.filter(function(x){return (x.who==="any"||!pv||x.who===pv)&&x.q.some(function(q){return s.indexOf(q)>-1})});'
          'o.innerHTML=m.length?"<span class=\\"big\\">You may qualify for "+m.length+" program"+(m.length>1?"s":"")+"</span>"+m.map(function(x){return "<div class=\\"prog\\"><h3>"+x.name+"</h3><p><b>"+x.price+"</b></p><p>"+x.detail+"</p><p><a href=\\""+x.apply+"\\" target=\\"_blank\\" rel=\\"noopener\\">"+x.applyt+"</a></p></div>"}).join("")+"<p>Lifeline can often be combined with a provider plan; ask the provider.</p>":"<p>No match from your answers for that provider. Try \\"Not sure / any\\", or call (888) 491-5666.</p>"}})()</script>')
    page(save, p, "Low-Income Internet Checker: Programs You May Qualify For (2026)",
         "Check which low-income internet programs you may qualify for: Lifeline, Xfinity Internet Essentials, Spectrum Internet Assist, Access from AT&T, Cox and Optimum, with prices and how to apply.",
         "Low-income internet checker", "Find discounted internet programs you may qualify for.", body,
         [("What replaced the Affordable Connectivity Program?", "The ACP ended in 2024. Lifeline still offers up to $9.25 a month off, and many providers run their own low-cost plans for households on SNAP, Medicaid, SSI or school lunch."),
          ("Can seniors get cheap internet?", "Yes, usually through income or benefits rather than age. Seniors on SSI qualify for Lifeline and for programs such as Spectrum Internet Assist and Optimum Advantage."),
          ("Do I need documents?", "Often yes: proof of the program you are on, such as a benefits letter or school lunch letter.")], js, "Low-income internet checker", SOURCES_LI)

    # 2 new-mover setup tool
    p = "/tools/moving-internet-setup"
    body = ('<div class="tool"><span class="fld">New address ZIP code</span><input id="zz" class="w" inputmode="numeric" maxlength="5" placeholder="e.g. 30301">'
            '<span class="fld">Move-in date</span><input id="md" class="w" type="date"><p><button class="btn" id="go" type="button">Build my plan</button></p><div class="res" id="out"></div></div>'
            '<p>More help: <a href="/moving">moving guides</a> · <a href="/moving/transfer-internet-to-new-address">transfer internet to a new address</a> · <a href="/help/move-internet-service">move your service</a></p>'
            '<div class="cta"><div><h3>Let us set up internet at your new place</h3><p>Call ' + PHONE + ' and we will check providers at your new address and book the install.</p></div><a class="btn alt" href="tel:+18884915666">Call (888) 491-5666</a></div>')
    js = ('<script>(function(){' + BF.CORE +
          'function d(dt,n){var x=new Date(dt.getTime()+n*864e5);return x.toLocaleDateString("en-US",{weekday:"short",month:"short",day:"numeric"})}'
          'document.getElementById("go").onclick=function(){var z=$("zz").value.trim(),v=$("md").value,o=$("out");if(!/^\\d{5}$/.test(z)||!v){o.innerHTML="Enter the new ZIP code and your move-in date.";return}'
          'var m=new Date(v+"T12:00:00");var steps=[[-28,"Check providers at the new address (below) and compare prices after any promo."],[-21,"Call your current provider: ask whether you can transfer service and what fees apply. Ask about any contract or early termination fee."],'
          '[-14,"Order service at the new address and book the install for move-in day or the day before. Write down the order number."],[-7,"Confirm the install appointment. Plan to cancel or transfer the old service the day after you move out."],'
          '[0,"Move-in day: be home for the install, then run a speed test."],[1,"Return old equipment and keep the receipt to avoid an unreturned equipment fee."]];'
          'o.innerHTML="<span class=\\"big\\">Your internet moving plan</span><ol class=\\"steps\\">"+steps.map(function(s){return "<li><b>"+d(m,s[0])+":</b> "+s[1]+"</li>"}).join("")+"</ol><p>Checking providers at "+z+"...</p>";'
          'look(z,function(err,dd){if(err){o.innerHTML+="<p>"+err+"</p>";return}var rs=dd.rows.slice().sort(function(a,b){return (a.t>=60&&a.t<=61)-(b.t>=60&&b.t<=61)||b.cov-a.cov||b.dn-a.dn}).slice(0,8);'
          'o.innerHTML=o.innerHTML.replace("<p>Checking providers at "+z+"...</p>","")+"<h3>Providers at "+z+(dd.city?" ("+dd.city+")":"")+"</h3>"+tbl(rs)+"<p><a href=\\"/internet/"+z+"\\">See plans and prices for "+z+"</a>."+CALL+"</p>"})}})()</script>')
    page(save, p, "Moving? Internet Setup Planner With Dates and Providers at Your New Address",
         "Enter your new ZIP code and move-in date to get a dated internet setup checklist and the providers that serve your new address.",
         "Internet setup planner for your move", "A dated checklist plus the providers at your new address.", body,
         [("How far ahead should I set up internet when moving?", "About two to four weeks before you move, so you can book an install for move-in day."),
          ("Should I transfer or switch providers when I move?", "Compare both. Your provider may not serve the new address, and new-customer offers from another provider can cost less.")], js, "Moving internet planner",
         [BF.FCC_BDC])

    # 3 bundle savings calculator
    p = "/tools/bundle-savings-calculator"
    body = ('<div class="tool"><b>What you pay now ($/month)</b><div class="row" style="display:flex;gap:16px;flex-wrap:wrap">'
            + "".join(f'<div><span class="fld">{esc(n)}</span><input id="{k}" class="w" type="number" min="0" step="0.01" placeholder="0"></div>' for n, k in [("Home internet", "ci"), ("Mobile (all lines)", "cm"), ("TV", "ct"), ("Home phone", "cp")]) +
            '</div><b>Bundle quote you are considering ($/month)</b><div style="display:flex;gap:16px;flex-wrap:wrap"><div><span class="fld">Bundle price</span><input id="bp" class="w" type="number" min="0" step="0.01" placeholder="e.g. 110"></div>'
            '<div><span class="fld">Months the bundle price lasts</span><input id="bm" class="w" type="number" min="1" value="12"></div><div><span class="fld">Price after that ($/month)</span><input id="ba" class="w" type="number" min="0" step="0.01" placeholder="e.g. 150"></div>'
            '<div><span class="fld">One-time costs (install, phones, fees)</span><input id="bo" class="w" type="number" min="0" step="0.01" placeholder="0"></div></div>'
            '<p><button class="btn" id="go" type="button">Compare over 2 years</button></p><div class="res" id="out"></div></div>'
            '<p>Internet and mobile bundles from cable and fiber companies can cut the total, but the saving often depends on AutoPay, a promo period and keeping every service. '
            'Ask for the price after the promo in writing. See the <a href="/tools/promo-price-calculator">promo price calculator</a>.</p>'
            '<div class="cta"><div><h3>Want us to find a bundle at your address?</h3><p>Call ' + PHONE + '.</p></div><a class="btn alt" href="tel:+18884915666">Call (888) 491-5666</a></div>')
    js = ('<script>(function(){var $=function(i){return +document.getElementById(i).value||0},m=function(v){return "$"+Math.abs(v).toFixed(0)};document.getElementById("go").onclick=function(){'
          'var now=$("ci")+$("cm")+$("ct")+$("cp"),bp=$("bp"),bm=Math.min(24,Math.max(1,$("bm"))),ba=$("ba")||bp,o=document.getElementById("out");if(!now||!bp){o.innerHTML="Enter what you pay now and the bundle price.";return}'
          'var cur=now*24,bun=bp*bm+ba*(24-bm)+$("bo"),d=cur-bun;o.className="res on";'
          'o.innerHTML="Over 2 years: now <b>"+m(cur)+"</b>, bundle <b>"+m(bun)+"</b>.<span class=\\"big "+(d>=0?"yes":"no")+"\\">"+(d>=0?"Bundle saves "+m(d):"Bundle costs "+m(d)+" more")+"</span>That is about "+m(d/24)+" a month on average."}})()</script>')
    page(save, p, "Bundle Savings Calculator: Is an Internet and Mobile Bundle Worth It?",
         "Compare what you pay now for internet, mobile, TV and phone with a bundle quote over two years, including the price after the promo and one-time costs.",
         "Bundle savings calculator", "Is the bundle really cheaper over two years?", body,
         [("Are internet and mobile bundles worth it?", "Often, if you would use every service anyway. Check the price after the promo, AutoPay requirements and what happens if you cancel one part."),
          ("Why compare over two years?", "Most promos last 12 to 24 months, so a two-year view shows the real cost after the price goes up.")], js, "Bundle savings calculator", None)

    # 4 promo-end reminder (callback lead)
    p = "/tools/promo-end-reminder"
    consent = ("By checking this box, I agree that YourBillCheck and its partner sales agents may contact me by phone call, text message or email, including with an automatic dialer or prerecorded messages, "
               "at the number I entered, about my internet, TV and mobile services. Consent is not a condition of any purchase. Message and data rates may apply. Reply STOP to opt out. See our Privacy Policy and Terms.")
    provs = "".join(f"<option>{w}</option>" for w in ["Xfinity", "Spectrum", "AT&T", "Verizon", "Cox", "T-Mobile", "Frontier", "Optimum", "CenturyLink", "Other"])
    body = ('<div class="tool"><p>Promo prices usually jump when they end. Tell us when yours ends and a specialist will call you about 30 days before, with options to keep your price down.</p>'
            '<span class="fld">First name</span><input id="fn" class="w" autocomplete="given-name">'
            '<span class="fld">Mobile number</span><input id="ph" class="w" type="tel" inputmode="tel" autocomplete="tel" placeholder="(555) 123-4567">'
            '<span class="fld">ZIP code</span><input id="zz" class="w" inputmode="numeric" maxlength="5">'
            '<span class="fld">Current provider</span><select id="pv">' + provs + '</select>'
            '<span class="fld">When does your promo price end?</span><input id="pe" class="w" type="month">'
            '<span class="fld">Current monthly bill ($, optional)</span><input id="mb" class="w" type="number" min="0" step="0.01">'
            '<div style="position:absolute;left:-9999px" aria-hidden="true"><input id="web" tabindex="-1" autocomplete="off"></div>'
            '<label class="chk" style="font-size:13px;color:var(--muted);align-items:flex-start"><input type="checkbox" id="cs" style="margin-top:3px"> <span id="ct">' + esc(consent) + '</span></label>'
            '<p><button class="btn" id="go" type="button">Remind me</button></p><p id="msg"></p></div>'
            '<p>Prefer to talk now? Call ' + PHONE + '. Want the numbers first? Use the <a href="/tools/promo-price-calculator">promo price calculator</a>.</p>')
    js = ('<script>(function(){var $=function(i){return document.getElementById(i)};$("go").onclick=function(){var m=$("msg"),fn=$("fn").value.trim(),d=$("ph").value.replace(/\\D/g,""),z=$("zz").value.trim(),pe=$("pe").value;'
          'if(d.length===11&&d[0]==="1")d=d.slice(1);if(!fn){m.textContent="Enter your first name.";return}if(d.length!==10){m.textContent="Enter a 10-digit US mobile number.";return}'
          'if(!/^\\d{5}$/.test(z)){m.textContent="Enter your 5-digit ZIP code.";return}if(!pe){m.textContent="Pick the month your promo ends.";return}if(!$("cs").checked){m.textContent="Check the box so we can call you.";return}if($("web").value)return;'
          'm.textContent="Sending...";var p={first_name:fn,phone:d,zip:z,current_provider:$("pv").value,monthly_price:$("mb").value||"",promo_status:"ends "+pe,goal:"promo-reminder",entry:"promo-reminder",'
          'recommendation:"Call ~30 days before "+pe+" about keeping the price down",consent:true,consent_text:$("ct").textContent.trim(),consent_time:new Date().toISOString(),page_url:location.href.split("?")[0],source:"yourbillcheck.com"};'
          'try{var q=new URLSearchParams(location.search);["utm_source","utm_medium","utm_campaign","utm_content","utm_term","fbclid"].forEach(function(k){if(q.get(k))p[k]=q.get(k)})}catch(e){}'
          'fetch("https://yourbillcheck-leads.khalid-shaikh.workers.dev",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(p)}).then(function(r){return r.json()}).then(function(r){'
          'm.innerHTML=r.ok?"<b>Done.</b> We will call you before your promo ends. Need help sooner? Call <a href=\\"tel:+18884915666\\">(888) 491-5666</a>.":"Something went wrong. Please call (888) 491-5666."}).catch(function(){m.textContent="Could not send. Please call (888) 491-5666."})}})()</script>')
    save(p, ui.shell(p, "Internet Promo End Reminder: Get a Call Before Your Price Goes Up",
                     "Tell us when your internet promo ends and a specialist will call about 30 days before with options to keep your bill down. Free.",
                     "Get reminded before your promo ends", "We call you about 30 days before the price goes up.", CSS + body,
                     [("Why does my bill go up when the promo ends?", "Promo prices for new customers usually last 12 or 24 months. After that, the regular price applies."),
                      ("Is this free?", "Yes. We may earn a commission if you switch through us, at no cost to you.")],
                     [("Home", SITE + "/"), ("Tools", SITE + "/tools"), ("Promo end reminder", SITE + p)], ["Free", "We call you"], date=DATE, script=js, checked=CHECKED))
