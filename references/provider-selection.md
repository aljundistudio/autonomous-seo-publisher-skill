# Provider selection

## Selection sequence

Ask for text provider, image provider, credential location, desired languages, expected posts per month, and preference among quality, speed, and cost. Keep the question compact. If the user says “etc.”, offer these common choices without treating them as exhaustive:

| Need | Choices |
|---|---|
| Text | OpenRouter, Gemini API, OpenAI API, Anthropic API, local OpenAI-compatible endpoint, custom REST API |
| Images | OpenRouter Images, Gemini image model, OpenAI Images, existing media library, custom endpoint, none |
| Secrets | Environment variable, protected environment file, secret manager, platform secret |

Do not ask for the secret value. Ask for a reference such as `OPENROUTER_API_KEY`, `GEMINI_API_KEY`, or `/etc/example/seo-agent.env`.

## Model choice

Provider catalogs, prices, context limits, and model identifiers change. Verify current official documentation before choosing a model. Select a concrete model based on:

- Arabic and English writing quality;
- structured JSON reliability;
- context and output limits;
- image-output capability and raster formats;
- latency and monthly budget;
- data residency or compliance needs;
- availability and explicit fallback policy.

Never use a convenient router alias as the production primary unless the user chooses nondeterministic routing. Record the exact text and image model identifiers in configuration and every run report.

## Provider adapter contract

Normalize all providers behind two logical calls:

```text
generate_json(system_prompt, user_prompt, schema, timeout) -> object
generate_image(prompt, aspect_ratio, dimensions, format, timeout) -> raster bytes + media type
```

The adapter must:

- load credentials only from an approved secret reference;
- set explicit timeouts;
- validate HTTP status and response shape;
- reject empty, truncated, or non-JSON text responses;
- reject non-raster or undersized image responses;
- record provider, model, request ID, latency, and cost when returned;
- redact credentials and sensitive response headers;
- retry only transient statuses with bounded exponential backoff;
- never change provider on failure unless the user approved that fallback.

## Recommended user prompt

Use wording similar to:

> Which provider should power article writing, and which should generate covers? You can choose OpenRouter, Gemini API, OpenAI API, Anthropic, a local/custom endpoint, or no generated images. Also tell me the environment-variable or protected-file name where the credentials are stored—do not paste the key itself.
