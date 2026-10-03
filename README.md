# Website Content Crawler – RAG Chunks for Vector DBs — Apify Actor usage guide

[![Run on Apify](https://img.shields.io/badge/Apify-Run%20this%20Actor-24C1E0)](https://apify.com/leadsbrary/website-rag-chunk-feed?fpr=aupara)
[![Try Apify free](https://img.shields.io/badge/Apify-Try%20it%20free-24C1E0)](https://console.apify.com/sign-up?fpr=aupara)

Website content crawler for RAG: turn any site into token-counted, heading-aware chunks with chunk ID, overlap, heading path, offsets, content hash and source URL. Export JSON, CSV or Excel. From $0.80 per 1,000 chunks.

> **This repository does not contain the Actor's source code.** The Actor is closed-source and
> runs on Apify's infrastructure. This repo is documentation plus ready-to-run client examples
> (curl, Python, JavaScript) that call the hosted Actor with **your own** Apify API token.

**Run it on Apify →** [https://apify.com/leadsbrary/website-rag-chunk-feed?fpr=aupara](https://apify.com/leadsbrary/website-rag-chunk-feed?fpr=aupara)

## What it does

- No JavaScript rendering — plain HTTP + HTML parsing only. Pages that render content client-side yield a `skipped` row (`skipReason: "empty_content"`); use a browser-based crawler for those sites.
- No login, paywall or access-control bypass, and no CAPTCHA solving.
- No embeddings are generated and no third-party LLM/embedding API is called — only chunking and tokenization.
- `robots.txt` is honoured by default (`respectRobotsTxt: true`).

## Use cases

- Crawl a documentation site and get chunks that can be embedded and upserted into a vector DB directly, using chunkId as the upsert key.
- Re-crawl the same site on a schedule and use contentHash + chunkId to re-embed only the chunks whose text actually changed.
- Feed an MCP server or an agent retrieval tool with pre-chunked, source-attributed website content (every chunk keeps its URL and heading path for citations).
- Build an evaluation or fine-tuning corpus from a public knowledge base with token counts already measured per chunk.


## Input

| Field | Type | Required | Description |
|---|---|---|---|
| `startUrls` | array | yes | Pages or sections to crawl. Each URL is a crawl seed; links found on the page are followed up to maxCrawlDepth. |
| `maxCrawlDepth` | integer | no | How many link hops to follow from each start URL. 0 = only the start URLs themselves. |
| `maxCrawlPages` | integer | no | Hard cap on pages fetched, including pages that produce no chunk. Protects spending. |
| `maxResults` | integer | no | Hard cap on chunk rows pushed to the dataset. The run stops cleanly when reached. |
| `sameDomainOnly` | boolean | no | Follow links only on the same hostname as the start URL(s). |
| `includeUrlGlobs` | array | no | Glob patterns a URL must match to be crawled, e.g. https://docs.example.com/guide/**. Empty = no restriction. |
| `excludeUrlGlobs` | array | no | Glob patterns that exclude a URL from crawling (changelogs, archives, locale duplicates). |
| `respectRobotsTxt` | boolean | no | Honour the target site's robots.txt disallow rules. Leave on unless you own the site. |
| `chunkStrategy` | string | no | heading-recursive: split on markdown headings first, then recursively on paragraphs/words to fit chunkSize. recursive: ignore headings. page: one chunk per page (no splitting). |
| `chunkSize` | integer | no | Target chunk size in tokens of the selected tokenizer. |
| `chunkOverlap` | integer | no | Tokens of the previous chunk repeated at the start of the next one. Must be smaller than chunkSize. |
| `minChunkChars` | integer | no | Chunks shorter than this (navigation leftovers, empty sections) are dropped instead of polluting the index. |
| `tokenizer` | string | no | Tokenizer used for chunkSize, chunkOverlap and tokenCount. |
| `outputFormat` | string | no | Format of the chunk text: cleaned markdown or plain text. |
| `includePageMetadata` | boolean | no | Include per-page metadata (description, author, publishedAt, modifiedAt) on every chunk row. |
| `proxyConfiguration` | object | no | Only needed if the site you crawl rate-limits datacenter traffic. |

The full input form (with defaults and validation) is on the [Actor page](https://apify.com/leadsbrary/website-rag-chunk-feed?fpr=aupara).


## Output (sample item)

Sample trimmed for readability (long texts and lists are shortened) — a real run returns the complete data.

```json
{
  "chunkId": "doc_9d6548fc_0000",
  "url": "https://docs.python.org/3/tutorial/introduction.html",
  "canonicalUrl": "https://docs.python.org/3/tutorial/introduction.html",
  "pageTitle": "3. An Informal Introduction to Python",
  "headingPath": [],
  "chunkIndex": 0,
  "totalChunksForPage": 13,
  "text": "In the following examples, input and output are distinguished by the presence or absence of prompts ([\\>>>](https://docs.python.org/3/glossary.html#term-0) and […](https://docs.python.org/3/glossary.html#term-...)): to repeat the example, you must type everything after the prompt…",
  "tokenCount": 399,
  "charCount": 1816,
  "overlapTokensWithPrevious": 0,
  "startCharOffset": 0,
  "endCharOffset": 1967,
  "contentHash": "b9176f2f827b1101",
  "language": "en",
  "pageMetadata": {
    "description": "In the following examples, input and output are distinguished by the presence or absence of prompts (>>> and …): to repeat the example, you must type everything after the prompt, when the ...",
    "author": null,
    "publishedAt": null,
    "modifiedAt": null
  },
  "depth": 0,
  "httpStatus": 200,
  "crawledAt": "2026-10-03T11:20:32.880Z",
  "chunkStrategy": "heading-recursive",
  "tokenizer": "cl100k_base",
  "status": "ok",
  "skipReason": null
}
```

## Pricing

Pay only for results: about **$1.20 per 1,000 results** on the Apify Free plan, down to **$0.80 per 1,000** on paid Apify plans.

Apify platform usage (compute) is billed by Apify on top of the per-result price — about **$0.06 per 1,000 results** in our measured test runs (estimate, varies with input). Tip: keep only the output formats and options you need to reduce it.

Prices can change — the [Actor page](https://apify.com/leadsbrary/website-rag-chunk-feed?fpr=aupara) always shows the current pricing.

## Quick start

You need an Apify account and an API token (Apify Console → **Settings → API & Integrations**).
Never commit your token: export it as the `APIFY_TOKEN` environment variable.

### cURL

```bash
curl -X POST "https://api.apify.com/v2/acts/leadsbrary~website-rag-chunk-feed/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @- <<'JSON'
{
  "startUrls": [
    {
      "url": "https://docs.python.org/3/tutorial/introduction.html"
    }
  ],
  "maxCrawlDepth": 0,
  "maxCrawlPages": 3,
  "maxResults": 3,
  "sameDomainOnly": true,
  "includeUrlGlobs": [],
  "excludeUrlGlobs": [],
  "respectRobotsTxt": true,
  "chunkStrategy": "heading-recursive",
  "chunkSize": 512,
  "chunkOverlap": 64,
  "minChunkChars": 120,
  "tokenizer": "cl100k_base",
  "outputFormat": "markdown",
  "includePageMetadata": true,
  "proxyConfiguration": {
    "useApifyProxy": false
  }
}
JSON
```

### Python (`apify-client`)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run_input = {
    "startUrls": [
        {
            "url": "https://docs.python.org/3/tutorial/introduction.html"
        }
    ],
    "maxCrawlDepth": 0,
    "maxCrawlPages": 3,
    "maxResults": 3,
    "sameDomainOnly": True,
    "includeUrlGlobs": [],
    "excludeUrlGlobs": [],
    "respectRobotsTxt": True,
    "chunkStrategy": "heading-recursive",
    "chunkSize": 512,
    "chunkOverlap": 64,
    "minChunkChars": 120,
    "tokenizer": "cl100k_base",
    "outputFormat": "markdown",
    "includePageMetadata": True,
    "proxyConfiguration": {
        "useApifyProxy": False
    }
}

run = client.actor("leadsbrary/website-rag-chunk-feed").call(run_input=run_input)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### JavaScript (`apify-client`)

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const runInput = {
  "startUrls": [
    {
      "url": "https://docs.python.org/3/tutorial/introduction.html"
    }
  ],
  "maxCrawlDepth": 0,
  "maxCrawlPages": 3,
  "maxResults": 3,
  "sameDomainOnly": true,
  "includeUrlGlobs": [],
  "excludeUrlGlobs": [],
  "respectRobotsTxt": true,
  "chunkStrategy": "heading-recursive",
  "chunkSize": 512,
  "chunkOverlap": 64,
  "minChunkChars": 120,
  "tokenizer": "cl100k_base",
  "outputFormat": "markdown",
  "includePageMetadata": true,
  "proxyConfiguration": {
    "useApifyProxy": false
  }
};

const run = await client.actor('leadsbrary/website-rag-chunk-feed').call(runInput);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

Runnable versions live in [`examples/`](./examples).

## Troubleshooting

- **401 / "User was not found or authentication token is not valid"** — check that `APIFY_TOKEN` is set and copied completely.
- **The run finished but the dataset is empty** — widen your search input or check the run log on the Apify Console.
- **Run stops early** — you may have reached the maximum cost per run you set in Apify; raise it in the run options.
- **Need something else?** Open an issue in this repository or use the Issues tab on the Actor page.

## Don't have an Apify account yet?

[Sign up here](https://console.apify.com/sign-up?fpr=aupara) — new accounts get $5 of free platform usage every month, enough to try most Actors without paying upfront.
Browse the full [Apify Store](https://apify.com/store?fpr=aupara) or [all Actors from this developer](https://apify.com/leadsbrary?fpr=aupara).

## Links

- Actor page: [https://apify.com/leadsbrary/website-rag-chunk-feed?fpr=aupara](https://apify.com/leadsbrary/website-rag-chunk-feed?fpr=aupara)
- All Actors from this developer: [https://apify.com/leadsbrary?fpr=aupara](https://apify.com/leadsbrary?fpr=aupara)
- Apify API reference: [https://docs.apify.com/api/v2](https://docs.apify.com/api/v2)

## Keywords

website content crawler rag chunks, embedding ready website scraper, rag chunk feed, website to vector db, mcp ready website crawler, docs crawler for rag, markdown chunker crawler, token aware chunking scraper, website knowledge base crawler, pinecone qdrant website ingestion, llm ready web scraper

#RAG #VectorDB #LLM #Embeddings #WebCrawler #Chunking #AI #LangChain #MCP #Apify #DeveloperTools #Markdown

## License

The example code in this repository is released under the MIT License — see [LICENSE](./LICENSE).
It does not cover the Actor itself, which remains closed-source and is operated by its developer on Apify.
