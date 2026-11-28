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
- CURRENT FOCUS (set by Khalid, Nov 27 2026, replaces the Nov 25 small-towns focus): BILLING-FIRST. The site is a free
  watchdog for household bills: people overpaying, hit by price increases, promo endings and added fees. Search Console
  Nov 21-26: 26 billing pages = 8 of 13 clicks, CTR 0.83%, avg position 8.9; 963 city/ZIP pages = 5 clicks, CTR 0.03%,
  position 37. Big comparison brands own "internet providers near me"; nobody owns "my bill went up, what do I do".
  - Effort split: ~90% billing (bill went up, price increases, fees, lower/negotiate your bill, retention scripts,
    price tracker, alerts, data studies on pricing), ~10% keeping existing pages healthy.
  - NO new town/city/fiber pages. Queue items of those types are 'parked'. Existing city/ZIP pages stay up (never
    delete) and should point visitors to the billing pages.
  - WRITE run mix: up to 5 items while the safety brake is active (see Limits), all from priority-1/2 billing items in queue.csv; 'ctr'/'improve' items on pages
    that already rank (positions 5-15) come FIRST, before new pages.
  - Every billing page: a direct answer to the exact search (including dollar amounts people search, e.g. "went up $15"),
    reported causes labelled "reported", a "what to say when you call" retention script, a link to the price tracker
    and alert signup, and an honest "you may not need to switch" option. Judge pages by calls + leads (ev:<date>), not clicks alone.
  - PHASE 1 (set by Khalid, Nov 27 2026): INTERNET BILLS ONLY. Every internet provider: bill went up, price increase, lower your bill, retention, cancel, fees, real cost vs promo, switching/moving fees, discounts. ~85% of effort on these pages, ~15% on bill tools/data (reader reports, price tracker, alerts, studies). TV and mobile pages are 'parked' until Khalid confirms those providers are sellable (Phase 2 TV ~Jan, Phase 3 mobile as partners are added). Do NOT write outage, generic plan, speed-test or 'providers near me' pages.
  - Full plan and goals: seo/ROADMAP.md.

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
  `gsc:yourbillcheck.com:latest` (JSON: query_page_28, page_28, query_7, daily_28, device_28, country_28; fresh data, ends yesterday, matches the Search Console report since 2026-11-27. Snapshots dated 2026-11-26 and earlier used final data only and undercount the last 2-3 days), refreshed daily 00:30 UTC by the
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

## Index cleanup (2026-11-28, approved by Khalid)
- All /internet/<ZIP> pages are noindex,follow and out of the sitemaps. City pages are noindex too EXCEPT the KEEPC list in the worker (top ~100 cities by GSC impressions + the 5 hand-written metro pages). State pages stay indexed. Pages still work for visitors.
- Reason: ZIP pages had 10,155 impressions and 0 clicks in 28 days; city pages 15,867 / 5; the template pages most likely pulled the whole site down (bill pages fell from ~pos 7 to outside top 50 on Nov 27-28; no manual action).
- Do NOT create new ZIP or city pages, and do not add cities to KEEPC without hand-written unique content and Khalid's OK. New pages = billing pages only.
- Priority for IMPROVE runs until rankings return: the ANTI-TEMPLATE queue items (unique titles/descriptions/intros per provider; /bills/<p> = 'why so high', /bills/<p>-bill-went-up = 'why it went up').

## Hard limits
- SAFETY BRAKE ACTIVE since 2026-11-28 (Khalid chose 'slow to 10/day'): max 10 new pages per day = each of the two WRITE runs (2:37 PM and 11:17 PM IST) publishes UP TO 5 new pages, max 70 per week. Reason: site-wide ranking drop on Nov 27-28 (bill pages fell from ~pos 7-8 to outside top 50 in US Google; still indexed; no manual action). Do not raise this limit without Khalid. (Was 20/day, raised Nov 27.) Skip any page that would be thin; never publish a page the Opus fact-checker fails.
- SAFETY BRAKE: if the weekly run sees billing-page average position worsen by 5+ places week on week, or fewer than half of last week's new pages indexed, go back to one WRITE run (10/day) and tell Khalid.
- Plus up to 20 IMPROVED existing pages per day in the evening IMPROVE run (raised by Khalid, Nov 27). Each page at most once per 7 days, so the real number depends on how many billing pages exist. Improvements never change a URL and do not count toward the new-page limit.
- No emails, posts, directory submissions or account changes without Khalid's approval. Off-page work produces
  drafts and lists only.
- Never delete pages. Weak pages are handled by the staged 30/60/90-day rules in PLAYBOOK.md (PRUNE) (improve, merge with 301, or noindex), never by deletion. Never change the phone number, author, or legal/footer text.

## Conversions (since 2026-11-27)
Cloudflare KV key `ev:<YYYY-MM-DD>` (UTC day) holds daily totals from the site: `{"t":{event:count},"p":{path:{event:count}},"s":{source:{event:count}}}`.
Events: `call` (tap on a phone number), `lead` (bill-check or other form sent to the CRM), `reminder` (promo-end reminder signup), `zip` (ZIP check on a city/ZIP page), `report` (outage report).
Sources: google, bing, other-search, ai, social, direct, internal, other. No personal data is stored.
Use it: rank pages and topics by calls + leads, not only clicks. Write more of what produces calls; fix pages with traffic but no calls (CTA, intent match). Counts start at zero; judge after 2 weeks.
