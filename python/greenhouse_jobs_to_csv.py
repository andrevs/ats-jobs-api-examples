"""Get every open job from Greenhouse / Lever / Ashby (and 5 more) career pages and save a CSV.

Usage:
    export APIFY_TOKEN=...
    python greenhouse_jobs_to_csv.py https://boards.greenhouse.io/airbnb lever:palantir Stripe
"""
import csv
import os
import sys

from apify_client import ApifyClient

ACTOR = "cape-data-labs/company-career-jobs-api"
FIELDS = ["company", "ats", "title", "department", "location", "workplaceType",
          "seniority", "employmentType", "salary_min", "salary_max", "salary_currency",
          "postedAt", "url", "applyUrl"]


def main(companies: list[str], out_path: str = "jobs.csv") -> None:
    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(ACTOR).call(run_input={
        "companies": companies,
        "includeDescription": False,  # smaller output; set True for full text + HTML
    })

    rows = 0
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for job in client.dataset(run["defaultDatasetId"]).iterate_items():
            salary = job.get("salary") or {}
            job["salary_min"] = salary.get("min")
            job["salary_max"] = salary.get("max")
            job["salary_currency"] = salary.get("currency")
            writer.writerow(job)
            rows += 1
    print(f"Saved {rows} jobs to {out_path}")


if __name__ == "__main__":
    main(sys.argv[1:] or ["https://boards.greenhouse.io/airbnb", "lever:palantir", "ashby:ramp"])
