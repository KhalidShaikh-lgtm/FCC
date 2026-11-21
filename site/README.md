# yourbillcheck.com site source

The live site is **not** a static repo. It is:

- Cloudflare Worker `yourbillcheck-site` (module worker, routes `yourbillcheck.com/*`, `www.yourbillcheck.com/*`), KV binding `SITE` holds `index.html` (home template), `plans.json` and worker backups (`worker.vN.js`).
- Cloudflare Pages project `yourbillcheck` serves guides, /privacy, /terms, /s.css (the Worker falls through to it).
- State/city/ZIP pages are rendered by the Worker from `zipdata/out/<st>-zips.json` in this repo.
- Separate Worker `yourbillcheck-leads` handles lead capture (not in this repo, holds secrets).

## v20 SEO/AEO/GEO layer
`site/seo-layer.js` is appended to the end of the v19 Worker, plus 9 string-replace patches (each anchor must match exactly once):

1. `const MOD="2026-11-21";` -> `"2026-11-22"`
2. `const NF=()=>new Response("Not found",{status:404});` -> `const NF=()=>notFound();`
3. before `const crumbHtml=c=>`: `html=decorate(html,o);`
4. before `const ssum=`: `sfaq.push.apply(sfaq,stateExtra(d,nz));`
5. before `const sum=L.length+" providers report internet service across "`: `cityExtra(faq,d,c,PL,S);`
6. before `const sum="In "+zip+`: `siteFaq(false).forEach(function(f){faq.push(f)});`
7. home response uses `homeShell(html)`
8. after `let p=u.pathname.replace(/\/+$/,"");`: `{ const xr=await extraRoutes(p,req); if(xr) return xr; }`
9. final `return fetch(req);` -> `return passthrough(req, env);`

Adds: home/State/City/ZIP/guide/legal meta + Open Graph + JSON-LD (Organization, WebSite, WebPage, Article, BreadcrumbList, ItemList, FAQPage), /about, /methodology, /guides, /internet, /robots.txt (AI crawler allow list), /llms.txt, /llms-full.txt, /sitemap-core.xml, /og.png, real 404s.

Deployed 2026-11-22 as KV `worker.v20.js`. **Rollback:** upload KV `worker.v19.js` as the `yourbillcheck-site` script (keep KV binding `SITE`, compat date 2024-11-01).

## gsc-api (Search Console read access)

`site/gsc-api.js` is a separate private Worker (`gsc-api`, workers.dev) that reads Google Search Console for `sc-domain:yourbillcheck.com` through the Search Console API using the owner's own OAuth login.

- Secrets (Cloudflare, never in git): `GSC_CLIENT_ID`, `GSC_CLIENT_SECRET`, `GSC_REFRESH_TOKEN`, `API_KEY`. Pass the key as `?k=` or header `x-key`.
- Routes: `/api/sites`, `/api/query?days=28&dimension=query|page|country|device|none&limit=25`, `/api/sitemaps`, `/api/sitemaps/submit?url=`, `/api/inspect?url=`.
- Reconnect: delete `GSC_REFRESH_TOKEN`, visit `/auth?k=<API_KEY>`, store the token shown once.
- Rotate the OAuth client secret in Google Cloud (Auth Platform > Clients > client > Additional information), update `GSC_CLIENT_SECRET`, redeploy, then delete the old secret.
