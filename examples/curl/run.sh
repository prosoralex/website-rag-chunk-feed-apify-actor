#!/usr/bin/env bash
# Run the "Website Content Crawler – RAG Chunks for Vector DBs" Apify Actor synchronously and print the dataset items.
# Usage: export APIFY_TOKEN=your_apify_token && ./run.sh
set -euo pipefail
: "${APIFY_TOKEN:?Set APIFY_TOKEN first (Apify Console > Settings > API & Integrations)}"

curl -sS -X POST "https://api.apify.com/v2/acts/leadsbrary~website-rag-chunk-feed/run-sync-get-dataset-items" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
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
