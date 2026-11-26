"""Outage checker pages: /outages hub and /outages/<provider>. Live counts come from the Worker's /api/outage (see outage.js)."""
import html, json
import ui, author

esc = lambda s: html.escape(str(s), quote=True)
SITE = "https://yourbillcheck.com"
DATE = "2026-11-26"
CHECKED = "November 26, 2026"
SITEKEY = "0x4AAAAAAGTvNE1QwmN1ES7r"
PHONE = '<a href="tel:+18884915666">(888) 491-5666</a>'

P = [("xfinity", "Xfinity", "the Xfinity app or xfinity.com/status", True, True),
     ("spectrum", "Spectrum", "the My Spectrum app", True, True),
     ("att", "AT&T", "the myAT&T app or Smart Home Manager", True, True),
     ("verizon", "Verizon", "the My Fios or My Verizon app", True, True),
     ("cox", "Cox", "the Cox app", True, True),
     ("t-mobile", "T-Mobile Home Internet", "the T-Mobile Internet app", True, True),
     ("frontier", "Frontier", "the MyFrontier app", True, True),
     ("centurylink", "CenturyLink", "the My CenturyLink app", True, True),
     ("optimum", "Optimum", "the Optimum app", True, True),
     ("starlink", "Starlink", "the Starlink app", False, False)]
TYPES = [("no-internet", "No internet"), ("slow", "Slow"), ("drops", "Keeps dropping"), ("wifi", "Wi-Fi only"), ("tv", "TV"), ("phone", "Home phone"), ("billing-login", "App or login")]

CSS = ('<style>.ost{border:1px solid var(--line);border-radius:16px;padding:18px 20px;background:#fff;max-width:760px;margin:0 0 22px}'
       '.ost .badge{display:inline-block;padding:6px 12px;border-radius:999px;font-weight:800}.ost .ok{background:#e6f6ef;color:#0a7a55}.ost .hi{background:#fdecea;color:#b42318}'
       '.bars{display:flex;gap:3px;align-items:flex-end;height:90px;margin:14px 0 4px;border-bottom:1px solid var(--line)}.bars i{flex:1;background:var(--mint);border-radius:3px 3px 0 0;min-height:2px}'
       '.ax{display:flex;justify-content:space-between;font-size:12px;color:var(--muted)}.rep button.t{margin:0 8px 8px 0;padding:9px 14px;border-radius:10px;border:1px solid var(--line);background:#fff;cursor:pointer;font:inherit}'
       '.rep button.t.on{background:var(--mint);color:#fff;border-color:var(--mint)}.rep input{padding:11px 12px;border:1px solid var(--line);border-radius:10px;font:inherit;width:160px}'
       '.hint{font-size:14px;color:var(--muted)}</style>')

def widget(slug, name):
    tb = "".join(f'<button type="button" class="t" data-t="{k}">{esc(v)}</button>' for k, v in TYPES)
    return (f'<div class="ost" id="st"><b>{esc(name)} problems reported in the last 24 hours</b><p id="stt" class="hint">Loading reports...</p>'
            '<div class="bars" id="bars"></div><div class="ax"><span>24 hours ago</span><span>Now</span></div><p id="stx" class="hint"></p></div>'
            f'<div class="ost rep"><h2 style="margin-top:0">Having a problem with {esc(name)}?</h2><p>Tell us what is wrong. It takes 10 seconds and helps others nearby.</p>{tb}'
            '<p><label for="oz"><b>Your ZIP code</b></label><br><input id="oz" inputmode="numeric" maxlength="5" placeholder="ZIP code" autocomplete="postal-code"></p>'
            '<div id="ts"></div><p><button class="btn" id="os">Report a problem</button></p><p id="om" class="hint"></p>'
            '<p class="hint">We store only the provider, problem type, the hour and the first 3 digits of your ZIP code. Your IP address is used only to stop duplicate reports and is not stored. '
            'These are reports from YourBillCheck visitors, not an official status from the provider.</p></div>')

def script(slug):
    return ('<script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" async defer></script>'
            '<script>(function(){var P=' + json.dumps(slug) + ',T="",tok="",$=function(i){return document.getElementById(i)};'
            'function load(){fetch("/api/outage?p="+P).then(function(r){return r.json()}).then(function(d){var mx=Math.max.apply(null,d.hours.concat([1]));'
            '$("bars").innerHTML=d.hours.map(function(n){return "<i title=\\""+n+" reports\\" style=\\"height:"+Math.round(n/mx*100)+"%\\"></i>"}).join("");'
            '$("stt").innerHTML=d.status==="elevated"?"<span class=\\"badge hi\\">More reports than usual</span> "+d.lastHour+" report(s) in the last hour.":'
            '(d.total24?"<span class=\\"badge ok\\">No unusual spike</span> "+d.total24+" report(s) in the last 24 hours.":"<span class=\\"badge ok\\">No problems reported</span> No visitor reports in the last 24 hours.");'
            'var ty=Object.keys(d.types).sort(function(a,b){return d.types[b]-d.types[a]});'
            '$("stx").innerHTML=(ty.length?"Most reported: "+ty.slice(0,3).join(", ").replace(/-/g," ")+". ":"")+(d.top.length?"Areas with most reports (ZIP codes starting): "+d.top.map(function(z){return z.zip3+"xx"}).join(", ")+".":"")})'
            '.catch(function(){$("stt").textContent="Reports could not load right now."})}load();'
            'document.querySelectorAll(".t").forEach(function(b){b.onclick=function(){document.querySelectorAll(".t").forEach(function(x){x.classList.remove("on")});b.classList.add("on");T=b.dataset.t}});'
            'var w=setInterval(function(){if(window.turnstile){clearInterval(w);turnstile.render("#ts",{sitekey:' + json.dumps(SITEKEY) + ',callback:function(t){tok=t}})}},300);'
            '$("os").onclick=function(){var z=$("oz").value.trim(),m=$("om");if(!T){m.textContent="Pick what is wrong first.";return}if(!/^\\d{5}$/.test(z)){m.textContent="Enter a 5-digit ZIP code.";return}'
            'if(!tok){m.textContent="Please complete the check above the button.";return}m.textContent="Sending...";'
            'fetch("/api/outage",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({p:P,zip:z,type:T,token:tok})}).then(function(r){return r.json()}).then(function(d){'
            'm.innerHTML=d.ok?(d.dup?"Thanks, we already have your report from this hour.":"Thanks, your report was added.")+" <a href=\\"/internet/"+z+"\\">See other providers at "+z+"</a> if this keeps happening.":(d.error||"Something went wrong.");'
            'if(window.turnstile)turnstile.reset();tok="";setTimeout(load,1500)}).catch(function(){m.textContent="Could not send. Please try again."})}})()</script>')

