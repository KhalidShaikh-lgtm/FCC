/* ====================================================================
   v20 SEO / AEO / GEO layer for the yourbillcheck-site Worker.
   Appended to the existing worker, so it reuses that worker's helpers:
   esc, cn, ST, SITE, MOD, GUIDES, H, provs. No backticks or template
   literals on purpose (the deploy script embeds this file as raw text).
   ==================================================================== */
const UPDATED=MOD;
const OGRAW="https://raw.githubusercontent.com/KhalidShaikh-lgtm/FCC/e350300c0609f3ad2fe7c31e58a04a98e9dfd70e/site/og.png";
const OGIMG=SITE+"/og.png";
const MON=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const fdate=function(s){const a=s.split("-").map(Number);return MON[a[1]-1]+" "+a[2]+", "+a[0]};
const unesc=function(s){return String(s).replace(/&quot;/g,'"').replace(/&lt;/g,"<").replace(/&gt;/g,">").replace(/&amp;/g,"&")};
const ORGLD={"@type":"Organization","@id":SITE+"/#org","name":"YourBillCheck","url":SITE+"/","logo":OGIMG,"founder":{"@type":"Person","name":"Vivek Budhiraja","jobTitle":"Founder","image":SITE+"/team/vivek-budhiraja.jpg","sameAs":["https://www.linkedin.com/in/vivek-budhiraja-47520847"]},"employee":{"@type":"Person","name":"Khalid Shaikh","jobTitle":"Head of Business Development","url":SITE+"/authors/khalid-shaikh"},"telephone":"+1-888-491-5666","contactPoint":{"@type":"ContactPoint","telephone":"+1-888-491-5666","contactType":"customer service","areaServed":"US","availableLanguage":"English"}};
const ldTag=function(j){return '<script type="application/ld+json">'+JSON.stringify(Object.assign({"@context":"https://schema.org"},j)).replace(/</g,"\\u003c")+"</script>"};
const NAVL='<a href="/about">About</a> · <a href="/methodology">How we get our data</a> · <a href="/guides">Guides</a>';
const FOOT='<a href="/">Home</a> · <a href="/internet">Internet by state</a> · <a href="/guides">Guides</a> · <a href="/about">About</a> · <a href="/methodology">Methodology</a> · <a href="/privacy">Privacy</a> · <a href="/terms">Terms</a> · YourBillCheck, 4550 W Buckingham Rd, Garland, TX 75042';
const UPD='Last updated <time datetime="'+UPDATED+'">'+fdate(UPDATED)+"</time>";
const FOOTRE=/(<footer[^>]*>\s*<div class="wrap">)/;
const DARKRE=/@media\(prefers-color-scheme:dark\)\{:root\{[^}]*\}\}\n?/;
const CTA='<div class="cta"><b>Check your bill or compare providers</b><br>Tell us your ZIP and what you pay now.<br><br><a class="btn" href="/#check">Check my bill</a> &nbsp; <a class="btn" style="background:transparent;color:var(--mint);border:2px solid var(--mint)" href="tel:+18884915666">Call (888) 491-5666</a></div>';

/* ---------- shared head tags: Open Graph, Twitter cards ---------- */
function headExtras(url,title,desc,full,type){
  let s="";
  if(full)s+='<meta property="og:title" content="'+esc(title)+'"><meta property="og:description" content="'+esc(desc)+'"><meta property="og:type" content="'+(type||"website")+'">';
  s+='<meta property="og:url" content="'+url+'"><meta property="og:site_name" content="YourBillCheck"><meta property="og:locale" content="en_US"><meta property="og:image" content="'+OGIMG+'"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="YourBillCheck: is your internet, TV or mobile bill too high? Check it in 60 seconds."><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="'+esc(title)+'"><meta name="twitter:description" content="'+esc(desc)+'"><meta name="twitter:image" content="'+OGIMG+'">';
  return s;
}

