/* ---------- outage reports (inserted before `async function __pg(` in the site Worker) ----------
   GET  /api/outage?p=<provider>      -> last 24 hourly report counts, problem types, top ZIP3 areas (edge-cached 60s)
   POST /api/outage {p,zip,type,token} -> verifies Turnstile, 1 report per provider per hour per visitor, stores counts only.
   Stored: provider, hour bucket, problem type, first 3 digits of ZIP. Not stored: IP, full ZIP, anything else.
   The visitor's IP is hashed with a secret only to rate-limit, kept 1 hour, then expires. */
const OUT_P={"xfinity":"Xfinity","spectrum":"Spectrum","att":"AT&T","verizon":"Verizon","cox":"Cox","t-mobile":"T-Mobile Home Internet","frontier":"Frontier","centurylink":"CenturyLink","optimum":"Optimum","starlink":"Starlink"};
const OUT_T=["no-internet","slow","drops","wifi","tv","phone","billing-login"];
const OUT_J=(o,s,c)=>new Response(JSON.stringify(o),{status:s||200,headers:{"content-type":"application/json","cache-control":c||"no-store"}});
function __hourKey(p,t){const d=new Date(t);return "out:"+p+":"+d.toISOString().slice(0,13).replace(/[-T]/g,"")}
async function __outage(req,env,u){
  const p=(u.searchParams.get("p")||"").toLowerCase();
  if(req.method==="GET"){
    if(!OUT_P[p])return OUT_J({error:"unknown provider"},400);
    const cache=caches.default,ck=new Request("https://yourbillcheck.com/api/outage?p="+p);
    const hit=await cache.match(ck);if(hit)return hit;
    const now=Date.now(),keys=[];for(let i=23;i>=0;i--)keys.push(__hourKey(p,now-i*36e5));
    const vals=await Promise.all(keys.map(k=>env.SITE.get(k,"json").catch(()=>null)));
    const hours=vals.map(v=>v?v.n:0),types={},zips={};
    vals.forEach(v=>{if(!v)return;for(const k in v.t)types[k]=(types[k]||0)+v.t[k];for(const z in v.z)zips[z]=(zips[z]||0)+v.z[z]});
    const recent=hours[22]+hours[23],avg=hours.slice(0,22).reduce((a,b)=>a+b,0)/22;
    const status=recent>=Math.max(6,avg*6)?"elevated":"normal";
    const top=Object.entries(zips).sort((a,b)=>b[1]-a[1]).slice(0,5).map(e=>({zip3:e[0],n:e[1]}));
    const res=OUT_J({p,name:OUT_P[p],hours,total24:hours.reduce((a,b)=>a+b,0),lastHour:hours[23],status,types,top,generated:new Date(now).toISOString()},200,"public, max-age=60");
    await cache.put(ck,res.clone());return res;
  }
  if(req.method==="POST"){
    let b={};try{b=await req.json()}catch(e){return OUT_J({error:"bad request"},400)}
    const bp=String(b.p||"").toLowerCase(),type=String(b.type||""),zip=String(b.zip||"");
    if(!OUT_P[bp]||OUT_T.indexOf(type)<0||!/^\d{5}$/.test(zip))return OUT_J({error:"missing fields"},400);
    if(!env.TURNSTILE_SECRET)return OUT_J({error:"reports paused"},503);
    const ip=req.headers.get("cf-connecting-ip")||"";
    const fd=new FormData();fd.append("secret",env.TURNSTILE_SECRET);fd.append("response",String(b.token||""));if(ip)fd.append("remoteip",ip);
    const v=await (await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify",{method:"POST",body:fd})).json().catch(()=>({success:false}));
    if(!v.success)return OUT_J({error:"verification failed, please try again"},403);
    const h=[...new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(env.TURNSTILE_SECRET+"|"+ip+"|"+bp)))].slice(0,12).map(x=>x.toString(16).padStart(2,"0")).join("");
    if(await env.SITE.get("rl:"+h))return OUT_J({ok:true,dup:true});
    await env.SITE.put("rl:"+h,"1",{expirationTtl:3600});
    const k=__hourKey(bp,Date.now()),cur=(await env.SITE.get(k,"json"))||{n:0,t:{},z:{}};
    cur.n++;cur.t[type]=(cur.t[type]||0)+1;const z3=zip.slice(0,3);cur.z[z3]=(cur.z[z3]||0)+1;
    await env.SITE.put(k,JSON.stringify(cur),{expirationTtl:172800});
    await caches.default.delete(new Request("https://yourbillcheck.com/api/outage?p="+bp));
    return OUT_J({ok:true});
  }
  return OUT_J({error:"method"},405);
}
