"""Interactive tools under /tools (batch 1). All client-side: nothing the visitor types is sent or stored."""
import html, json
import ui, author

esc = lambda s: html.escape(str(s), quote=True)
SITE = "https://yourbillcheck.com"
DATE = "2026-11-26"
CHECKED = "November 26, 2026"
PHONE = '<a href="tel:+18884915666">(888) 491-5666</a>'

NETFLIX_SPEED = ("Netflix Help Center: Internet connection speed recommendations", "https://help.netflix.com/en/node/306")
NETFLIX_DATA = ("Netflix Help Center: How to control how much data Netflix uses", "https://help.netflix.com/en/node/87")
ZOOM_BW = ("Zoom: Calculating bandwidth usage for Zoom Meetings", "https://library.zoom.com/admin-corner/network-management/quality-of-service-and-network-best-practices-explainer/calculating-bandwidth-usage-for-zoom-meetings-and-phone")
FCC_GUIDE = ("FCC: Broadband speed guide", "https://www.fcc.gov/consumers/guides/broadband-speed-guide")

CSS = ('<style>.tool{border:1px solid var(--line);border-radius:16px;padding:20px;background:#fff;max-width:760px;margin:0 0 26px}'
       '.tool label{display:block;font-weight:700;margin:12px 0 6px}.tool input,.tool select{width:100%;max-width:320px;padding:11px 12px;border:1px solid var(--line);border-radius:10px;font:inherit}'
       '.tool .row{display:flex;gap:16px;flex-wrap:wrap}.tool .row>div{flex:1 1 200px}.tool .chk{display:flex;gap:8px;align-items:center;font-weight:400;margin:8px 0}'
       '.tool .chk input{width:auto}.res{margin-top:18px;padding:16px;border-radius:12px;background:var(--mint-l,#e8f6f1);display:none}.res.on{display:block}'
       '.res b.big{font:800 30px var(--fd);display:block;margin:4px 0}.hint{font-size:14px;color:var(--muted)}'
       '.q{margin:14px 0}.q p{font-weight:700;margin:0 0 8px}.q button{margin:0 8px 8px 0;padding:9px 16px;border-radius:10px;border:1px solid var(--line);background:#fff;cursor:pointer;font:inherit}'
       '.q button.on{background:var(--mint);color:#fff;border-color:var(--mint)}</style>')

def zipcta(msg):
    return ('<div class="cta"><div><h3>' + esc(msg) + '</h3><p>Enter your ZIP code to see who serves your area, or call ' + PHONE +
            ' and a specialist will check your exact address.</p></div><a class="btn alt" href="/">Check my ZIP code</a></div>')

def src(items):
    return "<h2>Sources</h2><ul>" + "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{esc(t)}</a></li>' for t, u in items) + "</ul>"

