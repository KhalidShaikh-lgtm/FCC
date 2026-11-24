# SEO site profile: yourbillcheck.com

Read this first on every SEO run. The team playbook (roles, quality bar, run modes) is the `seo-team` skill;
if that skill is not available, follow `seo/PLAYBOOK.md` in this repo, which is the same text.

## Business
- What it is: independent US internet comparison + bill-check site. Revenue = inbound calls to our call center,
  which sells internet plans (commission). Primary CTA: call (888) 491-5666. Secondary: ZIP search.
- Audience: US households choosing or switching internet, or upset about a bill.
- Author on every page: Khalid Shaikh, Director (author.py handles the box and schema). Never invent other authors,
  reviews, testimonials or ratings.
- Tone: plain, short sentences, no hype, no "best ever". Say "reported" when a fact comes from a third party
  rather than the provider. Every page lists sources and a "checked" date.
- Never claim to be the provider or affiliated with it. Never quote a price as guaranteed.

## Where traffic is (update weekly from the GSC snapshot)
- Nov 24, 2026: impressions almost all on city/state/ZIP pages. Query clusters, biggest first:
  1. "internet providers in [city/state]"  2. "fiber internet in [city]"  3. "near me / at my address"
  4. brand + place ("xtream by mediacom", "xfinity delaware", "windstream jasper ga")  5. "cheap internet [place]".
- Current focus (set by Khalid, Nov 24): LOCAL. Fiber-by-city pages and richer city pages for places that already
  get impressions. Bill/fee pages (Wave 1) went live Nov 24; judge them from mid-December.

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

## Hard limits
- Max 3 new pages per writing run, max 10 per week. Quality over count.
- No emails, posts, directory submissions or account changes without Khalid's approval. Off-page work produces
  drafts and lists only.
- Never delete pages. Never change the phone number, author, or legal/footer text.
