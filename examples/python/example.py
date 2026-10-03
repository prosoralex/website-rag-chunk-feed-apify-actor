"""
Run the "Website Content Crawler – RAG Chunks for Vector DBs" Apify Actor and print its results.

Setup:
    pip install -r requirements.txt
    export APIFY_TOKEN=your_apify_token   # Apify Console > Settings > API & Integrations

This repository only documents the Actor; its source code runs on Apify's infrastructure.
"""
import os
import sys

from apify_client import ApifyClient

ACTOR_ID = "leadsbrary/website-rag-chunk-feed"

RUN_INPUT = {
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


def main() -> None:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable first (Apify Console > Settings > API & Integrations).")
    client = ApifyClient(token)
    print(f"Starting {ACTOR_ID} ...")
    run = client.actor(ACTOR_ID).call(run_input=RUN_INPUT)
    print(f"Run finished with status: {run['status']}")
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        print(item)


if __name__ == "__main__":
    main()
