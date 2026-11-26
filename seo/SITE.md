# SEO site profile: yourbillcheck.com

Read this first on every SEO run. The team playbook (roles, quality bar, run modes) is the `seo-team` skill;
if that skill is not available, follow `seo/PLAYBOOK.md` in this repo, which is the same text.

## Business
- What it is: independent US internet comparison + bill-check site. Revenue = inbound calls to our call center,
  which sells internet plans (commission). Primary CTA: call (888) 491-5666. Secondary: ZIP search.
- Audience: US households choosing or switching internet, or upset about a bill.
- Author on every page: Khalid Shaikh, Head of Business Development (company founder: Vivek Budhiraja, About page only) (author.py handles the box and schema). Never invent other authors,
  reviews, testimonials or ratings.
- Tone: plain, short sentences, no hype, no "best ever". Say "reported" when a fact comes from a third party
  rather than the provider. Every page lists sources and a "checked" date.
- Never claim to be the provider or affiliated with it. Never quote a price as guaranteed.

## Where traffic is (update weekly from the GSC snapshot)
- Nov 24, 2026: impressions almost all on city/state/ZIP pages. Query clusters, biggest first:
  1. "internet providers in [city/state]"  2. "fiber internet in [city]"  3. "near me / at my address"
  4. brand + place ("xtream by mediacom", "xfinity delaware", "windstream jasper ga")  5. "cheap internet [place]".
- Current focus (set by Khalid, Nov 25): SMALL TOWNS FIRST (~80% of effort), big cities ~20%. Low competition ranks
  fastest (same pattern that made dbi-infomatics.com rank in weeks). The call center can sell anywhere, rural included,
  so every town is sellable. Each WRITE run of 10: 8 priority-1 small-town items + 2 priority-2 items (bigger cities). Pick towns already getting GSC impressions; add new ones from the snapshot weekly. Bill/fee pages (Wave 1) went live Nov 24; judge them from mid-December.

## How to publish on this site
- Repo: KhalidShaikh-lgtm/FCC. Pages build from Python in `site/`. Live site = Cloudflare Worker reading
  `site/pages/*.html` from GitHub `main`, so a merged PR is live within ~10 minutes.
- New pages: add ONE JSON file under `site/content/<type>/` (schema at the top of `site/build_content.py`).
  Allowed paths: `/fiber/<st>/<city>`, `/internet/<st>/<city>` (overrides the auto city page), `/guides/<slug>`,
  `/fees/<slug>`, `/save/<slug>`, `/bills/<slug>`. Lowercase, hyphens, no trailing slash.
- Then: `cd site && python3 build_pages.py` (must print the page count with no error), commit on a new branch,
  open a PR with `gh api repos/KhalidShaikh-lgtm/FCC/pulls`, squash-merge with
  `gh api -X PUT repos/KhalidShaikh-lgtm/FCC/pulls/<n>/merge -f merge_method=squash`.
  If a merge conflicts on generated files, rebuild from a fresh branch off origin/main.
- Data you can use: our own city pages (FCC BDC June 30, 2026 by ZIP) e.g. https://yourbillcheck.com/internet/az/phoenix
  (read with WebFetch), provider sites, broadband labels, reputable reviewers (BroadbandNow, HighSpeedInternet,
  CNET, CableTV.com, Cord Cutters News). Do not use spammy price-scraper sites.
- Search Console data (no browser needed): Cloudflare KV namespace 946f6287fdfb4ed9b78f2377a4ab0324, key
  `gsc:yourbillcheck.com:latest` (JSON: query_page_28, page_28, query_7, daily_28), refreshed daily 00:30 UTC by the
  `gsc-api` worker. Read it via the Cloudflare tool:
  GET /accounts/{accountId}/storage/kv/namespaces/946f6287fdfb4ed9b78f2377a4ab0324/values/gsc:yourbillcheck.com:latest
- Worker changes (new URL prefixes, redirects): see `site/README.md`; current worker = KV `worker.v45.js`.
  Only touch the worker if a page type needs a new prefix; roll back by re-uploading the previous version.

- When a page goes live, write `published YYYY-MM-DD` in its queue.csv notes (pruning stages use this date).

- Queue items whose notes say `not before YYYY-MM-DD` must be skipped (left as todo) until that date.
- Freshness: the sitemap uses each page's real dateModified (site/pages/lastmod.json, built from the page's `date`).
  Only change a page's `date`/`checked` when its facts were actually re-verified or content materially changed.
- Year in titles: in the first REFRESH run of each year (and from mid-December for next-year pages), update year
  references in titles/H1s of evergreen guides to the current year, only where the content is re-verified.

## Hard limits
- Max 10 new pages per writing run (daily), max 70 per week (set by Khalid, Nov 25). Skip any page that would be thin.
- No emails, posts, directory submissions or account changes without Khalid's approval. Off-page work produces
  drafts and lists only.
- Never delete pages. Weak pages are handled by the staged 30/60/90-day rules in PLAYBOOK.md (PRUNE) (improve, merge with 301, or noindex), never by deletion. Never change the phone number, author, or legal/footer text.