def build(save):
    for slug, name, app, has_help, has_st in P:
        p = f"/outages/{slug}"
        steps = [f"Check for an outage in {app}. The provider's own status is the most reliable.",
                 "Restart your modem and router: unplug both for 60 seconds, plug in the modem first, then the router.",
                 "Plug a computer into the router with a cable. If it works by cable, the problem is Wi-Fi, not an outage.",
                 "Check the cables and the lights on your equipment." + (f' See <a href="/help/{slug}">{esc(name)} troubleshooting</a>.' if has_help else ' See <a href="/help/router-red-light">what router lights mean</a>.'),
                 "If service is out for a long time, ask the provider whether you qualify for a credit for the time it was down."]
        more = ['<a href="/tools/wifi-or-internet-problem">Is it my Wi-Fi or my internet?</a>', '<a href="/help/internet-not-working">Internet not working</a>']
        if has_st:
            more.insert(0, f'<a href="/speed-test/{slug}">{esc(name)} speed test</a>')
        else:
            more.insert(0, '<a href="/speed-test">Speed test</a>')
        body = (CSS + widget(slug, name)
                + f"<h2>What to do if {esc(name)} is down</h2><ol class=\"steps\">" + "".join(f"<li>{s}</li>" for s in steps) + "</ol>"
                + "<p>" + " · ".join(more) + ' · <a href="/outages">Other providers</a></p>'
                + f'<div class="cta"><div><h3>Tired of {esc(name)} outages?</h3><p>See which other providers serve your address, or call {PHONE} and a specialist will check for you.</p></div><a class="btn alt" href="/">Check my ZIP code</a></div>')
        title = f"Is {name} Down? Live Outage Reports and What to Do"
        desc = f"Is {name} down right now? See {name} problems reported by visitors in the last 24 hours, report your own, and get fix steps."
        faq = [(f"Is {name} down right now?", f"Check the live reports on this page and {app}. Our counts come from visitor reports, so a spike suggests a wider problem, but the provider confirms official outages."),
               (f"How do I report a {name} outage?", f"Report it to {name} in {app} or by phone so it is logged on your account, and add a report here to help others nearby."),
               (f"Will {name} give me a credit for an outage?", f"Ask {name}. Many providers offer a credit for longer outages when you request it, and terms vary.")]
        save(p, ui.shell(p, title, desc, f"Is {name} down?", f"Live problem reports from visitors and what to do next.", author.box(CHECKED) + body, faq,
                         [("Home", SITE + "/"), ("Outages", SITE + "/outages"), (f"{name} outages", SITE + p)], ["Live reports", "Updated every minute"],
                         date=DATE, script=script(slug), checked=CHECKED, author=author.PERSON))
    p = "/outages"
    cards = "".join(f'<a class="card" href="/outages/{s}"><b>Is {esc(n)} down?</b><span>Live reports and fixes</span></a>' for s, n, *_ in P)
    body = ('<div class="grid">' + cards + '</div><h2>How this works</h2><p>Each provider page shows problems reported by YourBillCheck visitors in the last 24 hours, '
            'by hour, with the most common problem types. A spike above normal suggests a wider outage. Always confirm in your provider\'s app, which shows official outages for your address.</p>'
            '<p><a href="/tools/wifi-or-internet-problem">Not sure it is an outage? Check if it is your Wi-Fi</a> · <a href="/speed-test">Run a speed test</a></p>'
            f'<div class="cta"><div><h3>Outages keep happening?</h3><p>Compare providers at your address, or call {PHONE}.</p></div><a class="btn alt" href="/">Check my ZIP code</a></div>')
    save(p, ui.shell(p, "Internet Outage Checker: Is My Internet Down? | YourBillCheck",
                     "Is your internet down? Check live problem reports for Xfinity, Spectrum, AT&T, Verizon, Cox, T-Mobile and more, report an outage and get fix steps.",
                     "Internet outage checker", "Check live problem reports for your provider.", body, None,
                     [("Home", SITE + "/"), ("Outages", SITE + p)], ["10 providers", "Live reports"], date=DATE, checked=CHECKED))
