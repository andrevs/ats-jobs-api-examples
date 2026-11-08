"""Find remote roles that publish a salary range, across many companies at once.

Usage:
    export APIFY_TOKEN=...
    python remote_jobs_with_salary.py
"""
import os

from apify_client import ApifyClient

ACTOR = "cape-data-labs/company-career-jobs-api"
COMPANIES = ["Stripe", "ashby:ramp", "greenhouse:airbnb", "lever:palantir", "Notion"]


def main() -> None:
    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(ACTOR).call(run_input={
        "companies": COMPANIES,
        "workplaceTypes": ["remote"],
        "postedWithinDays": 30,
        "includeDescription": False,
    })
    jobs = [j for j in client.dataset(run["defaultDatasetId"]).iterate_items() if j.get("salary")]
    jobs.sort(key=lambda j: j["salary"].get("max") or 0, reverse=True)
    for j in jobs[:25]:
        s = j["salary"]
        print(f"{s.get('currency')} {s.get('min')}-{s.get('max')}/{s.get('period')}  {j['company']}: {j['title']}  {j['url']}")
    print(f"\n{len(jobs)} remote jobs with a published salary.")


if __name__ == "__main__":
    main()
