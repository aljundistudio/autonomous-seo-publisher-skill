# Website adapter and scheduling contract

## Adapter discovery

Inspect the active website before defining commands. Determine:

1. authoritative content file, database, or CMS API;
2. article and media schemas;
3. active release pointer and release directory;
4. build, sitemap, feed, and cache-invalidation commands;
5. protected files that must survive releases;
6. production health URLs and rollback operation.

Do not infer these paths from another website.

## Normalized adapter operations

Implement the following operations with site-native commands or CMS APIs:

```text
inspect()          -> active release, schema, latest posts, protected-file hashes
stage(run_id)      -> isolated release or transaction
write_post(data)   -> authoritative content record
write_cover(bytes) -> versioned raster asset
build()            -> pages, indexes, feeds, sitemaps, schemas
verify_stage()     -> deterministic checks without public switch
activate()         -> atomic pointer switch or CMS publish transaction
verify_live()      -> HTTP and content checks
rollback()         -> restore previous release or revision
```

Every operation must fail non-zero or throw on error. `activate()` must not run if any earlier required operation failed.

## Atomic static/VPS pattern

```text
active = realpath(current)
release = releases/<timestamp>-seo-<slug>
copy active -> release
mutate release
build and verify release
create temporary symlink -> release
atomically rename temporary symlink -> current
verify public URLs
rollback current -> active on failure
```

Retain at least one known-good previous release. Verify resolved paths before recursive cleanup.

## CMS/API pattern

- Create a draft first.
- Upload the raster cover and obtain its stable media ID.
- Attach structured content, metadata, language links, and media.
- Preview or validate the draft.
- Publish with an idempotency key where supported.
- Re-read the published record and public URLs.
- Revert to the prior revision or unpublish on verification failure.

## Server scheduling pattern

Prefer systemd timer plus oneshot service on Linux:

- timer runs at the configured local time;
- service loads a protected environment file;
- service acquires `flock` or an equivalent exclusive lock;
- service checks the authoritative store for today's post;
- failures schedule bounded retries rather than a tight loop;
- success records `last_success_date` in the publishing timezone;
- manual runs call the same service and same duplicate guard.

For cron-only systems, wrap the cycle in the same lock, timeout, idempotency, logging, and failure-closed behavior.

## Verification minimum

- article pages in every language: HTTP 200;
- cover: HTTP 200, raster media type, plausible byte size;
- canonical and hreflang: correct absolute URLs;
- Article and FAQ JSON-LD: parseable;
- sitemap/feed/robots: HTTP 200 and contain intended URLs;
- authoritative content store: exactly one new record;
- verification files: unchanged hashes;
- live pointer: expected release;
- service and timer: healthy and next run visible.