/* ---------- state / city / ZIP pages (built by shell) ---------- */
const BILLG=[["Xfinity","/bills/xfinity-bill-went-up","Xfinity"],["Spectrum","/bills/spectrum-bill-went-up","Spectrum"],["AT&T","/bills/att-bill-went-up","AT&amp;T"],["Verizon","/bills/verizon","Verizon"],["Cox","/bills/cox-bill-went-up","Cox"],["Optimum","/bills/optimum","Optimum"],["Frontier","/bills/frontier","Frontier"],["CenturyLink","/bills/centurylink","CenturyLink"],["T-Mobile","/bills/t-mobile","T-Mobile"],["Starlink","/bills/starlink","Starlink"]];
function billLinks(html){const a=html.indexOf('"@type":"ItemList"');if(a<0)return "";const seg=html.slice(a,html.indexOf("</script>",a));const f=BILLG.filter(function(g){return seg.indexOf('"name":"'+g[0]+'"')>-1}).slice(0,6);if(!f.length)return "";return '<p style="font-size:.95rem;margin:0 0 14px"><b>Already have one of these providers?</b> See why bills go up and how to pay less: '+f.map(function(g){return '<a href="'+g[1]+'">'+g[2]+' bill guide</a>'}).join(" \u00b7 ")+' \u00b7 <a href="/fees">hidden fees explained</a></p>'}
function decorate(html,o){
  html=html.replace(/<section class="xr"[\s\S]*?<\/section>\s*<section class="xr-facts"[\s\S]*?<\/section>\s*/,"");
  if(html.indexOf('id="loc-css"')<0)html=html.replace("</head>",'<style id="loc-css">.zh{font-family:var(--font-display)!important;font-weight:800!important;letter-spacing:-.02em;line-height:1.08}.ct{display:inline-block;padding:3px 10px;border-radius:999px;font-size:.82rem;font-weight:700;background:#eef1f4;color:#0f2233;white-space:nowrap}.ct-fiber{background:#dff3ea;color:#076e52}.ct-cable{background:#e4ecfb;color:#1d4ea8}.ct-5g,.ct-fixed{background:#fff1c7;color:#7a5600}.ct-satellite{background:#f1e8fb;color:#5b2d91}.ct-dsl{background:#f0f0f0;color:#444}.cov{display:inline-block;vertical-align:middle;width:60px;height:8px;border-radius:99px;background:#e3e8ee;margin-right:8px;overflow:hidden}.cov i{display:block;height:100%;background:var(--mint,#0a8f6a);border-radius:99px}.seo table tbody tr:hover{background:#f6faf8}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid var(--mint,#0a8f6a);outline-offset:2px}@media (max-width:760px){.seo table{display:block;overflow-x:auto;max-width:100%;-webkit-overflow-scrolling:touch}.cov{width:40px}}</style>'+"</head>");
  if(!/property="og:url"/.test(html))html=html.replace("</head>",headExtras(o.url,o.title,o.desc,false)+"</head>");
  html=html.replace(FOOTRE,'$1<p style="margin:0 0 10px;font-size:.9rem">'+NAVL+"</p>");
  html=html.replace('<section class="seo"><div class="wrap">','<section class="seo"><div class="wrap"><p style="font-size:.88rem;color:var(--muted);margin:0 0 12px">'+UPD+' · Availability: FCC data as of June 30, 2026 · Prices: Nov 2026 · <a href="/methodology">How we get our data</a></p>'+billLinks(html));
  return html;
}

/* ---------- home page (stored in KV as index.html) ---------- */
const HT="Free Internet, TV & Mobile Bill Check | YourBillCheck";
const HD="Upload your internet, TV or mobile bill and see in 60 seconds if you're overpaying. Compare providers, speeds and typical starting prices by ZIP code. Free.";
const HOGT="Is your bill too high? Find out in 60 seconds | YourBillCheck";
const HOGD="Snap your bill. See what you pay a year. Lower it with your provider or switch. Free.";
function homeShell(html){
  html=html.replace(/<title>[^<]*<\/title>/,"<title>"+esc(HT)+"</title>")
   .replace(/<meta name="description" content="[^"]*">/,'<meta name="description" content="'+esc(HD)+'"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">');
  const ld=[ORGLD,
   {"@type":"WebSite","@id":SITE+"/#website","url":SITE+"/","name":"YourBillCheck","inLanguage":"en-US","publisher":{"@id":SITE+"/#org"}},
   {"@type":"WebPage","@id":SITE+"/#page","url":SITE+"/","name":HT,"description":HD,"dateModified":UPDATED,"inLanguage":"en-US","isPartOf":{"@id":SITE+"/#website"},"primaryImageOfPage":{"@type":"ImageObject","url":OGIMG}}];
  html=html.replace("</head>",headExtras(SITE+"/",HOGT,HOGD,false)+ld.map(ldTag).join("")+"</head>");
  return html.replace(FOOTRE,'$1<p style="margin:0 0 10px;font-size:.9rem">'+NAVL+"</p>");
}

