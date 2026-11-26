// gsc-api: private Cloudflare Worker giving read access to Google Search Console for yourbillcheck.com.
// Deployed as Worker "gsc-api" (workers.dev). Secrets (never in this repo): GSC_CLIENT_ID, GSC_CLIENT_SECRET,
// GSC_REFRESH_TOKEN, API_KEY. Auth: pass ?k=<API_KEY> or header x-key.
// One-time connect: visit /auth?k=<API_KEY>, approve, store the shown token as GSC_REFRESH_TOKEN.
const SITE_URL="sc-domain:yourbillcheck.com";
const REDIRECT="https://gsc-api.khalid-shaikh.workers.dev/callback";
const SCOPE="https://www.googleapis.com/auth/webmasters";
const J=(o,s)=>new Response(JSON.stringify(o,null,2),{status:s||200,headers:{"content-type":"application/json"}});
function okKey(req,url,env){
  const k=req.headers.get("x-key")||url.searchParams.get("k")||"";
  if(!env.API_KEY||k.length!==env.API_KEY.length)return false;
  let d=0;for(let i=0;i<k.length;i++)d|=k.charCodeAt(i)^env.API_KEY.charCodeAt(i);
  return d===0;
}
async function token(env){
  const r=await fetch("https://oauth2.googleapis.com/token",{method:"POST",headers:{"content-type":"application/x-www-form-urlencoded"},body:new URLSearchParams({client_id:env.GSC_CLIENT_ID,client_secret:env.GSC_CLIENT_SECRET,refresh_token:env.GSC_REFRESH_TOKEN,grant_type:"refresh_token"})});
  const j=await r.json();if(!j.access_token)throw new Error("token: "+JSON.stringify(j));return j.access_token;
}
async function g(env,url,opt){
  const t=await token(env);
  const r=await fetch(url,Object.assign({},opt||{},{headers:Object.assign({authorization:"Bearer "+t,"content-type":"application/json"},(opt&&opt.headers)||{})}));
  const x=await r.text();let j;try{j=JSON.parse(x)}catch(e){j={raw:x}}
  return J(j,r.status);
}
// Daily snapshot for the SEO agents: writes Search Console data to KV (binding SITE) so cloud jobs can read it
// through the Cloudflare API without a browser. Sites list: KV key "gsc:sites" (JSON array of GSC property ids).
async function sq(env,site,body){const t=await token(env);const r=await fetch("https://www.googleapis.com/webmasters/v3/sites/"+encodeURIComponent(site)+"/searchAnalytics/query",{method:"POST",headers:{authorization:"Bearer "+t,"content-type":"application/json"},body:JSON.stringify(Object.assign({dataState:"all"},body))});return (await r.json()).rows||[]}
async function snapshot(env){
  let sites=[SITE_URL];try{const x=await env.SITE.get("gsc:sites");if(x)sites=JSON.parse(x)}catch(e){}
  const end=new Date(Date.now()-864e5),f=d=>d.toISOString().slice(0,10),back=n=>f(new Date(end.getTime()-n*864e5)),out={};
  for(const site of sites){
    const d={site,generated:new Date().toISOString(),range28:[back(28),f(end)],
      query_page_28:await sq(env,site,{startDate:back(28),endDate:f(end),dimensions:["query","page"],rowLimit:5000}),
      page_28:await sq(env,site,{startDate:back(28),endDate:f(end),dimensions:["page"],rowLimit:5000}),
      query_7:await sq(env,site,{startDate:back(7),endDate:f(end),dimensions:["query"],rowLimit:2000}),
      daily_28:await sq(env,site,{startDate:back(28),endDate:f(end),dimensions:["date"],rowLimit:100}),
      device_28:await sq(env,site,{startDate:back(28),endDate:f(end),dimensions:["device"],rowLimit:10}),
      country_28:await sq(env,site,{startDate:back(28),endDate:f(end),dimensions:["country"],rowLimit:50}),
      data_state:"all (includes fresh, not-yet-final data, same as the Search Console report)"};
    const key=site.replace(/^sc-domain:/,"").replace(/^https?:\/\//,"").replace(/\/$/,"");
    const j=JSON.stringify(d);await env.SITE.put("gsc:"+key+":latest",j);await env.SITE.put("gsc:"+key+":"+f(new Date()),j,{expirationTtl:120*864e5/1000});
    out[key]=d.query_page_28.length;
  }
  return out;
}
// Daily discovery push (no browser): resubmit sitemaps to Google via the Search Console API, and send
// new URLs (not sent before) to IndexNow (Bing, Yahoo, Yandex, Seznam...). Key file served by the site worker.
const INDEXNOW_KEY="e27e938bdeef37a44f985b08b6a67619";
async function ping(env){
  const out={sitemaps:[],indexnow:0};const t=await token(env);
  for(const sm of["https://yourbillcheck.com/sitemap.xml","https://yourbillcheck.com/sitemap-pages.xml"]){
    const r=await fetch("https://www.googleapis.com/webmasters/v3/sites/"+encodeURIComponent(SITE_URL)+"/sitemaps/"+encodeURIComponent(sm),{method:"PUT",headers:{authorization:"Bearer "+t}});out.sitemaps.push(sm+" "+r.status)}
  try{
    const m=await (await fetch("https://raw.githubusercontent.com/KhalidShaikh-lgtm/FCC/main/site/pages/manifest.json?t="+Date.now())).json();
    const sent=new Set(JSON.parse((await env.SITE.get("indexnow:sent"))||"[]"));
    // newest-first, small daily batch straight to Bing (the shared endpoint answered 429 to one big batch)
    const pri=x=>/^\/(tools|outages|bills|fees|guides|save)/.test(x)?0:1;
    const fresh=m.filter(x=>!sent.has(x)).sort((x,y)=>pri(x)-pri(y)).slice(0,200);
    out.indexnow_pending=m.filter(x=>!sent.has(x)).length;
    if(fresh.length){const r=await fetch("https://www.bing.com/indexnow",{method:"POST",headers:{"content-type":"application/json; charset=utf-8"},body:JSON.stringify({host:"yourbillcheck.com",key:INDEXNOW_KEY,keyLocation:"https://yourbillcheck.com/"+INDEXNOW_KEY+".txt",urlList:fresh.map(x=>"https://yourbillcheck.com"+x)})});
      out.indexnow_status=r.status;if(r.status>=300)out.indexnow_reply=(await r.text()).slice(0,300);
      if(r.status<300){fresh.forEach(x=>sent.add(x));await env.SITE.put("indexnow:sent",JSON.stringify([...sent]));out.indexnow=fresh.length}}
  }catch(e){out.indexnow_error=String(e)}
  await env.SITE.put("ping:last",JSON.stringify(Object.assign({at:new Date().toISOString()},out)));
  return out;
}
export default {
  async scheduled(ev,env,ctx){ctx.waitUntil(Promise.all([snapshot(env),ping(env)]))},
  async fetch(req,env){
    const u=new URL(req.url),p=u.pathname;
    if(p==="/")return new Response("gsc-api ok",{status:200});
    if(!okKey(req,u,env)&&p!=="/callback")return J({error:"unauthorized"},401);
    if(p==="/auth"){
      if(!env.GSC_CLIENT_ID)return J({error:"GSC_CLIENT_ID secret not set"},500);
      const a=new URL("https://accounts.google.com/o/oauth2/v2/auth");
      a.search=new URLSearchParams({client_id:env.GSC_CLIENT_ID,redirect_uri:REDIRECT,response_type:"code",scope:SCOPE,access_type:"offline",prompt:"consent",state:"gsc"}).toString();
      return Response.redirect(a.toString(),302);
    }
    if(p==="/callback"){
      const code=u.searchParams.get("code");
      if(!code||u.searchParams.get("state")!=="gsc")return new Response("missing code",{status:400});
      if(env.GSC_REFRESH_TOKEN)return new Response("Already connected. Delete the GSC_REFRESH_TOKEN secret to reconnect.",{status:403});
      const r=await fetch("https://oauth2.googleapis.com/token",{method:"POST",headers:{"content-type":"application/x-www-form-urlencoded"},body:new URLSearchParams({code,client_id:env.GSC_CLIENT_ID,client_secret:env.GSC_CLIENT_SECRET,redirect_uri:REDIRECT,grant_type:"authorization_code"})});
      const j=await r.json();
      if(!j.refresh_token)return new Response("No refresh token returned: "+(j.error||"")+" "+(j.error_description||""),{status:400});
      return new Response("<!DOCTYPE html><meta charset=utf-8><body style='font-family:sans-serif;max-width:640px;margin:40px auto'><h2>Connected</h2><p>Copy this value into the Worker secret <b>GSC_REFRESH_TOKEN</b>, then close this page. It is shown only once.</p><textarea rows=4 style='width:100%' onclick='this.select()'>"+j.refresh_token+"</textarea></body>",{headers:{"content-type":"text/html; charset=utf-8","cache-control":"no-store"}});
    }
    if(!env.GSC_REFRESH_TOKEN)return J({error:"not connected yet: visit /auth?k=KEY"},503);
    const enc=encodeURIComponent(SITE_URL);
    if(p==="/api/ping")return J(await ping(env));
    if(p==="/api/snapshot")return J(await snapshot(env));
    if(p==="/api/sites")return g(env,"https://www.googleapis.com/webmasters/v3/sites");
    if(p==="/api/query"){
      const days=Math.min(Number(u.searchParams.get("days")||28),480),dim=u.searchParams.get("dimension")||"query",lim=Math.min(Number(u.searchParams.get("limit")||25),1000);
      const end=new Date(Date.now()-864e5),start=new Date(end.getTime()-days*864e5),f=d=>d.toISOString().slice(0,10);
      return g(env,"https://www.googleapis.com/webmasters/v3/sites/"+enc+"/searchAnalytics/query",{method:"POST",body:JSON.stringify({startDate:f(start),endDate:f(end),dimensions:dim==="none"?[]:[dim],rowLimit:lim,dataState:"all"})});
    }
    if(p==="/api/sitemaps")return g(env,"https://www.googleapis.com/webmasters/v3/sites/"+enc+"/sitemaps");
    if(p==="/api/sitemaps/submit"){
      const s=u.searchParams.get("url");if(!s||s.indexOf("https://yourbillcheck.com/")!==0)return J({error:"url must start with https://yourbillcheck.com/"},400);
      return g(env,"https://www.googleapis.com/webmasters/v3/sites/"+enc+"/sitemaps/"+encodeURIComponent(s),{method:"PUT"});
    }
    if(p==="/api/inspect"){
      const s=u.searchParams.get("url");if(!s||s.indexOf("https://yourbillcheck.com/")!==0)return J({error:"url must start with https://yourbillcheck.com/"},400);
      return g(env,"https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",{method:"POST",body:JSON.stringify({inspectionUrl:s,siteUrl:SITE_URL})});
    }
    return J({error:"not found",routes:["/api/sites","/api/query?days=28&dimension=query|page|country|device|none&limit=25","/api/sitemaps","/api/sitemaps/submit?url=","/api/inspect?url="]},404);
  }
};
