// Run the "Website Content Crawler – RAG Chunks for Vector DBs" Apify Actor and print its results.
// Setup: npm install  &&  export APIFY_TOKEN=your_apify_token  &&  node example.mjs
// This repository only documents the Actor; its source code runs on Apify's infrastructure.
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set the APIFY_TOKEN environment variable first (Apify Console > Settings > API & Integrations).');
    process.exit(1);
}

const client = new ApifyClient({ token });

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
console.log(`Run finished with status: ${run.status}`);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(JSON.stringify(items, null, 2));