/* ---------- extra FAQ answers (all derived from real data or site policy) ---------- */
function siteFaq(withSource){
  const a=[];
  if(withSource)a.push(["Where does YourBillCheck get its availability data?","From the FCC Broadband Data Collection, which is provider-reported coverage as of June 30, 2026, matched to ZIP codes. It shows what providers report across a ZIP code, not a guarantee for your exact address, so we confirm your address with you before you order."]);
  a.push(["Are the prices shown what I will pay?","Not exactly. Prices are typical advertised new-customer starting prices from November 2026. They often need AutoPay, exclude taxes, fees and equipment, and promotional prices can rise after the first year or two. We confirm the current offer for your address."]);
  a.push(["Does it cost anything to use YourBillCheck?","No. The comparison and bill check are free. We may earn a commission from providers when you sign up through us, at no cost to you and without changing your price."]);
  return a;
}
const zc=function(n){return n+" ZIP code"+(n==1?"":"s")};
const TL={10:"DSL",40:"cable",50:"fiber",60:"satellite",61:"satellite"};
function stateExtra(d,nz){
  const S=ST[d.code],tz={},fp={};let fz=0;
  Object.keys(d.z).forEach(function(zz){
    const p=d.z[zz].p;if(!p.length)return;
    const seen={},fs={};
    p.forEach(function(r){const l=TL[r[1]]||"fixed wireless and 5G home";seen[l]=1;if(r[1]==50)fs[cn(d.b[r[0]])]=1});
    Object.keys(seen).forEach(function(l){tz[l]=(tz[l]||0)+1});
    const fk=Object.keys(fs);if(fk.length){fz++;fk.forEach(function(b){fp[b]=(fp[b]||0)+1})}
  });
  const types=Object.keys(tz).sort(function(a,b){return tz[b]-tz[a]}).map(function(l){return l+" in "+zc(tz[l])});
  const tf=Object.keys(fp).sort(function(a,b){return fp[b]-fp[a]}).slice(0,5);
  const out=[["What types of home internet are available in "+S+"?","Providers report "+types.join(", ")+", out of "+zc(nz)+" with provider data in "+S+". The types you can get depend on your street, so enter your ZIP code to see your options."],
   ["Is fiber internet available in "+S+"?",fz?"Yes, in parts of "+S+". Providers report fiber in "+fz+" of "+zc(nz)+". "+(tf.length>1?"The providers reporting fiber in the most ZIP codes are ":"The provider reporting fiber is ")+tf.join(", ")+". Fiber is offered only in some neighborhoods, so check your ZIP code and your address.":"No provider reports fiber in the latest FCC data for "+S+". Cable, 5G home internet, fixed wireless and satellite may be available."]];
  return out.concat(siteFaq(true));
}
function cityExtra(faq,d,c,PL,S){
  const rows=c.zips.map(function(z){return [z,provs(d,z,PL).filter(function(x){return !x.sat}).length]}).filter(function(r){return r[1]>0}).sort(function(a,b){return b[1]-a[1]||(a[0]<b[0]?-1:1)}).slice(0,3);
  if(c.zips.length>1&&rows.length)faq.push(["Which ZIP codes in "+c.name+", "+S+" have the most internet providers?",rows.map(function(r){return r[0]+" ("+r[1]+" provider"+(r[1]==1?"":"s")+")"}).join(", ")+" report the most non-satellite providers. Counts vary by ZIP code, so enter yours to see your options."]);
  siteFaq(true).forEach(function(f){faq.push(f)});
}

