---
name: autonomous-seo-publisher
description: Configure and operate a provider-neutral autonomous SEO agent that researches, writes, illustrates, stages, publishes, schedules, verifies, and reports bilingual or monolingual blog posts for an existing website. Use when an agent must add daily or recurring SEO publishing to any CMS, static site, VPS deployment, or custom website; migrate an existing content agent between OpenRouter, Gemini, OpenAI, Anthropic, local, or custom APIs; publish a sample post; or repair an unreliable SEO automation while preserving production data and rollback paths.
---

# Autonomous SEO Publisher

Build a safe publishing system around the website that already exists. Use medium reasoning by default. Increase deliberation only for production routing, schema migration, or rollback decisions.

## Start with provider selection

Do not assume a provider from an earlier project or a nearby configuration. If the user did not explicitly choose providers for this workflow, ask one compact setup question before making provider-specific changes:

1. Which text provider: OpenRouter, Gemini API, OpenAI API, Anthropic API, local model, or custom endpoint?
2. Which image provider: same provider, OpenRouter Images, Gemini Image, OpenAI Images, existing media library, or no generated covers?
3. Where are credentials already stored: environment variable, protected server file, secret manager, or not configured yet?

Recommend a concrete model only after checking the provider's current official documentation and the user's quality, cost, language, and volume needs. Never ask the user to paste a full API key in chat. Ask them to store it locally or on the server and confirm the variable or protected-file name.

Read [provider-selection.md](references/provider-selection.md) after the provider is selected.

## Establish the publishing contract

Inspect the live route and active deployment before writing:

- Find the authoritative content store, article schema, cover directory, page generator, build command, sitemap generator, robots file, verification files, current release pointer, and rollback mechanism.
- Inspect at least one existing article in each supported language.
- Preserve the existing design, URL conventions, structured data, analytics, verification files, and unrelated content.
- Prefer the website's existing CMS or publisher. Do not create a parallel blog unless the user explicitly requests one.

Read [site-adapters.md](references/site-adapters.md), then create `seo-publisher.json` from [config.example.json](references/config.example.json). Validate it with:

```bash
python scripts/validate_config.py /path/to/seo-publisher.json
```

If Python is unavailable, perform the same checks manually rather than skipping validation.

## Run one publishing cycle

Follow this sequence exactly.

### 1. Acquire a lock and check idempotency

- Use a server-side lock so overlapping cron, manual, or retry runs cannot publish concurrently.
- Resolve today's date in the configured publishing timezone.
- Inspect the authoritative content store. If a valid published post already exists for the same brand and date, verify its pages and cover, report `skipped_existing`, and stop.
- Use a stable idempotency key such as `<site>-<brand>-<local-date>`.

### 2. Choose a non-duplicate topic

- Compare the proposed topic with existing titles, slugs, keywords, search intents, and recent editorial themes.
- Target a real high-intent question appropriate to the site's customers and geography.
- Browse current primary sources when freshness, regulations, product details, or precise claims matter.
- Do not invent statistics, clients, awards, certifications, quotations, laws, or outcomes.

### 3. Generate structured editorial content

Request strict JSON matching [editorial-contract.md](references/editorial-contract.md). Require:

- a useful answer-first introduction;
- independently natural writing in every requested language;
- substantial sections with practical frameworks, trade-offs, pitfalls, and next actions;
- focused keywords, meta titles, descriptions, image alt text, internal-link suggestions, and FAQs;
- citations or source notes when claims need external evidence;
- no keyword stuffing, fake expertise, generic filler, or unsupported superlatives.

Validate the JSON, required fields, minimum depth, unique slug, FAQ count, and prohibited claims before rendering.

### 4. Generate and validate the cover

- Use the image provider selected by the user.
- Generate a raster PNG, JPEG, or WebP in the site's required aspect ratio and dimensions.
- Follow the site's visual identity and the article concept. Do not insert text, logos, people, or watermarks unless requested.
- Reject SVG, HTML, placeholder diagrams, tiny payloads, wrong aspect ratios, corrupt files, and images returned with an unexpected media type.
- Optimize the final raster non-destructively and give it descriptive alt text.
- If cover generation fails, do not publish and do not switch the live release.

### 5. Stage an atomic release

- Copy or clone the active release into a new timestamped release.
- Write the article and cover only inside the new release or CMS transaction.
- Rebuild article pages, archive pages, feeds, sitemaps, image sitemaps, structured data, `robots.txt`, and AI-discovery files used by the site.
- Preserve ownership, permissions, canonical URLs, language alternates, verification files, and existing content.
- Never edit the live `current` tree in place when an atomic release mechanism is available.

### 6. Verify before switching live

Check the staged output:

- content schema parses;
- build exits successfully;
- Arabic/RTL and English/LTR output render correctly when applicable;
- canonical, hreflang, Article schema, FAQ schema, Open Graph, metadata, internal links, and cover references are valid;
- cover is raster, readable, correctly sized, and present;
- no duplicate date, topic, slug, or URL exists;
- sitemap and robots output include the intended routes;
- protected verification files are unchanged.

Switch the live pointer atomically only after every required check passes. Keep the previous release available for rollback.

### 7. Verify production and report

After the switch, require HTTP 200 for every language page, cover, sitemap, and feed affected by the run. Confirm the live content store contains exactly one new record. On any failure, roll back automatically and report the failing check without exposing secrets.

Report:

- outcome: `published`, `skipped_existing`, `rolled_back`, or `failed_closed`;
- article URLs by language;
- cover URL;
- topic and provider/model identifiers;
- scheduled next run and timezone;
- release and rollback identifiers;
- failed checks, if any.

## Install server automation

Prefer a server-native timer such as systemd over a desktop cron for production websites. The scheduled service must:

- load credentials from protected environment or secret files;
- run as the least-privileged appropriate user;
- use an exclusive lock;
- enforce one post per brand per local date;
- retry transient failures with bounded backoff;
- time out provider and build requests;
- write structured status and cost metadata without secrets;
- leave the live release unchanged on failure;
- support a manual `run now` trigger through the same guarded path.

Read the scheduling and adapter patterns in [site-adapters.md](references/site-adapters.md).

## Safety rules

- Treat live publishing as an external write: require explicit authorization unless the user's request already includes deployment or publication.
- Back up before modifying a live agent, content store, service, timer, or reverse-proxy configuration.
- Keep concrete provider and model identifiers; avoid ambiguous automatic routers unless the user selects them.
- Store secrets with restrictive permissions and redact them from logs, diffs, commands, reports, and generated files.
- Do not weaken TLS, authentication, ownership, CSP, or file permissions to make publishing work.
- Do not claim a post is live until production URLs and assets are verified.
- Do not silently fall back to another paid provider or model. Ask once and record an approved fallback policy.
- Stop and preserve the previous release when a required image, content, build, schema, or HTTP check fails.
