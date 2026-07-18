# Editorial JSON contract

Request JSON only. Adapt field names to the site's native schema after generation, not inside the model response.

```json
{
  "topic_key": "stable-english-key",
  "search_intent": "commercial or informational intent",
  "category": "strategy",
  "cover_prompt": "visual concept without text or logos",
  "languages": {
    "ar": {
      "title": "",
      "slug": "",
      "seo_title": "",
      "meta_description": "",
      "excerpt": "",
      "keywords": [""],
      "image_alt": "",
      "summary": [""],
      "sections": [
        {"heading": "", "paragraphs": ["", ""], "bullets": [""]}
      ],
      "faqs": [
        {"question": "", "answer": ""}
      ],
      "internal_links": [
        {"anchor": "", "target_hint": ""}
      ]
    },
    "en": {
      "title": "",
      "slug": "",
      "seo_title": "",
      "meta_description": "",
      "excerpt": "",
      "keywords": [""],
      "image_alt": "",
      "summary": [""],
      "sections": [
        {"heading": "", "paragraphs": ["", ""], "bullets": [""]}
      ],
      "faqs": [
        {"question": "", "answer": ""}
      ],
      "internal_links": [
        {"anchor": "", "target_hint": ""}
      ]
    }
  },
  "sources": [
    {"title": "", "url": "", "supports": ""}
  ]
}
```

## Quality gates

Reject or regenerate when:

- a required language or field is absent;
- the slug duplicates an existing route;
- title or intent substantially overlaps a recent post;
- sections are shallow, repetitive, or generic;
- Arabic is a literal or awkward translation of English;
- meta description is empty or misleading;
- keywords are stuffed into prose;
- FAQs repeat section headings without adding value;
- internal link targets do not exist;
- a factual claim lacks support when support is required;
- the model invents clients, results, figures, laws, certifications, awards, or quotes;
- JSON contains markdown fences, commentary, or an unexpected schema.

Use the site's existing word-depth and section conventions where available. Otherwise prefer six developed sections and four useful FAQs; adjust for search intent rather than padding to a word count.