/* ---------- trust pages: About, Methodology, Guides hub, state hub ---------- */
const METH=[
["Where availability comes from","Provider availability comes from the FCC Broadband Data Collection, the data behind the FCC National Broadband Map. Internet providers report where they offer service and the FCC publishes it. Our tables use the data as of June 30, 2026, matched to ZIP codes, so each page shows which providers report service in or around that ZIP code."],
["What the numbers mean","Top speed is the fastest download speed a provider reports in the area. Coverage is an estimate of how much of the ZIP code the provider reports covering, and satellite is shown as available almost everywhere. Connection type (fiber, cable, DSL, 5G home internet, fixed wireless or satellite) comes from the technology the provider reports."],
["How we order providers","Wired and fixed wireless options are listed before satellite. Within those, we order by connection type (fiber, then cable, then fixed wireless and 5G home internet, then DSL), then by reported coverage, then by starting price. Commissions do not affect the order."],
["Where prices come from","Starting prices are typical advertised new-customer prices from providers' public pages, as of November 2026. They often need AutoPay and exclude taxes, fees and equipment, and promotional prices can rise after the first year or two. We show the lowest-priced plan we track for each provider, so your price can differ."],
["How savings are estimated","Estimated yearly savings are your current monthly bill minus a provider's starting price, multiplied by 12. They are illustrations, not promises."],
["How the bill check works","If you upload a bill, we use it only to read the provider, services and monthly total. Please hide or crop account numbers before uploading. We never ask for your provider login or password."],
["What this data cannot tell you","Availability here is by ZIP code, not by street address, and it can differ from one street to the next. Before you order, we confirm availability and the current offer for your exact address."],
["How we make money","YourBillCheck is free to use. We may earn a commission from providers when you sign up through us, at no cost to you and without changing your price. We are not affiliated with, endorsed by or sponsored by any provider."],
["How often we update","We rebuild our ZIP tables when the FCC publishes a new data release. The data dates are shown on every page, along with the date the page was last updated."],
["Corrections","If something on the site looks wrong, call (888) 491-5666 and we will review it."]
];
const ABOUT=[
["Who runs YourBillCheck","<div style=\"display:flex;gap:14px;align-items:center;border:1px solid #e3e8ee;border-radius:14px;padding:14px 16px;margin:10px 0;max-width:560px;background:#fff\"><img src=\"/team/vivek-budhiraja.jpg\" width=\"64\" height=\"64\" alt=\"Vivek Budhiraja\" style=\"border-radius:50%;object-fit:cover;flex:none\"><div><b>Vivek Budhiraja</b><br><span>Founder</span><br><a href=\"https://www.linkedin.com/in/vivek-budhiraja-47520847\" rel=\"noopener me\" target=\"_blank\">LinkedIn</a></div></div><div style=\"display:flex;gap:14px;align-items:center;border:1px solid #e3e8ee;border-radius:14px;padding:14px 16px;margin:10px 0;max-width:560px;background:#fff\"><span aria-hidden=\"true\" style=\"width:64px;height:64px;border-radius:50%;flex:none;display:grid;place-items:center;background:var(--mint,#0a8f6a);color:#fff;font-weight:800;font-size:22px\">KS</span><div><b><a href=\"/authors/khalid-shaikh\">Khalid Shaikh</a></b><br><span>Head of Business Development</span><br><a href=\"https://www.linkedin.com/in/khalid-shaikh-73826627/\" rel=\"noopener me\" target=\"_blank\">LinkedIn</a></div></div>"],
["Who we are","YourBillCheck is an independent comparison and sales service for people in the United States. We help households check whether their internet, TV or mobile bill is too high and compare internet providers by ZIP code. We are based at 4550 W Buckingham Rd, Garland, TX 75042."],
["What you can do here","Upload your bill, or enter your provider and monthly total, and see what you pay in a year and how much you could save. Browse internet providers by <a href=\"/internet\">state</a>, city and ZIP code, with top speeds, coverage and typical starting prices. If you want help, a specialist can confirm what is available at your exact address and help you sign up."],
["How we make money","YourBillCheck is free to use. We may earn a commission from providers when you sign up through us, at no cost to you and without changing your price."],
["Where our data comes from","Availability comes from FCC data and prices come from provider offers. Read <a href=\"/methodology\">how we get our data</a> for the details and the limits."],
["Independence","We are not affiliated with, endorsed by or sponsored by any provider. Provider names are trademarks of their owners and are used only to identify services. Providers are listed in the order explained on our methodology page, not by who pays us."],
["Contact","Call (888) 491-5666 or write to YourBillCheck, 4550 W Buckingham Rd, Garland, TX 75042. Read our <a href=\"/privacy\">Privacy Policy</a> and <a href=\"/terms\">Terms of Use</a>."]
];
const GDESC={
"how-to-lower-your-internet-bill":"Practical steps to reduce what you pay for home internet, TV and phone.",
"fiber-vs-cable-internet":"Fiber and cable are the two main wired home internet options. Here is how they differ and how to pick.",
"how-much-internet-speed-do-you-need":"A plain guide to choosing an internet speed for your household without overpaying.",
"internet-for-streaming-and-gaming":"What to look for in a home internet connection if you stream video or play online games.",
"satellite-internet-guide":"Satellite internet can reach places wired providers do not. Here is when it makes sense."
};
const GFAQ={
"fiber-vs-cable-internet":[
 ["Is fiber faster than cable?","Fiber is usually offered with equal download and upload speeds, while cable often has fast downloads but much slower uploads. Top download speeds depend on the plan, so compare the specific plans available at your address."],
 ["Which is better for working from home?","Fiber's matching upload speed helps with video calls and cloud backups. If fiber is not available at your address, cable is a good option for most homes."],
 ["Why does cable internet slow down at busy times?","Cable capacity is shared across a neighborhood, so speeds can vary when many people are online. Fiber tends to hold steadier speeds at busy hours."],
 ["How do I know if fiber is available at my address?","Fiber is offered only in certain neighborhoods. Enter your ZIP code to see which providers report fiber, then confirm your exact address, because availability can differ by street."]],
"how-to-lower-your-internet-bill":[
 ["Why did my internet bill go up?","Promotional prices often expire after 12 to 24 months and then step up to the regular rate. Compare your current monthly total with the price you signed up for."],
 ["Can I save money by using my own modem or router?","Many providers charge a monthly fee for equipment. Using your own compatible equipment can cut that fee, so ask your provider what it supports."],
 ["Should I call my provider or switch?","Call first and ask for current offers, then compare with other providers available at your address. A bill review can show where you are overpaying."],
 ["What should I look for on my bill?","Look at the full monthly total rather than the first-year price, and check for TV packages, equipment rentals and add-ons you do not use."]],
"how-much-internet-speed-do-you-need":[
 ["How much internet speed does a household need?","As a rough guide, light use by one or two people is often fine at 100 to 300 Mbps, a busy household at 300 to 600 Mbps, and heavy use with many devices or large uploads at 1 Gbps or more."],
 ["Does upload speed matter?","Yes. Video calls, backups and posting large files depend on upload speed, so check it and not just the download number."],
 ["Why is my Wi-Fi slower than my plan?","Older routers and Wi-Fi limits can cap what your devices actually receive. A better router can matter more than a higher plan."]],
"internet-for-streaming-and-gaming":[
 ["What internet is best for gaming?","Online games need low latency and a stable connection more than very high speeds. Wired connections, especially fiber and cable, usually beat satellite for latency."],
 ["Is Wi-Fi or Ethernet better for gaming and streaming?","A wired Ethernet connection to your console or PC avoids Wi-Fi interference and often gives the steadiest results."],
 ["How much speed do I need to stream?","One HD or 4K stream uses a modest amount of bandwidth, but several streams at once add up. Plan for the number of screens in use together."]],
"satellite-internet-guide":[
 ["Is satellite internet good for rural areas?","It can reach places wired providers do not, including rural areas where fiber and cable may not reach."],
 ["How does satellite compare with fiber or cable?","Speeds and latency are usually lower and less predictable, and plans, equipment and pricing differ from wired providers."],
 ["Can satellite internet be a backup?","Some households use satellite as a backup if their wired service has outages."]]
};