def app_ld(path, name, desc):
    return [{"@type": "WebApplication", "name": name, "url": SITE + path, "description": desc, "applicationCategory": "UtilitiesApplication",
             "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "isAccessibleForFree": True}]

def page(save, path, title, desc, h1, lead, body, faq, script, name):
    crumbs = [("Home", SITE + "/"), ("Tools", SITE + "/tools"), (name, SITE + path)]
    save(path, ui.shell(path, title, desc, h1, lead, CSS + author.box(CHECKED) + body, faq, crumbs, ["Free tool", "Nothing is stored"],
                        jsonld_extra=app_ld(path, name, desc), date=DATE, script=script, checked=CHECKED, author=author.PERSON))

TOOLS = [
    ("/outages", "Is my internet down?", "Live outage reports for 10 providers, plus fix steps."),
    ("/tools/promo-price-calculator", "Promo price calculator", "See what your internet bill becomes when the promotion ends, and what it costs over a year."),
    ("/tools/internet-speed-calculator", "Internet speed calculator", "Work out how much download speed your household needs."),
    ("/tools/data-usage-calculator", "Data usage calculator", "Estimate your monthly data and check it against a data cap."),
    ("/tools/streaming-vs-cable-calculator", "Streaming vs cable calculator", "Compare your cable TV bill with the streaming services you would use instead."),
    ("/tools/wifi-or-internet-problem", "Is it my Wi-Fi or my internet?", "Answer a few questions to find where your connection problem is."),
    ("/speed-test", "Internet speed test", "Test your download and upload speed in about 30 seconds."),
]

def build(save):
    # ---------- 1. promo price calculator ----------
    p = "/tools/promo-price-calculator"
    body = ('<div class="tool"><div class="row"><div><label for="pp">Promo price now ($/month)</label><input id="pp" type="number" min="0" step="0.01" placeholder="e.g. 50"></div>'
            '<div><label for="rp">Price after the promo ($/month)</label><input id="rp" type="number" min="0" step="0.01" placeholder="e.g. 80"><p class="hint">Find it in your offer details, order confirmation or bill. If you do not know it, ask your provider: "What will my price be when the promotion ends?"</p></div></div>'
            '<div class="row"><div><label for="fe">Monthly fees and equipment ($)</label><input id="fe" type="number" min="0" step="0.01" placeholder="e.g. 15"></div>'
            '<div><label for="ml">Months left on the promo</label><input id="ml" type="number" min="0" step="1" placeholder="e.g. 3"></div></div>'
            '<p><button class="btn" id="go">Calculate</button></p><div class="res" id="out"></div></div>'
            '<h2>What usually happens when a promo ends</h2><p>Most providers price new customers below their regular rate for 12 or 24 months. When that ends, the bill moves to the regular price, and discounts tied to AutoPay or a bundle can drop at the same time. '
            'You can often keep a lower price by asking for a current offer, switching to a newer plan, or moving to another provider. Read <a href="/guides/internet-promo-ended">what to do when your promo ends</a> and <a href="/guides/why-internet-bill-went-up">why internet bills go up</a>.</p>'
            + zipcta("Is a cheaper provider available at your address?"))
    js = ('<script>(function(){var $=function(i){return document.getElementById(i)},m=function(v){return "$"+v.toFixed(2)};$("go").onclick=function(){'
          'var pp=+$("pp").value||0,rp=+$("rp").value||0,fe=+$("fe").value||0,ml=Math.max(0,Math.round(+$("ml").value||0)),o=$("out");'
          'if(!rp){o.className="res on";o.innerHTML="Enter the price after the promo to see the change.";return}'
          'var now=pp+fe,after=rp+fe,jump=after-now,yr1=Math.min(ml,12)*now+(12-Math.min(ml,12))*after;'
          'o.className="res on";o.innerHTML="Your bill goes from <b>"+m(now)+"</b> to <b>"+m(after)+"</b> a month."+'
          '"<b class=big>"+(jump>=0?"+":"")+m(jump)+" a month</b>That is "+m(jump*12)+" more a year at the regular price. Your next 12 months cost about <b>"+m(yr1)+"</b>."+'
          '(jump>0?" <br><br>Call your provider before the promo ends and ask for a current offer, or <a href=\\"/\\">check other providers at your ZIP</a>.":"")}})()</script>')
    page(save, p, "Internet Promo Price Calculator: What Your Bill Becomes After the Promo",
         "Free calculator: enter your promo price and regular price to see your new monthly bill, the yearly increase and the next 12 months' cost. Nothing is stored.",
         "Internet promo price calculator", "See what your bill becomes when the promotion ends.", body,
         [("Why does my internet bill go up after 12 months?", "Most new-customer prices are promotional for 12 or 24 months. After that the plan moves to the provider's regular price, and some discounts may end too."),
          ("Can I keep my promo price?", "Sometimes. Ask your provider for a current offer or a newer plan before the promo ends, or compare other providers at your address."),
          ("Does this calculator save what I enter?", "No. The math runs in your browser and nothing is sent or stored.")], js, "Promo price calculator")

    # ---------- 2. speed calculator ----------
    p = "/tools/internet-speed-calculator"
    body = ('<div class="tool"><div class="row"><div><label for="s4">4K streams at the same time</label><input id="s4" type="number" min="0" value="0"></div>'
            '<div><label for="sh">HD streams at the same time</label><input id="sh" type="number" min="0" value="1"></div></div>'
            '<div class="row"><div><label for="vc">Video calls at the same time</label><input id="vc" type="number" min="0" value="0"></div>'
            '<div><label for="gm">People gaming online at the same time</label><input id="gm" type="number" min="0" value="0"></div></div>'
            '<div class="row"><div><label for="br">People browsing, social media or music</label><input id="br" type="number" min="0" value="1"></div>'
            '<div><label for="dv">Smart devices (cameras, speakers, TVs idle)</label><input id="dv" type="number" min="0" value="5"></div></div>'
            '<label class="chk"><input type="checkbox" id="up"> Someone uploads large files or streams live</label>'
            '<p><button class="btn" id="go">Calculate my speed</button></p><div class="res" id="out"></div></div>'
            '<h2>How we calculate it</h2><p>We add what each activity needs at the same moment, using the providers\' own figures: Netflix recommends 5 Mbps for Full HD and 15 Mbps for 4K, and Zoom lists about 3 Mbps download and 3.8 Mbps upload for a 1080p group call. '
            'We use 7 Mbps per HD stream and 25 Mbps per 4K stream to leave room for other apps, 5 Mbps per gamer (latency matters more than speed for play; game downloads are where speed helps), 3 Mbps per person browsing, and 0.5 Mbps per smart device, then add 50% headroom because Wi-Fi rarely delivers your full plan speed. '
            'For more, read <a href="/guides/how-much-internet-speed-do-you-need">how much internet speed you need</a>.</p>'
            + zipcta("Find plans at your address that meet this speed"))
    js = ('<script>(function(){var $=function(i){return +document.getElementById(i).value||0};document.getElementById("go").onclick=function(){'
          'var need=$("s4")*25+$("sh")*7+$("vc")*4+$("gm")*5+$("br")*3+$("dv")*0.5,rec=Math.ceil(need*1.5/25)*25;if(rec<50)rec=50;'
          'var tier=rec<=100?"100 Mbps":rec<=300?"300 Mbps":rec<=500?"500 Mbps":rec<=1000?"1 Gig (1,000 Mbps)":"2 Gig or more";'
          'var up=document.getElementById("up").checked||$("vc")>1,o=document.getElementById("out");o.className="res on";'
          'o.innerHTML="Your busiest moment uses about <b>"+Math.round(need)+" Mbps</b>. With headroom we suggest:<b class=big>"+rec+" Mbps download</b>A <b>"+tier+"</b> plan fits."+'
          '(up?" Because of video calls or uploads, pick fiber or a plan with at least 20 Mbps upload.":"")+" <a href=\\"/\\">See plans at your ZIP</a>."}})()</script>')
    page(save, p, "Internet Speed Calculator: How Many Mbps Do You Need?",
         "Free internet speed calculator. Count your streams, video calls, gamers and devices to see the download speed and plan size your household needs.",
         "Internet speed calculator", "Work out the download speed your household needs.", body + src([NETFLIX_SPEED, ZOOM_BW, FCC_GUIDE]),
         [("Is 100 Mbps enough?", "For one or two people streaming in HD and browsing, usually yes. Several 4K streams, video calls and gamers at once usually need 300 Mbps or more."),
          ("Why add headroom?", "Wi-Fi, distance from the router and other devices mean you rarely get your full plan speed on every device, so we add 50%."),
          ("Does upload speed matter?", "Yes for video calls, live streaming and sending large files. Fiber usually offers much higher upload speeds than cable.")], js, "Internet speed calculator")

    # ---------- 3. data usage calculator ----------
    p = "/tools/data-usage-calculator"
    body = ('<div class="tool"><p class="hint">Hours per day for the whole household</p><div class="row">'
            '<div><label for="hd">HD streaming (hours/day)</label><input id="hd" type="number" min="0" step="0.5" value="3"></div>'
            '<div><label for="uh">4K streaming (hours/day)</label><input id="uh" type="number" min="0" step="0.5" value="0"></div></div><div class="row">'
            '<div><label for="vc">HD video calls (hours/day)</label><input id="vc" type="number" min="0" step="0.5" value="0"></div>'
            '<div><label for="bw">Browsing, social, music (hours/day)</label><input id="bw" type="number" min="0" step="0.5" value="3"></div></div><div class="row">'
            '<div><label for="gd">Game or app downloads (GB/month)</label><input id="gd" type="number" min="0" value="0"></div>'
            '<div><label for="cap">Your plan\'s data cap (GB, 0 = no cap)</label><input id="cap" type="number" min="0" value="1200"><p class="hint">1,200 GB is 1.2 TB. See <a href="/fees/xfinity-data-overage">Xfinity\'s data cap</a> and <a href="/fees/data-overage-fee">data overage fees</a>.</p></div></div>'
            '<p><button class="btn" id="go">Estimate my data</button></p><div class="res" id="out"></div></div>'
            '<h2>The numbers we use</h2><p>Netflix says HD uses up to 3 GB an hour and 4K up to 7 GB an hour. A 1080p group video call at Zoom\'s listed 3 Mbps down and 3.8 Mbps up works out to about 3 GB an hour. '
            'We estimate browsing, social media and music at 0.15 GB an hour; video-heavy social apps use more. Real use varies by app and settings, so treat the result as an estimate and check your provider\'s usage meter.</p>'
            + zipcta("Want a plan with no data cap?"))
    js = ('<script>(function(){var $=function(i){return +document.getElementById(i).value||0};document.getElementById("go").onclick=function(){'
          'var gb=($("hd")*3+$("uh")*7+$("vc")*3+$("bw")*0.15)*30+$("gd"),cap=$("cap"),o=document.getElementById("out");o.className="res on";'
          'var t="You use about:<b class=big>"+Math.round(gb).toLocaleString()+" GB a month</b>";'
          'if(cap>0){var pct=Math.round(gb/cap*100);t+=pct>=100?"That is <b>over your "+cap.toLocaleString()+" GB cap</b>. You may pay overage charges; an unlimited plan or a provider without caps could cost less.":pct>=80?"That is "+pct+"% of your cap, close to the limit in a busy month.":"That is "+pct+"% of your cap, comfortably under it."}'
          'o.innerHTML=t+" <a href=\\"/\\">Compare plans at your ZIP</a>."}})()</script>')
    page(save, p, "Internet Data Usage Calculator: Will You Hit Your Data Cap?",
         "Estimate how many GB of home internet data you use a month from streaming, video calls and downloads, and check it against your plan's data cap.",
         "Internet data usage calculator", "Estimate your monthly data and check it against a data cap.", body + src([NETFLIX_DATA, ZOOM_BW]),
         [("How much data does streaming use?", "Netflix lists up to 3 GB an hour for HD and up to 7 GB an hour for 4K."),
          ("Is 1.2 TB a month enough?", "For most households, yes. Heavy 4K streaming in a large household, or many large game downloads, can go past it."),
          ("What happens if I go over my cap?", "It depends on the provider. Some charge for extra blocks of data and some sell unlimited add-ons. See our data overage fee guide.")], js, "Data usage calculator")

    # ---------- 4. streaming vs cable ----------
    p = "/tools/streaming-vs-cable-calculator"
    svc = [("Live TV service (YouTube TV, Hulu + Live TV, Sling, Fubo)", "lv"), ("Netflix", "nf"), ("Disney+ / Hulu / ESPN+", "dh"), ("Max", "mx"),
           ("Peacock", "pc"), ("Paramount+", "pm"), ("Prime Video", "pv"), ("Other", "ot")]
    rows = "".join(f'<div><label for="{k}">{esc(n)} ($/month)</label><input id="{k}" type="number" min="0" step="0.01" placeholder="0"></div>' for n, k in svc)
    body = ('<div class="tool"><div class="row"><div><label for="tv">Your TV part of the cable bill ($/month)</label><input id="tv" type="number" min="0" step="0.01" placeholder="e.g. 110">'
            '<p class="hint">Include the TV package, box rental, broadcast TV and regional sports fees.</p></div>'
            '<div><label for="ad">Extra internet cost if you drop TV ($/month)</label><input id="ad" type="number" min="0" step="0.01" placeholder="0"><p class="hint">Some bundles cost more for internet alone, or you may want a faster plan.</p></div></div>'
            '<h3>Streaming you would use instead</h3><p class="hint">Enter the price on each service\'s own site; prices change often.</p><div class="row">' + rows + '</div>'
            '<p><button class="btn" id="go">Compare</button></p><div class="res" id="out"></div></div>'
            '<p>TV fees explained: <a href="/fees/broadcast-tv-fee">broadcast TV fee</a> · <a href="/fees/regional-sports-fee">regional sports fee</a>. '
            'Streaming needs good internet: use the <a href="/tools/internet-speed-calculator">speed calculator</a> and <a href="/tools/data-usage-calculator">data calculator</a>.</p>'
            + zipcta("Cutting cable? Make sure your internet can handle it"))
    keys = json.dumps([k for _, k in svc])
    js = ('<script>(function(){var $=function(i){return +document.getElementById(i).value||0},m=function(v){return "$"+Math.abs(v).toFixed(2)};document.getElementById("go").onclick=function(){'
          'var s=' + keys + '.reduce(function(a,k){return a+$(k)},0)+$("ad"),tv=$("tv"),d=tv-s,o=document.getElementById("out");o.className="res on";'
          'if(!tv){o.innerHTML="Enter the TV part of your cable bill.";return}'
          'o.innerHTML="Cable TV: <b>"+m(tv)+"</b> a month. Streaming instead: <b>"+m(s)+"</b> a month.<b class=big>"+(d>=0?"You save "+m(d):"Streaming costs "+m(d)+" more")+" a month</b>That is "+m(d*12)+" a year."}})()</script>')
    page(save, p, "Streaming vs Cable Calculator: Will Cutting Cable Save You Money?",
         "Compare the TV part of your cable bill with the streaming services you would pay for instead, and see the monthly and yearly difference.",
         "Streaming vs cable calculator", "Will cutting the cord actually save you money?", body,
         [("Is streaming cheaper than cable?", "Often, but not always. A live TV streaming service plus several apps can cost as much as cable. Add up what you would really use."),
          ("Do I need faster internet to stream?", "One HD stream needs about 5 Mbps per Netflix; several 4K streams at once need much more. Use our speed calculator."),
          ("Does this calculator store my numbers?", "No. Everything runs in your browser.")], js, "Streaming vs cable calculator")

    # ---------- 5. wifi or internet ----------
    p = "/tools/wifi-or-internet-problem"
    qs = [("wired", "Is a device plugged into the router with a cable also slow or offline?"),
          ("all", "Are all your devices affected, not just one?"),
          ("near", "Is it still bad when you stand next to the router?"),
          ("lights", "Is a light on the modem or router red, orange or blinking unusually?")]
    qhtml = "".join(f'<div class="q" data-k="{k}"><p>{esc(t)}</p><button type="button" data-v="1">Yes</button><button type="button" data-v="0">No</button><button type="button" data-v="2">Not sure</button></div>' for k, t in qs)
    body = ('<div class="tool">' + qhtml + '<div class="res" id="out"></div></div>'
            '<h2>Next steps</h2><ul><li><a href="/speed-test">Run a speed test</a> next to the router and in the room with the problem.</li>'
            '<li><a href="/help/router-red-light">What your router lights mean</a></li><li><a href="/help">Provider troubleshooting guides</a></li></ul>'
            + zipcta("Outages and slow speeds every month? Compare providers"))
    js = ('<script>(function(){var a={};document.querySelectorAll(".q").forEach(function(q){q.querySelectorAll("button").forEach(function(b){b.onclick=function(){'
          'q.querySelectorAll("button").forEach(function(x){x.classList.remove("on")});b.classList.add("on");a[q.dataset.k]=+b.dataset.v;r()}})});'
          'function r(){if(Object.keys(a).length<4)return;var o=document.getElementById("out"),t;'
          'if(a.wired===1||a.lights===1)t="<b class=big>Likely your internet service</b>A wired device or the modem lights point to the connection coming into your home. Restart the modem and router (unplug 60 seconds), check your provider\'s outage page or app, then call your provider if it continues.";'
          'else if(a.all===0)t="<b class=big>Likely that one device</b>Restart it, forget and rejoin the Wi-Fi network, and update its software.";'
          'else if(a.near===0)t="<b class=big>Likely Wi-Fi range</b>Speed is fine near the router, so the signal is not reaching. Move the router higher and central, away from walls and appliances, or add a mesh system or extender.";'
          'else t="<b class=big>Could be either</b>Restart the modem and router, then <a href=\\"/speed-test\\">run a speed test</a> with a device plugged in by cable. If the wired test is slow too, it is your service; if not, it is your Wi-Fi.";'
          'o.className="res on";o.innerHTML=t}})()</script>')
    page(save, p, "Is It My Wi-Fi or My Internet? Quick Problem Checker",
         "Answer four quick questions to find out whether slow or dropped internet is your Wi-Fi, one device or your provider's service, with what to do next.",
         "Is it my Wi-Fi or my internet?", "Answer four questions to find where the problem is.", body,
         [("How do I know if it is my provider or my Wi-Fi?", "Plug a computer into the router with a cable. If it is still slow or offline, the problem is usually the service. If it works, the problem is Wi-Fi."),
          ("Should I restart my router?", "Yes. Unplug the modem and router for about 60 seconds, plug the modem in first, then the router."),
          ("When should I call my provider?", "When a wired device is also slow or offline after a restart, or the modem shows a warning light.")], js, "Wi-Fi or internet problem checker")

    # ---------- hub ----------
    p = "/tools"
    cards = "".join(f'<a class="card" href="{u}"><b>{esc(n)}</b><span>{esc(d)}</span></a>' for u, n, d in TOOLS)
    body = ('<div class="grid">' + cards + '</div><p>More tools are on the way: fiber finder, low-income internet checker and more. '
            'All tools are free, and nothing you type is stored.</p>' + zipcta("Ready to compare providers?"))
    save(p, ui.shell(p, "Free Internet Tools: Speed, Data, Promo Price and Bill Calculators | YourBillCheck",
                     "Free internet tools: speed test, speed and data calculators, promo price calculator, streaming vs cable and a Wi-Fi problem checker.",
                     "Free internet tools", "Calculators and checkers to help you pay less and get the right internet.", body, None,
                     [("Home", SITE + "/"), ("Tools", SITE + p)], ["Free", "No sign-up"], date=DATE, checked=CHECKED))
