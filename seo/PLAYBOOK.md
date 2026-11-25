# SEO Team Playbook

A complete SEO team as roles one agent plays in sequence, with a separate checker for anything that goes live.
Works for any site: everything site-specific lives in that site's `seo/` folder (SITE.md, queue.csv, log.md).

## 0. Start of every run
1. Find the site's repo and read `seo/SITE.md`, the top of `seo/log.md`, and `seo/queue.csv`.
2. Load Search Console data the way SITE.md says (snapshot in Cloudflare KV, or GSC directly).
3. Do only the run mode you were asked for. Respect SITE.md hard limits (pages per run, approval rules).
4. End every run by adding one dated line to the top of `seo/log.md` and updating `queue.csv` statuses,
   committed in the same PR as the work.

## 1. The team

| Role | Job | Output |
|---|---|---|
| Director | Picks what to work on from data, enforces limits, decides when to stop | Run plan (3-5 lines in log) |
| Analyst | Reads GSC: rising queries, pages at position 5-20, high impressions with low CTR, pages losing clicks, new query clusters | Queue changes with reasons |
| Researcher | For one target query: top 5 Google results (what they cover, gaps, format), facts with primary sources, local data | Research notes inside the PR description |
| Writer | Turns research into the page in the site's format | Page file |
| Editor | Plain English, a 40-60 word short answer at the top (AEO), title <= 60 chars with the query near the front, meta 140-160 chars, H2s that match sub-questions, 3-6 internal links in and out, FAQ from real "People also ask" questions | Edited page |
| Fact-checker | A SEPARATE subagent that has not seen the drafting. Checks every number, date, price and claim against the listed sources; marks third-party claims "reported"; removes anything unsupported | Pass/fail list; fixes applied |
| Technical SEO | Build passes, page returns 200 live, one H1, canonical, schema (Article, FAQ, Breadcrumb), in sitemap, no broken internal links, mobile layout OK | Verification line in log |
| Off-page | Link-worthy assets (data studies, trackers, tools), PR angles, citation/directory list, unlinked-mention and broken-link finds, outreach drafts | Drafts and lists ONLY, in `seo/offpage/`; nothing sent without the owner's approval |
| Reporter | Weekly summary for the owner | 10 lines max |

## 2. Run modes

### ONBOARD (new product or site)
Input from the owner: product/idea, website URL, how it makes money, the one action we want visitors to take,
target country, who the author is.
1. Create `seo/SITE.md` from the template in section 5, `seo/queue.csv`, `seo/log.md`.
2. Research: 5-10 seed topics, competitors (top 3 that rank for the money query), keyword clusters grouped by
   intent (buy now / compare / problem / learn). Prefer clusters where the site can be genuinely useful (own data,
   tools, local detail).
3. Site plan: pillar pages + supporting pages per cluster, internal-link map, 30 queue items prioritised by
   (intent x feasibility x volume).
4. Technical baseline: sitemap, robots, canonical, schema, page speed, Search Console property and sitemap
   submitted (needs the owner to add the property once if it is a new domain).
5. Schedule the recurring runs (section 3) for the site.
6. Report the plan to the owner in 10 lines.

### PLAN (weekly)
Analyst + Director. From GSC (last 7 vs previous, 28 days):
- Position 5-20 with impressions: add "improve" items (expand, answer missing sub-questions, add internal links).
- Impressions > 100 and CTR < 1%: rewrite title/meta.
- New queries with no matching page: new page items.
- Two pages ranking for the same query: merge or differentiate.
- Pages that lost > 30% clicks: refresh item.
Re-rank the queue; at most 15 items marked priority 1.

### WRITE (2-3 times a week)
Take the top 1-3 `todo` items (never more than SITE.md allows). For each: Researcher -> Writer -> Editor ->
Fact-checker subagent -> fix -> build -> Technical SEO check after merge. If the fact-checker fails something
that cannot be sourced, cut it. Mark the item `published` with the date. If an item is not worth doing (no
real data, duplicate), mark it `skipped` with a reason.

### IMPROVE (weekly, after PLAN)
Apply up to 3 "improve" or "ctr" items to existing pages. Same check chain. Never change the URL.

### REFRESH (monthly)
Re-verify prices, dates and "checked" lines on the 10 most-visited pages and any page with time-sensitive facts
(price trackers). Update `checked` dates only when facts were actually re-verified.

### PRUNE (staged 30 / 60 / 90 days after a page went live)
Page age comes from queue.csv (`published YYYY-MM-DD` in notes) or the log. "Impressions" = GSC snapshot, last 28 days.
- Day 30 (checked weekly in PLAN): page has 0 impressions -> probably not indexed. Add 2-3 internal links from
  stronger related pages, add more real local data, make sure it is in the sitemap. No removal.
- Day 60 (checked weekly in PLAN): page has impressions but < 10 and 0 clicks -> improve it (answer missing
  sub-questions, better title/meta) or, if another page covers the same intent, merge into it with a 301.
- Day 90 (monthly in REFRESH): still 0 clicks and < 10 impressions in the last 90 days after the day-30/60 fixes ->
  add noindex and drop it from the sitemap. Reversible; the URL keeps working for visitors.
Never delete files. Actions touching more than 50 pages, or a whole templated group (e.g. all ZIP pages), are
proposals for the owner's approval. Log every action with URL, stage and reason in seo/pruned.csv.

### OFFPAGE (every two weeks)
Find 10 link opportunities (resource pages, local news, directories, journalists asking for sources, unlinked
mentions). Write outreach drafts. Save to `seo/offpage/YYYY-MM-DD.md`. Tell the owner they are ready. Never send.

### REPORT (weekly)
Clicks, impressions, average position (week vs previous week), top 5 rising queries, pages published, pages
improved, what needs the owner (approvals, access, data). No filler.

## 3. Default schedule per site (owner's time zone; avoid :00 and :30)
- Mon: PLAN + IMPROVE + REPORT
- Tue, Thu, Sat: WRITE
- 1st of month: REFRESH
- Every other Wed: OFFPAGE

## 4. Quality bar (Google helpful-content rules)
- Each page must add something the top results lack: own data, local detail, a tool, a clearer answer.
- No thin or templated filler; no keyword stuffing; no AI-sounding fluff ("in today's digital age").
- Real author, real sources, real dates. No fake reviews, ratings, quotes or credentials.
- Prefer fewer, better pages. Mass-produced pages risk the whole site.

## 5. SITE.md template
Business (what, revenue, primary CTA) / Audience / Author / Tone and claims rules / Where traffic is /
Current focus / How to publish (repo, build, deploy, page format) / Data sources allowed / Search Console
access / Hard limits (pages per run, approvals).
