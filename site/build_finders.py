"""Batch 3 tools: ZIP-based finders built on the FCC Broadband Data Collection data we already serve (zipdata/out/<st>-zips.json via /data/<st>.json).
Data row per provider: [brand index, technology code, max down Mbps, max up Mbps, % of ZIP covered]."""
import html, json, os
import ui, author

esc = lambda s: html.escape(str(s), quote=True)
SITE = "https://yourbillcheck.com"
DATE = "2026-11-26"
CHECKED = "November 26, 2026"
PHONE = '<a href="tel:+18884915666">(888) 491-5666</a>'
HERE = os.path.dirname(os.path.abspath(__file__))
Z3 = open(os.path.join(HERE, "zip3.json")).read()
FCC_MAP = ("FCC National Broadband Map", "https://broadbandmap.fcc.gov/")
FCC_BDC = ("FCC Broadband Data Collection", "https://www.fcc.gov/BroadbandData")

CSS = ('<style>.tool{border:1px solid var(--line);border-radius:16px;padding:20px;background:#fff;max-width:820px;margin:0 0 26px}'
       '.tool input,.tool select{padding:11px 12px;border:1px solid var(--line);border-radius:10px;font:inherit}.tool input{width:150px}'
       '.res{margin-top:18px}.res table{width:100%;border-collapse:collapse}.res th,.res td{text-align:left;padding:9px 8px;border-bottom:1px solid var(--line);font-size:15px}'
       '.res .big{font:800 24px var(--fd);display:block;margin:6px 0}.hint{font-size:14px;color:var(--muted)}.yes{color:#0a7a55;font-weight:800}.no{color:#b42318;font-weight:800}</style>')

# shared lookup: zip -> state file -> rows
CORE = ('var Z3=' + Z3 + ';var TL={10:"DSL",40:"Cable",50:"Fiber",60:"Satellite",61:"Satellite",70:"Fixed wireless / 5G home",71:"Fixed wireless / 5G home",72:"Fixed wireless / 5G home"};'
        'function sp(m){return m>=1000?(m/1000).toFixed(m%1000?1:0)+" Gbps":m+" Mbps"}'
        'function look(z,cb){var st=Z3[z.slice(0,3)];if(!st){cb("We do not have data for that ZIP code.");return}'
        'fetch("/data/"+st+".json").then(function(r){return r.json()}).then(function(d){var e=d.z[z];if(!e){cb("We do not have FCC data for "+z+". Call (888) 491-5666 and we will check your address.");return}'
        'var rows=e.p.map(function(p){return {n:d.b[p[0]],t:p[1],tl:TL[p[1]]||"Other",dn:p[2],up:p[3],cov:p[4]}});cb(null,{st:st,city:e.c,rows:rows,asof:d.asof})}).catch(function(){cb("Could not load data. Please try again.")})}'
        'function $(i){return document.getElementById(i)}'
        'function tbl(rs){return "<table><tr><th>Provider</th><th>Type</th><th>Top download</th><th>Upload</th><th>ZIP covered</th></tr>"+rs.map(function(r){return "<tr><td><b>"+r.n+"</b></td><td>"+r.tl+"</td><td>"+sp(r.dn)+"</td><td>"+sp(r.up)+"</td><td>"+(r.t==60||r.t==61?"Almost everywhere":r.cov+"%")+"</td></tr>"}).join("")+"</table>"}'
        'var CALL=" <a href=\\"tel:+18884915666\\">Call (888) 491-5666</a> and a specialist will confirm your exact address.";')

def form(btn):
    return (f'<div class="tool"><label for="zz"><b>Your ZIP code</b></label><br><input id="zz" inputmode="numeric" maxlength="5" placeholder="e.g. 75201" autocomplete="postal-code"> '
            f'<button class="btn" id="go" type="button">{esc(btn)}</button><div class="res" id="out"></div></div>')

