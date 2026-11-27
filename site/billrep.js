/* ---------- reader bill-increase reports (inserted before 'async function __pg(' in the site Worker; route in __pg) ----------
   GET  /api/bill-report?p=<provider>  -> last 3 report-months: count, median/typical increase, top reasons, by month (edge-cached 5 min).
                                          Figures are only shown on the site once a provider has 5+ reports.
   POST /api/bill-report {p,zip,old,new,month,reason,token} -> Turnstile check, 1 report per provider per visitor per day.
   Stored: provider, month of the increase, the increase in whole dollars, old/new bill rounded to $5 bands, reason chosen
   from a fixed list, first 3 digits of ZIP. Not stored: IP, full ZIP, names, free text. IP is hashed only to rate-limit (24h). */
const BR_P={"xfinity":"Xfinity","spectrum":"Spectrum","att":"AT&T","verizon-fios":"Verizon Fios","cox":"Cox","optimum":"Optimum",
 "frontier":"Frontier","centurylink":"CenturyLink","t-mobile":"T-Mobile","t-mobile-home-internet":"T-Mobile Home Internet","starlink":"Starlink",
 "verizon":"Verizon Wireless","att-wireless":"AT&T Wireless","directv":"DirecTV","dish":"DISH","mediacom":"Mediacom","kinetic":"Kinetic",
 "brightspeed":"Brightspeed","sparklight":"Sparklight","astound":"Astound","wow":"WOW!","metronet":"Metronet","google-fiber":"Google Fiber",
 "cricket":"Cricket","metro-by-t-mobile":"Metro by T-Mobile","boost-mobile":"Boost Mobile","visible":"Visible","mint-mobile":"Mint Mobile",
 "xfinity-mobile":"Xfinity Mobile","spectrum-mobile":"Spectrum Mobile","youtube-tv":"YouTube TV","sling-tv":"Sling TV","hulu-live-tv":"Hulu + Live TV"};
const BR_R={"promo-ended":"Promo or price lock ended","price-increase":"Provider raised prices","new-fee":"New or higher fee","equipment":"Equipment charge",
 "lost-discount":"Lost a discount (e.g. AutoPay)","plan-change":"Plan or package changed","tv-fees":"TV / broadcast or sports fee","unknown":"No reason given / don't know"};
const BR_J=(o,s,c)=>new Response(JSON.stringify(o),{status:s||200,headers:{"content-type":"application/json","cache-control":c||"no-store"}});
const __ym=d=>d.toISOString().slice(0,7);
function __q(a,f){if(!a.length)return null;const s=[...a].sort((x,y)=>x-y),i=(s.length-1)*f,lo=Math.floor(i),hi=Math.ceil(i);return Math.round(s[lo]+(s[hi]-s[lo])*(i-lo))}
async function __billrep(req,env,u){
  if(req.method==="GET"){
    const p=(u.searchParams.get("p")||"").toLowerCase();if(!BR_P[p])return BR_J({error:"unknown provider"},400);
    const cache=caches.default,ck=new Request("https://yourbillcheck.com/api/bill-report?p="+p);const hit=await cache.match(ck);if(hit)return hit;
    const now=new Date(),months=[];for(let i=0;i<3;i++){const d=new Date(Date.UTC(now.getUTCFullYear(),now.getUTCMonth()-i,1));months.push(__ym(d))}
    const vals=await Promise.all(months.map(m=>env.SITE.get("br:"+p+":"+m,"json").catch(()=>null)));
    let inc=[],reasons={},by={};vals.forEach((v,i)=>{by[months[i]]=v?v.n:0;if(!v)return;inc=inc.concat(v.d||[]);for(const k in v.r)reasons[k]=(reasons[k]||0)+v.r[k]});
    const n=inc.length,top=Object.entries(reasons).sort((a,b)=>b[1]-a[1]).slice(0,3).map(e=>({reason:BR_R[e[0]]||e[0],n:e[1]}));
    const out={p,name:BR_P[p],n,show:n>=5,months:by,generated:now.toISOString()};
    if(n>=5)Object.assign(out,{median:__q(inc,.5),p25:__q(inc,.25),p75:__q(inc,.75),top});
    const res=BR_J(out,200,"public, max-age=300");await cache.put(ck,res.clone());return res;
  }
  if(req.method==="POST"){
    let b={};try{b=await req.json()}catch(e){return BR_J({error:"bad request"},400)}
    const p=String(b.p||"").toLowerCase(),zip=String(b.zip||""),reason=String(b.reason||""),month=String(b.month||"");
    const o=Number(b.old),nw=Number(b.new);
    if(!BR_P[p]||!BR_R[reason]||!/^\d{5}$/.test(zip)||!/^\d{4}-\d{2}$/.test(month))return BR_J({error:"Please fill in every field."},400);
    if(!(o>=5&&o<=1500&&nw>o&&nw-o<=500))return BR_J({error:"Check the amounts: the new bill should be higher than the old one."},400);
    const now=new Date(),mo=new Date(month+"-01T00:00:00Z"),oldest=new Date(Date.UTC(now.getUTCFullYear(),now.getUTCMonth()-5,1));
    if(isNaN(mo)||mo>now||mo<oldest)return BR_J({error:"Pick a month in the last 6 months."},400);
    if(!env.TURNSTILE_SECRET)return BR_J({error:"Reports are paused."},503);
    const ip=req.headers.get("cf-connecting-ip")||"";
    const fd=new FormData();fd.append("secret",env.TURNSTILE_SECRET);fd.append("response",String(b.token||""));if(ip)fd.append("remoteip",ip);
    const v=await (await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify",{method:"POST",body:fd})).json().catch(()=>({success:false}));
    if(!v.success)return BR_J({error:"Verification failed, please try again."},403);
    const h=[...new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(env.TURNSTILE_SECRET+"|br|"+ip+"|"+p)))].slice(0,12).map(x=>x.toString(16).padStart(2,"0")).join("");
    if(await env.SITE.get("rlb:"+h))return BR_J({ok:true,dup:true});
    await env.SITE.put("rlb:"+h,"1",{expirationTtl:86400});
    const k="br:"+p+":"+month,cur=(await env.SITE.get(k,"json"))||{n:0,d:[],r:{},z:{},b:[]};
    const inc=Math.round(nw-o);cur.n++;if(cur.d.length<1000){cur.d.push(inc);cur.b.push([Math.round(o/5)*5,Math.round(nw/5)*5])}
    cur.r[reason]=(cur.r[reason]||0)+1;const z3=zip.slice(0,3);cur.z[z3]=(cur.z[z3]||0)+1;
    await env.SITE.put(k,JSON.stringify(cur),{expirationTtl:400*86400});
    await caches.default.delete(new Request("https://yourbillcheck.com/api/bill-report?p="+p));
    return BR_J({ok:true,increase:inc});
  }
  return BR_J({error:"method"},405);
}
