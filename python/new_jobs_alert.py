"""Daily new-jobs monitor: returns (and charges for) only jobs you haven't seen before.

Run it from cron / GitHub Actions once a day, or schedule the Actor inside Apify.

Usage:
    export APIFY_TOKEN=...
    export SLACK_WEBHOOK_URL=...   # optional; prints to stdout if unset
    python new_jobs_alert.py
"""
import os

import requests
from apify_client import ApifyClient

ACTOR = "cape-data-labs/company-career-jobs-api"
WATCHLIST = ["Stripe", "ashby:ramp", "https://jobs.lever.co/palantir", "greenhouse:airbnb"]
KEYWORDS = ["data", "engineer"]          # only titles containing any of these
MEMORY = "my-watchlist"                  # separate "already seen" list per monitor


def main() -> None:
    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(ACTOR).call(run_input={
        "companies": WATCHLIST,
        "titleKeywords": KEYWORDS,
        "onlyNewJobs": True,
        "stateStoreName": MEMORY,
        "includeDescription": False,
    })
    jobs = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    if not jobs:
        print("No new jobs today.")
        return

    lines = [f"• {j['company']}: <{j['url']}|{j['title']}> ({j.get('location') or 'n/a'})" for j in jobs]
    text = f"{len(jobs)} new job(s):\n" + "\n".join(lines)
    webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if webhook:
        requests.post(webhook, json={"text": text}, timeout=10).raise_for_status()
    print(text)


if __name__ == "__main__":
    main()