def wrap(render):
    return ('<script>(function(){' + CORE + 'function run(){var z=$("zz").value.trim(),o=$("out");if(!/^\\d{5}$/.test(z)){o.innerHTML="Enter a 5-digit ZIP code.";return}o.innerHTML="Checking...";'
            'look(z,function(err,d){if(err){o.innerHTML=err;return}o.innerHTML=(' + render + ')(z,d)+"<p class=hint>FCC Broadband Data Collection, as of "+d.asof+". What providers report for the ZIP code, not a guarantee for your address.</p>"})}'
            '$("go").onclick=run;$("zz").onkeydown=function(e){if(e.key==="Enter")run()};var q=new URLSearchParams(location.search).get("zip");if(q){$("zz").value=q;run()}})()</script>')

def cta(msg):
    return ('<div class="cta"><div><h3>' + esc(msg) + '</h3><p>A specialist can confirm what is available at your exact address and help you order. Call ' + PHONE + '.</p></div>'
            '<a class="btn alt" href="tel:+18884915666">Call (888) 491-5666</a></div>')

def src(items):
    return "<h2>Sources</h2><ul>" + "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{esc(t)}</a></li>' for t, u in items) + "</ul>"

def page(save, path, title, desc, h1, lead, body, faq, script, name):
    ld = [{"@type": "WebApplication", "name": name, "url": SITE + path, "description": desc, "applicationCategory": "UtilitiesApplication",
           "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "isAccessibleForFree": True}]
    save(path, ui.shell(path, title, desc, h1, lead, CSS + author.box(CHECKED) + body + src([FCC_BDC, FCC_MAP]), faq,
                        [("Home", SITE + "/"), ("Tools", SITE + "/tools"), (name, SITE + path)], ["Free tool", "FCC data"],
                        jsonld_extra=ld, date=DATE, script=script, checked=CHECKED, author=author.PERSON))

FINDERS = [
    ("/tools/fiber-checker", "Fiber internet checker", "Find out if fiber internet is available in your ZIP code."),
    ("/tools/internet-availability-checker", "Internet availability checker", "Every provider that reports service in your ZIP code."),
    ("/tools/rural-internet-finder", "Rural internet finder", "Best options where cable and fiber do not reach."),
    ("/tools/compare-providers", "Compare two providers", "Side-by-side speeds and coverage at your ZIP code."),
    ("/tools/business-internet-finder", "Business internet finder", "Providers that can serve a business at your ZIP code."),
]

def build(save):
    # 1 fiber
    r = ('function(z,d){var f=d.rows.filter(function(r){return r.t==50}).sort(function(a,b){return b.cov-a.cov||b.dn-a.dn});'
         'if(!f.length){var c=d.rows.filter(function(r){return r.t==40});return "<span class=\\"big no\\">No fiber reported in "+z+"</span>"+(c.length?"Your fastest wired option is cable: "+c.map(function(r){return r.n+" up to "+sp(r.dn)}).join(", ")+".":"See the <a href=\\"/tools/rural-internet-finder?zip="+z+"\\">rural internet finder</a> for other options.")+CALL}'
         'return "<span class=\\"big yes\\">Fiber is reported in "+z+(d.city?" ("+d.city+")":"")+"</span>"+tbl(f)+"<p>Coverage is the share of the ZIP code each provider reports reaching, so fiber may reach some streets and not others."+CALL+"</p>"}')
    page(save, "/tools/fiber-checker", "Is Fiber Internet Available at My Address? Free Fiber Checker by ZIP",
         "Check if fiber internet is available in your ZIP code: fiber providers, top speeds and how much of the ZIP code they cover, from FCC data.",
         "Is fiber available in my area?", "Check fiber providers, speeds and coverage by ZIP code.",
         form("Check for fiber") + '<h2>Why fiber is worth checking</h2><p>Fiber usually offers the fastest speeds and upload speeds as fast as downloads, which helps video calls, working from home and backups. '
         'Read <a href="/guides/fiber-vs-cable-internet">fiber vs cable</a>.</p>' + cta("Fiber listed in your ZIP? Confirm your street"),
         [("How do I know if fiber is available at my address?", "This tool shows fiber providers reported in your ZIP code and how much of it they cover. Fiber can reach one street and not the next, so call us or the provider to confirm your exact address."),
          ("Is fiber better than cable?", "Fiber usually has much faster upload speeds and is often more reliable at busy times. Cable can be just as fast for downloads.")], wrap(r), "Fiber internet checker")
    # 2 availability
    r = ('function(z,d){var rs=d.rows.slice().sort(function(a,b){return (a.t>=60&&a.t<=61)-(b.t>=60&&b.t<=61)||b.cov-a.cov||b.dn-a.dn});'
         'return "<span class=\\"big\\">"+rs.length+" providers report service in "+z+(d.city?" ("+d.city+")":"")+"</span>"+tbl(rs)+"<p><a href=\\"/internet/"+z+"\\">See plans and starting prices for "+z+"</a>."+CALL+"</p>"}')
    page(save, "/tools/internet-availability-checker", "Internet Availability Checker: What Internet Can I Get at My Address?",
         "Free internet availability checker. Enter your ZIP code to see every provider that reports service, with connection type, top speeds and coverage, from FCC data.",
         "What internet can I get at my address?", "See every provider that reports service in your ZIP code.",
         form("Check availability") + '<h2>Need your exact address checked?</h2><p>The FCC National Broadband Map lets you search a single address. Our table covers the whole ZIP code; '
         'a specialist can confirm your address by phone.</p>' + cta("Want your exact address checked?"),
         [("How do I find internet providers for my address?", "Enter your ZIP code here to see providers that report service, then confirm your exact address with us by phone or on the FCC National Broadband Map."),
          ("Why does a provider show partial coverage?", "Providers report service by location. A coverage figure under 100% means they reach part of the ZIP code.")], wrap(r), "Internet availability checker")
    # 3 rural
    r = ('function(z,d){var wired=d.rows.filter(function(r){return (r.t==50||r.t==40||r.t==10)&&r.cov>=50}),alt=d.rows.filter(function(r){return r.t>=60}).sort(function(a,b){return b.dn-a.dn});'
         'var h=wired.length?"<p>Good news: wired service reaches most of "+z+": "+wired.map(function(r){return r.n+" ("+r.tl+")"}).join(", ")+". Wired is usually the best choice where it reaches you.</p>":"<p>Cable and fiber reach little or none of "+z+", so these are your main options:</p>";'
         'return "<span class=\\"big\\">Rural options in "+z+(d.city?" ("+d.city+")":"")+"</span>"+h+tbl(alt)+"<p><b>Tips:</b> 5G home and fixed wireless need good signal at your home, so ask for a check before you order. Satellite works almost anywhere; low-orbit satellite (Starlink) usually has much lower lag than older satellite."+CALL+"</p>"}')
    page(save, "/tools/rural-internet-finder", "Rural Internet Finder: Best Internet Where Cable and Fiber Don't Reach",
         "Find rural internet options by ZIP code: 5G home internet, fixed wireless and satellite providers with top speeds, from FCC data.",
         "Rural internet finder", "Best options when cable and fiber do not reach your home.",
         form("Find rural options") + '<h2>Rural internet options explained</h2><p><b>5G home internet</b> uses a cell network and works where the signal is strong. <b>Fixed wireless</b> beams service from a local tower. '
         '<b>Satellite</b> works almost anywhere; read our <a href="/guides/satellite-internet-guide">satellite internet guide</a>. <b>DSL</b> uses phone lines and is often slow but steady.</p>' + cta("Not sure which rural option fits? We can check"),
         [("What is the best internet for rural areas?", "Fiber or cable if they reach you. If not, 5G home or fixed wireless where the signal is good, then satellite. Starlink usually beats older satellite on speed and lag."),
          ("Can I get internet with no cable lines?", "Yes. 5G home, fixed wireless and satellite need no cable lines.")], wrap(r), "Rural internet finder")
    # 4 compare
    r = ('function(z,d){var rs=d.rows;var opts=rs.map(function(r,i){return "<option value="+i+">"+r.n+" ("+r.tl+")</option>"}).join("");'
         'setTimeout(function(){var a=$("pa"),b=$("pb");if(!a)return;b.selectedIndex=Math.min(1,rs.length-1);function c(){var x=rs[a.value],y=rs[b.value];'
         'function w(p,q,v){return p>q?" class=yes":p<q?" class=no":""}$("cmp").innerHTML="<table><tr><th></th><th>"+x.n+"</th><th>"+y.n+"</th></tr><tr><td>Type</td><td>"+x.tl+"</td><td>"+y.tl+"</td></tr><tr><td>Top download</td><td"+w(x.dn,y.dn)+">"+sp(x.dn)+"</td><td"+w(y.dn,x.dn)+">"+sp(y.dn)+"</td></tr><tr><td>Top upload</td><td"+w(x.up,y.up)+">"+sp(x.up)+"</td><td"+w(y.up,x.up)+">"+sp(y.up)+"</td></tr><tr><td>ZIP covered</td><td>"+x.cov+"%</td><td>"+y.cov+"%</td></tr></table>"}a.onchange=c;b.onchange=c;c()},0);'
         'return "<span class=\\"big\\">Compare providers in "+z+"</span><p><select id=pa>"+opts+"</select> vs <select id=pb>"+opts+"</select></p><div id=cmp></div><p>Prices depend on your address and current offers."+CALL+"</p>"}')
    page(save, "/tools/compare-providers", "Compare Internet Providers at Your ZIP Code: Side-by-Side Tool",
         "Pick two internet providers available in your ZIP code and compare connection type, top download and upload speeds and coverage side by side.",
         "Compare two internet providers", "Side-by-side speeds and coverage for providers in your ZIP code.",
         form("Show providers") + '<p>Popular comparisons: <a href="/compare/xfinity-vs-spectrum">Xfinity vs Spectrum</a> · <a href="/compare/att-vs-xfinity">AT&amp;T vs Xfinity</a> · <a href="/compare/t-mobile-vs-verizon">T-Mobile vs Verizon</a> · <a href="/compare">all comparisons</a></p>'
         + cta("Want help choosing? Talk to a specialist"),
         [("How do I compare internet providers?", "Compare connection type, upload and download speed, coverage at your address, the price after any promotion, and fees. This tool covers the first three; we can quote prices by phone.")], wrap(r), "Compare two providers")
    # 5 business
    r = ('function(z,d){var rs=d.rows.filter(function(r){return r.t<60}).sort(function(a,b){return (b.t==50)-(a.t==50)||b.up-a.up});'
         'return "<span class=\\"big\\">Business internet options in "+z+(d.city?" ("+d.city+")":"")+"</span>"+tbl(rs)+"<p>Businesses usually want fiber or cable with strong upload speeds, a static IP option and a service guarantee. Business plans and prices differ from home plans."+CALL+"</p>"}')
    page(save, "/tools/business-internet-finder", "Business Internet Finder: Providers for Your Business by ZIP Code",
         "Find business internet providers by ZIP code: fiber, cable and wireless options with top upload and download speeds, then get a business quote.",
         "Business internet finder", "Providers that can serve a business at your ZIP code.",
         form("Find business options") + '<h2>What to ask for a business line</h2><ul><li>Upload speed for video calls, cloud backups and cameras</li><li>Static IP address, if you host anything</li>'
         '<li>Service level agreement and repair times</li><li>Backup connection (5G or a second provider) if downtime costs you money</li><li>Contract length and early termination fees</li></ul>' + cta("Get a business internet quote"),
         [("What is the best internet for a small business?", "Fiber where available, for its upload speed and reliability. Cable is a strong second. Many businesses add a 5G backup line."),
          ("Is business internet different from home internet?", "Usually yes: business plans often include static IPs, faster repair commitments and different pricing and contracts.")], wrap(r), "Business internet finder")
