"""Score target accounts by hiring intent and export a lead list (CSV) for Clay, HubSpot or Salesforce.

Usage:
    export APIFY_TOKEN=...
    python hiring_signal_leads.py stripe.com notion.so ashby:ramp
"""
import csv
import os
import sys

from apify_client import ApifyClient

ACTOR = "cape-data-labs/company-hiring-signals"
TARGET_TOOLS = {"Snowflake", "dbt", "Databricks"}   # tools your product sells alongside / replaces


def score(row: dict) -> int:
    """Toy intent score: recent hiring + relevant tools mentioned in job ads."""
    points = min(row.get("postedLast30Days") or 0, 50)
    mentioned = {tool for group in (row.get("techStackMentioned") or {}).values() for tool in group}
    points += 20 * len(mentioned & TARGET_TOOLS)
    return points


def main(companies: list[str]) -> None:
    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(ACTOR).call(run_input={"companies": companies})
    rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    rows.sort(key=score, reverse=True)

    with open("hiring_signal_leads.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["company", "intent_score", "open_jobs", "posted_last_30_days", "top_signal"])
        for r in rows:
            signals = r.get("signals") or [""]
            w.writerow([r["company"], score(r), r.get("openJobs"), r.get("postedLast30Days"), signals[0]])
    print(f"Saved {len(rows)} accounts to hiring_signal_leads.csv")


if __name__ == "__main__":
    main(sys.argv[1:] or ["stripe.com", "ashby:ramp", "Notion"])
