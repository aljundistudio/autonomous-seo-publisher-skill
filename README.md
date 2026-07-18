# Autonomous SEO Publisher

A provider-neutral Codex skill for safely automating SEO blog creation and publication on existing websites.

It is designed for medium-reasoning agents and supports static sites, VPS releases, custom CMSs, APIs, and databases. The workflow is intentionally failure-closed: it locks concurrent runs, prevents duplicate daily posts, stages atomic releases, validates content and raster covers, verifies SEO output, and rolls back when a live check fails.

## What it does

- Asks the user to select text and image providers: OpenRouter, Gemini, OpenAI, Anthropic, local, or a custom endpoint.
- Keeps credentials out of prompts and source code; it requests only an environment-variable, protected-file, or secret-manager reference.
- Researches non-duplicate, high-intent topics and generates structured multilingual articles.
- Builds SEO metadata, FAQ content, internal-link suggestions, canonical/hreflang metadata, Article and FAQ schema, sitemaps, feeds, and image sitemaps.
- Generates and validates optimized raster covers; SVG/vector placeholders are rejected.
- Publishes through an atomic release or CMS transaction, then confirms live HTTP responses before reporting success.
- Provides systemd/cron-safe scheduling guidance, locks, idempotency, retries, and rollback.

## Install

Copy the `autonomous-seo-publisher` directory into an agent's skills directory, then invoke:

```
Use $autonomous-seo-publisher to configure and run a safe automated SEO publishing workflow for my website.
```

## Configure

1. Inspect the live site and its active publishing path.
2. Ask the site owner for their preferred text provider, image provider, and **credential reference**—never the secret itself.
3. Copy `references/config.example.json` as `seo-publisher.json` in the site project and adapt it to its native content store and release mechanism.
4. Validate it:

```bash
python scripts/validate_config.py /path/to/seo-publisher.json
```

5. Run a guarded sample post, verify staging and production URLs, then configure a server-native timer.

See [SKILL.md](SKILL.md) for the complete operating procedure.

## Security

This project intentionally contains no provider keys, passwords, customer content, or production server access details. Store secrets in restrictive environment files or a secret manager, and configure an explicit fallback policy before enabling a secondary paid provider.

## License

Add a license appropriate to your preferred reuse policy before accepting outside contributions.