function simplePage(o){
  const url=SITE+o.path;
  const ld=[ORGLD,{"@type":o.type||"WebPage","@id":url+"#page","url":url,"name":o.title,"description":o.desc,"dateModified":UPDATED,"inLanguage":"en-US","publisher":{"@id":SITE+"/#org"},"isPartOf":{"@id":SITE+"/#website"}},
   {"@type":"BreadcrumbList","itemListElement":o.crumbs.map(function(c,i){return {"@type":"ListItem","position":i+1,"name":c[0],"item":c[1]}})}];
  const bc='<p class="note">'+o.crumbs.map(function(c,i){return i<o.crumbs.length-1?'<a href="'+c[1].replace(SITE,"")+'">'+esc(c[0])+"</a> › ":esc(c[0])}).join("")+"</p>";
  return '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+esc(o.title)+'</title><meta name="description" content="'+esc(o.desc)+'"><link rel="canonical" href="'+url+'"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">'+headExtras(url,o.title,o.desc,true,"website")+'<link rel="stylesheet" href="/s.css">'+ld.map(ldTag).join("")+'</head><body><div class="w"><a class="top" href="/">YourBillCheck</a>'+bc+"<h1>"+esc(o.h1)+'</h1><p class="lead">'+o.lead+'</p><p class="note">'+UPD+' · <a href="/methodology">How we get our data</a></p>'+o.body+(o.cta?CTA:"")+"<footer>"+FOOT+"</footer></div></body></html>";
}
const sections=function(a){return a.map(function(s){return "<h2>"+esc(s[0])+"</h2><p>"+s[1]+"</p>"}).join("")};
function aboutPage(){return simplePage({path:"/about",type:"AboutPage",title:"About YourBillCheck | Independent Bill Check and Internet Comparison",desc:"YourBillCheck is an independent service that helps US households check if their internet, TV or mobile bill is too high and compare internet providers by ZIP code.",h1:"About YourBillCheck",lead:"An independent service that helps you check whether your bill is too high and compare internet providers in your ZIP code.",crumbs:[["Home",SITE+"/"],["About",SITE+"/about"]],body:sections(ABOUT),cta:true})}
function methPage(){return simplePage({path:"/methodology",title:"Methodology: Where Our Internet Data Comes From | YourBillCheck",desc:"How YourBillCheck finds internet availability (FCC data matched to ZIP codes), where prices come from, how savings are estimated and what the limits are.",h1:"How YourBillCheck gets its data",lead:"Where our availability and prices come from, how we order providers, how savings are estimated and what the numbers cannot tell you.",crumbs:[["Home",SITE+"/"],["Methodology",SITE+"/methodology"]],body:sections(METH),cta:true})}
function guidesPage(){return simplePage({path:"/guides",type:"CollectionPage",title:"Internet and Bill Guides | YourBillCheck",desc:"Plain-language guides on lowering your internet bill, fiber vs cable, how much speed you need, streaming and gaming, and satellite internet.",h1:"Internet and bill guides",lead:"Plain-language guides to help you pay less and pick the right internet.",crumbs:[["Home",SITE+"/"],["Guides",SITE+"/guides"]],body:"<ul>"+GUIDES.map(function(g){return '<li><a href="/guides/'+g[0]+'">'+esc(g[1])+"</a> - "+esc(GDESC[g[0]]||"")+"</li>"}).join("")+"</ul>",cta:true})}
function hubPage(){return simplePage({path:"/internet",type:"CollectionPage",title:"Internet Providers by State | Compare Plans by ZIP | YourBillCheck",desc:"Compare internet providers in every US state: fiber, cable, 5G home and satellite by city and ZIP code, with top speeds and typical starting prices.",h1:"Internet providers by state",lead:"Pick your state, then your city or ZIP code, to compare providers, top speeds and typical starting prices.",crumbs:[["Home",SITE+"/"],["Internet by state",SITE+"/internet"]],body:"<ul>"+Object.keys(ST).sort(function(a,b){return ST[a]<ST[b]?-1:1}).map(function(k){return '<li><a href="/internet/'+k+'">'+esc(ST[k])+"</a></li>"}).join("")+"</ul>",cta:true})}

