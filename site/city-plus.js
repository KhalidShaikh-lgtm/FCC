/* v42 city-page differentiators: quick picks, local stats vs state, nearby cities (same ZIP3 area), bill-guide links. */
const __BILL={"xfinity":"xfinity","spectrum":"spectrum","at&t":"att","verizon":"verizon","t-mobile":"t-mobile","frontier":"frontier","cox":"cox","cox communications":"cox","optimum":"optimum","centurylink":"centurylink","starlink":"starlink"};
function __zstats(d,zips){let n=0,fib=0,gig=0,wired=0;zips.forEach(z=>{const r=d.z[z];if(!r||!r.p.length)return;n++;const w={};let f=0,g=0;r.p.forEach(p=>{if(p[1]==60||p[1]==61)return;w[p[0]]=1;if(p[1]==50)f=1;if(p[2]>=1000)g=1});fib+=f;gig+=g;wired+=Object.keys(w).length});return {n,fib,gig,wired}}
function __stateStats(d){if(!d.__ss)d.__ss=__zstats(d,Object.keys(d.z));return d.__ss}
function __near(d,cs,c){if(!d.__z3){const m={};Object.entries(d.cities).forEach(([k,v])=>v.zips.forEach(z=>{const p=z.slice(0,3);(m[p]=m[p]||{})[k]=(m[p][k]||0)+1}));d.__z3=m}
 const sc={};c.zips.forEach(z=>{const p=+z.slice(0,3);[[0,100],[-1,1],[1,1],[-2,.01],[2,.01]].forEach(([o,w])=>{const m=d.__z3[String(p+o).padStart(3,"0")]||{};Object.keys(m).forEach(k=>{if(k!==cs)sc[k]=(sc[k]||0)+w*m[k]})})});
 return Object.keys(sc).sort((a,b)=>(sc[b]-sc[a])||(d.cities[b].zips.length-d.cities[a].zips.length)).slice(0,10)}
function __pct(a,b){return b?Math.round(100*a/b):0}
function cityPlus(d,c,cs,L,ok,fast,pc,fib,S){
 try{
 const card=(t,v,s)=>'<div style="flex:1 1 200px;border:1px solid #e3e8ee;border-radius:12px;padding:14px 16px;background:#fff"><div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:#58697a">'+t+'</div><div style="font-size:18px;font-weight:800;margin:4px 0">'+v+'</div><div style="font-size:14px;color:#58697a">'+s+'</div></div>';
 const wide=ok.slice().sort((a,b)=>b.n-a.n)[0];
 let h='<h2>Quick picks in '+esc(c.name)+'</h2><div style="display:flex;flex-wrap:wrap;gap:12px;margin:12px 0 18px">';
 if(fast)h+=card("Fastest",esc(cn(fast.b)),"Up to "+fmt(fast.d)+" reported");
 if(pc)h+=card("Lowest starting price",esc(cn(pc.b)),"From about "+esc(pc.pr.from)+"/mo for new customers");
 if(wide)h+=card("Widest coverage",esc(cn(wide.b)),"Reported in "+wide.n+" of "+c.zips.length+" ZIP code"+(c.zips.length>1?"s":""));
 if(fib.length)h+=card("Fiber option",esc(cn(fib[0].b)),"Fiber reported in part of "+esc(c.name));
 h+='</div><p style="font-size:14px;color:#58697a">Picks use FCC data (June 30, 2026) and typical new-customer prices (Nov 2026). Your street may differ, so confirm your exact address.</p>';
 const cst=__zstats(d,c.zips),sst=__stateStats(d),SN=ST[d.code];
 if(cst.n&&sst.n){
  const cf=__pct(cst.fib,cst.n),sf=__pct(sst.fib,sst.n),cg=__pct(cst.gig,cst.n),sg=__pct(sst.gig,sst.n),cw=(cst.wired/cst.n).toFixed(1),sw=(sst.wired/sst.n).toFixed(1);
  const cmp=(a,b)=>a>b?"above":a<b?"below":"in line with";
  h+='<h2>How '+esc(c.name)+' compares with the rest of '+esc(SN)+'</h2><table><tr><th>Measure</th><th>'+esc(c.name)+'</th><th>'+esc(SN)+' average</th></tr>'+
   '<tr><td>ZIP codes with fiber reported</td><td><b>'+cf+'%</b></td><td>'+sf+'%</td></tr>'+
   '<tr><td>ZIP codes with 1 Gbps or faster</td><td><b>'+cg+'%</b></td><td>'+sg+'%</td></tr>'+
   '<tr><td>Wired and 5G providers per ZIP code</td><td><b>'+cw+'</b></td><td>'+sw+'</td></tr></table>'+
   '<p>Fiber coverage in '+esc(c.name)+' is '+cmp(cf,sf)+' the '+esc(SN)+' average, and households here have '+(+cw>+sw?"more":+cw<+sw?"fewer":"about as many")+' non-satellite providers to choose from per ZIP code. '+
   (+cw>=3?"More choice usually means more room to negotiate a lower bill.":"With fewer providers, promotions and retention offers matter more, so check your bill when a promotion ends.")+'</p>';
 }
 const bl=[];L.slice(0,12).forEach(x=>{const k=__BILL[String(cn(x.b)).toLowerCase()];if(k&&bl.indexOf(k)<0)bl.push(k)});
 if(bl.length)h+='<h2>Paying too much in '+esc(c.name)+'?</h2><p>If your bill went up after a promotion ended, these guides show what each charge is and how to get a lower rate: '+
   bl.slice(0,6).map(k=>'<a href="/bills/'+k+'">'+esc(cn(L.find(x=>__BILL[String(cn(x.b)).toLowerCase()]===k).b))+' bill guide</a>').join(" · ")+' · <a href="/bills">All bill guides</a></p>';
 const nb=__near(d,cs,c);
 if(nb.length)h+='<h2>Internet providers near '+esc(c.name)+'</h2><ul class="lk">'+nb.map(k=>'<li><a href="/internet/'+d.code+'/'+k+'">'+esc(d.cities[k].name)+'</a></li>').join("")+'</ul>';
 return h;
 }catch(e){return ""}
}
