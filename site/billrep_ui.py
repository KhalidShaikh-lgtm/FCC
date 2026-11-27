"""Reader bill-increase report box for /bills/<provider>-bill-went-up pages. Backend: /api/bill-report (site/billrep.js in the Worker)."""
import json, html
SITEKEY = "0x4AAAAAAGTvNE1QwmN1ES7r"
REASONS = [("promo-ended", "Promo or price lock ended"), ("price-increase", "Provider raised prices"), ("new-fee", "New or higher fee"),
           ("equipment", "Equipment charge"), ("lost-discount", "Lost a discount (e.g. AutoPay)"), ("plan-change", "Plan or package changed"),
           ("tv-fees", "TV / broadcast or sports fee"), ("unknown", "No reason given / don't know")]

def key_from_path(path):
    s = path.rstrip("/").split("/")[-1]
    return s[:-len("-bill-went-up")] if s.endswith("-bill-went-up") else None

def box(pkey, name):
    n = html.escape(name)
    opts = "".join(f'<option value="{k}">{html.escape(t)}</option>' for k, t in REASONS)
    return ('<style>.br{border:2px solid var(--ink);border-radius:18px;padding:20px 22px;margin:26px 0;background:#fff}.br h2{margin:0 0 6px}'
            '.br .g{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:10px 0}.br label{font-size:13px;color:var(--muted)}'
            '.br input,.br select{width:100%;padding:10px;font-size:16px;box-sizing:border-box}.br .st{background:#f4f7fa;border-radius:12px;padding:12px 14px;margin:8px 0 12px}</style>'
            f'<div class="br" id="report"><h2>Did your {n} bill go up? Tell other readers</h2>'
            f'<p style="margin:0 0 6px">Add your increase in 20 seconds. We publish only combined totals, never single reports, and never your name or full ZIP code.</p>'
            '<div class="st" id="brS" hidden></div>'
            '<div class="g"><label>Old monthly bill ($)<input id="brO" type="number" inputmode="decimal" min="5" step="0.01"></label>'
            '<label>New monthly bill ($)<input id="brN" type="number" inputmode="decimal" min="5" step="0.01"></label>'
            '<label>Month it went up<input id="brM" type="month"></label>'
            '<label>Your ZIP code<input id="brZ" inputmode="numeric" maxlength="5" autocomplete="postal-code"></label></div>'
            f'<label>Reason the provider gave<select id="brR">{opts}</select></label>'
            '<div id="brT" style="margin:10px 0"></div><p style="margin:8px 0 0"><button class="btn" id="brB" type="button">Add my report</button></p><p id="brX" role="status" style="margin:8px 0 0"></p></div>'
            '<script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" async defer></script>'
            '<script>(function(){var P=' + json.dumps(pkey) + ',N=' + json.dumps(name) + ',tok="",$=function(i){return document.getElementById(i)};'
            'function money(v){return "$"+v}'
            'function load(){fetch("/api/bill-report?p="+P).then(function(r){return r.json()}).then(function(d){var s=$("brS");if(!d||!d.show){if(d&&d.n>0){s.hidden=false;s.textContent=d.n+" reader report"+(d.n>1?"s":"")+" so far. We show typical amounts once there are 5."}return}'
            's.hidden=false;s.innerHTML="<b>"+d.n+" readers reported a "+N+" increase in the last 3 months.</b> Typical increase: "+money(d.median)+" a month (most between "+money(d.p25)+" and "+money(d.p75)+")."+(d.top&&d.top.length?" Most common reason: "+d.top[0].reason+".":"")}).catch(function(){})}'
            'load();var w=setInterval(function(){if(window.turnstile){clearInterval(w);turnstile.render("#brT",{sitekey:' + json.dumps(SITEKEY) + ',callback:function(t){tok=t}})}},300);'
            '$("brB").onclick=function(){var m=$("brX"),o=parseFloat($("brO").value),nw=parseFloat($("brN").value),mo=$("brM").value,z=$("brZ").value.trim();'
            'if(!(o>0&&nw>o)){m.textContent="Enter your old and new bill; the new one should be higher.";return}if(!mo){m.textContent="Pick the month it went up.";return}'
            'if(!/^\\d{5}$/.test(z)){m.textContent="Enter your 5-digit ZIP code.";return}if(!tok){m.textContent="Please complete the quick check above.";return}'
            'm.textContent="Sending...";fetch("/api/bill-report",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({p:P,old:o,new:nw,month:mo,zip:z,reason:$("brR").value,token:tok})})'
            '.then(function(r){return r.json()}).then(function(r){if(r.ok){m.innerHTML=r.dup?"Thanks, we already have your report for "+N+" today.":"<b>Thanks.</b> Your $"+r.increase+" increase is counted. Want it back down? Read the steps below or call <a href=\\"tel:+18884915666\\">(888) 491-5666</a>.";'
            'try{navigator.sendBeacon("/api/ev",new Blob([JSON.stringify({e:"report",p:location.pathname,r:document.referrer||""})],{type:"text/plain"}))}catch(e){}setTimeout(load,1500)}else{m.textContent=r.error||"Something went wrong."}'
            'if(window.turnstile)turnstile.reset();tok=""}).catch(function(){m.textContent="Could not send. Please try again."})}})()</script>')