/* ---------- pages served by Cloudflare Pages: guides, privacy, terms ---------- */
function guideTransform(html,slug){
  const f=GFAQ[slug],url=SITE+"/guides/"+slug;
  html=html.replace(/https:\/\/www\.yourbillcheck\.com/g,SITE).replace(/href="\/tx"/g,'href="/internet/tx"');
  const t=unesc((html.match(/<title>([^<]*)<\/title>/)||[])[1]||""),dsc=unesc((html.match(/<meta name="description" content="([^"]*)">/)||[])[1]||""),h1=unesc((html.match(/<h1>([^<]*)<\/h1>/)||[])[1]||t);
  const ld=[ORGLD,{"@type":"Article","@id":url+"#article","headline":h1,"description":dsc,"url":url,"mainEntityOfPage":url,"dateModified":UPDATED,"image":OGIMG,"inLanguage":"en-US","author":{"@id":SITE+"/#org"},"publisher":{"@id":SITE+"/#org"}},
   {"@type":"BreadcrumbList","itemListElement":[["Home",SITE+"/"],["Guides",SITE+"/guides"],[h1,url]].map(function(c,i){return {"@type":"ListItem","position":i+1,"name":c[0],"item":c[1]}})},
   {"@type":"FAQPage","mainEntity":f.map(function(q){return {"@type":"Question","name":q[0],"acceptedAnswer":{"@type":"Answer","text":q[1]}}})}];
  html=html.replace("</head>",headExtras(url,t,dsc,true,"article")+ld.map(ldTag).join("")+"</head>");
  html=html.replace(/(<p class="lead">[\s\S]*?<\/p>)/,'$1<p class="note">'+UPD+' · <a href="/methodology">How we get our data</a></p>');
  const faq="<h2>Common questions</h2>"+f.map(function(q){return "<h3>"+esc(q[0])+"</h3><p>"+esc(q[1])+"</p>"}).join("");
  html=html.replace("<h2>Check what is available at your address</h2>",faq+"<h2>Check what is available at your address</h2>");
  return html.replace(/<footer>[\s\S]*<\/footer>/,"<footer>"+FOOT+"</footer>");
}
function legalTransform(html,p){
  const url=SITE+p,t=unesc((html.match(/<title>([^<]*)<\/title>/)||[])[1]||""),
   d=p==="/privacy"?"What YourBillCheck collects, how we use and share it, and your choices, including call and text consent and how to opt out.":"The terms that apply when you use YourBillCheck to check your bill and compare internet, TV and mobile service.";
  html=html.replace(/https:\/\/www\.yourbillcheck\.com/g,SITE).replace(DARKRE,"");
  let add="";
  if(!/rel="canonical"/.test(html))add+='<link rel="canonical" href="'+url+'">';
  if(!/name="description"/.test(html))add+='<meta name="description" content="'+esc(d)+'">';
  add+=headExtras(url,t,d,true,"website");
  html=html.replace("</head>",add+"</head>");
  return html.replace("<footer>","<footer>"+NAVL+" · ");
}
async function passthrough(req,env){
  const u=new URL(req.url),p=u.pathname.replace(/\/+$/,"")||"/",head=req.method==="HEAD";
  let r;
  if(env&&env.ORIGIN)r=await fetch(env.ORIGIN+u.pathname+u.search,{method:req.method,headers:{"accept":req.headers.get("accept")||"*/*"}});
  else r=await fetch(req);
  if(req.method!=="GET"&&req.method!=="HEAD")return r;
  const ct=r.headers.get("content-type")||"";
  const out=function(t,type){return new Response(head?null:t,{status:200,headers:{"content-type":type,"cache-control":"public, max-age=3600"}})};
  if(p==="/s.css"&&r.ok){if(head)return r;return out((await r.text()).replace(DARKRE,""),"text/css; charset=utf-8")}
  if(ct.indexOf("text/html")<0||r.status!==200)return r;
  const gm=p.match(/^\/guides\/([a-z0-9-]+)$/);
  if(gm&&GFAQ[gm[1]]){if(head)return r;return out(guideTransform(await r.text(),gm[1]),"text/html; charset=utf-8")}
  if(p==="/privacy"||p==="/terms"){if(head)return r;return out(legalTransform(await r.text(),p),"text/html; charset=utf-8")}
  return notFound();
}
function notFound(){
  return new Response('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found | YourBillCheck</title><meta name="robots" content="noindex,follow"><link rel="stylesheet" href="/s.css"></head><body><div class="w"><a class="top" href="/">YourBillCheck</a><h1>Page not found</h1><p>We could not find that page. Enter your ZIP code on the <a href="/">home page</a> or browse <a href="/internet">internet providers by state</a>.</p></div></body></html>',{status:404,headers:{"content-type":"text/html; charset=utf-8","cache-control":"public, max-age=300"}});
}

/* ---------- robots, llms.txt, sitemap ---------- */
const BOTS=["GPTBot","OAI-SearchBot","ChatGPT-User","ClaudeBot","Claude-SearchBot","Claude-User","PerplexityBot","Perplexity-User","Google-Extended","Applebot-Extended","CCBot"];
const ROBOTS2="User-agent: *\nAllow: /\nDisallow: /api/\n\n"+BOTS.map(function(b){return "User-agent: "+b+"\nAllow: /\nDisallow: /api/\n"+(["ClaudeBot","GPTBot","CCBot","PerplexityBot"].indexOf(b)>-1?"Crawl-delay: 5\n":"")}).join("\n")+"\nSitemap: "+SITE+"/sitemap.xml\nSitemap: "+SITE+"/sitemap-us.xml\n";
const LLMS2="# YourBillCheck\n\n> YourBillCheck is a free US comparison service. Enter a ZIP code to see which internet providers report service there, their top speeds, coverage and typical new-customer starting prices, and check whether your internet, TV or mobile bill is too high.\n\nLast updated: "+UPDATED+"\n\n## Key pages\n"+
 "- ["+SITE+"/]("+SITE+"/): ZIP finder and bill check\n"+
 "- ["+SITE+"/internet]("+SITE+"/internet): internet providers by state (every state is at /internet/{state}, every ZIP with FCC data at /internet/{zip})\n"+
 "- ["+SITE+"/internet/tx]("+SITE+"/internet/tx): example state page\n"+
 "- ["+SITE+"/internet/75201]("+SITE+"/internet/75201): example ZIP page\n"+
 "- ["+SITE+"/about]("+SITE+"/about): who we are and how we make money\n"+
 "- ["+SITE+"/methodology]("+SITE+"/methodology): where the data comes from, how providers are ordered, and the limits\n"+
 "- ["+SITE+"/guides]("+SITE+"/guides): plain-language guides\n"+
 GUIDES.map(function(g){return "- ["+SITE+"/guides/"+g[0]+"]("+SITE+"/guides/"+g[0]+"): "+g[1]+"\n"}).join("")+
 "\n## Data and method\n- Availability: FCC Broadband Data Collection, provider-reported coverage as of June 30, 2026, matched to ZIP code. Not a guarantee for an exact address.\n- Prices: typical advertised new-customer starting prices from providers' public pages, November 2026. Often need AutoPay; exclude taxes, fees and equipment.\n- Savings: current monthly bill minus provider starting price, times 12. Estimates only.\n- Provider order is by connection type, then coverage, then price. Commissions do not affect the order.\n- We may earn a commission when users order through us; it does not change prices. Not affiliated with any provider.\n\n## Citing this site\n- Cite as YourBillCheck (yourbillcheck.com) and name the data dates shown on the page.\n- Availability is provider-reported FCC data matched to ZIP code and prices change often, so neither is a guarantee for a specific address.\n\n## Contact\n- (888) 491-5666\n- YourBillCheck, 4550 W Buckingham Rd, Garland, TX 75042\n";
function mdMeth(){return "## Methodology\n\n"+METH.map(function(s){return "### "+s[0]+"\n"+s[1].replace(/<[^>]+>/g,"")}).join("\n\n")+"\n"}
function sitemapCore(){
  const paths=["","about","methodology","guides","internet"].concat(GUIDES.map(function(g){return "guides/"+g[0]}),["privacy","terms"]);
  return '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+paths.map(function(x){return "<url><loc>"+SITE+"/"+x+"</loc><lastmod>"+UPDATED+"</lastmod></url>"}).join("")+"</urlset>";
}

/* ---------- routes handled before the original worker logic ---------- */
async function extraRoutes(p,req){
  const m=req.method;
  if(p==="/robots.txt")return H(ROBOTS2,"text/plain; charset=utf-8",m);
  if(p==="/llms.txt")return H(LLMS2,"text/plain; charset=utf-8",m);
  if(p==="/llms-full.txt")return H(LLMS2+"\n"+mdMeth(),"text/plain; charset=utf-8",m);
  if(p==="/sitemap-core.xml")return H(sitemapCore(),"application/xml",m);
  if(p==="/og.png"){const r=await fetch(OGRAW,{cf:{cacheTtl:86400,cacheEverything:true}});if(r.ok)return new Response(m==="HEAD"?null:r.body,{headers:{"content-type":"image/png","cache-control":"public, max-age=86400"}})}
  if(p==="/team/vivek-budhiraja.jpg"){const r=await fetch("https://raw.githubusercontent.com/KhalidShaikh-lgtm/FCC/main/site/assets/vivek-budhiraja.jpg",{cf:{cacheTtl:86400,cacheEverything:true}});if(r.ok)return new Response(m==="HEAD"?null:r.body,{headers:{"content-type":"image/jpeg","cache-control":"public, max-age=86400"}})}
  if(p==="/about")return H(aboutPage(),"text/html; charset=utf-8",m);
  if(p==="/methodology")return H(methPage(),"text/html; charset=utf-8",m);
  if(p==="/guides")return H(guidesPage(),"text/html; charset=utf-8",m);
  if(p==="/internet")return H(hubPage(),"text/html; charset=utf-8",m);
  return null;
}
