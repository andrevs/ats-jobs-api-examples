# Greenhouse, Lever & Ashby Jobs API — Python & Node.js examples

Copy-paste scripts for pulling **every open job from company career pages** on Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Recruitee, Personio and Breezy HR — and for turning those jobs into **hiring-intent leads**.

The scripts call two hosted APIs on Apify (no scraping infrastructure, no proxies, no logins):

| What you want | API | Price |
|---|---|---|
| Every individual job, one clean format (title, location, remote, seniority, salary, apply URL) | [Greenhouse, Lever, Ashby & Workable Jobs Scraper API](https://apify.com/cape-data-labs/company-career-jobs-api) | $1.50 per 1,000 jobs |
| One row per company: hiring velocity, teams growing, tech stack from job ads, buying signals | [Hiring Signals & Tech Stack Leads](https://apify.com/cape-data-labs/company-hiring-signals) | $10 per 1,000 companies |

Apify's free plan includes monthly credit, which is enough to try every example here.

> Disclosure: I built both APIs. Issues and feature requests are welcome — open one here or on the Apify page.

## Setup

```bash
git clone https://github.com/andrevs/ats-jobs-api-examples
cd ats-jobs-api-examples
pip install -r requirements.txt
export APIFY_TOKEN=...   # from https://console.apify.com/settings/integrations
```

## Examples

| Script | What it does |
|---|---|
| [`python/greenhouse_jobs_to_csv.py`](python/greenhouse_jobs_to_csv.py) | Get all jobs from one or more Greenhouse / Lever / Ashby boards and save a CSV |
| [`python/new_jobs_alert.py`](python/new_jobs_alert.py) | Daily "new jobs only" monitor for a watchlist of companies — prints or posts to a Slack webhook |
| [`python/remote_jobs_with_salary.py`](python/remote_jobs_with_salary.py) | Find remote roles with a published salary range across many companies |
| [`python/hiring_signal_leads.py`](python/hiring_signal_leads.py) | Score a list of target accounts by hiring intent and export a lead list for Clay / HubSpot / Salesforce |
| [`node/jobs.mjs`](node/jobs.mjs) | The same jobs pull in Node.js |

## Input formats

Each company can be given as:

- a name — `Stripe`
- a careers-page URL — `https://boards.greenhouse.io/airbnb`, `https://jobs.lever.co/palantir`, `https://jobs.ashbyhq.com/ramp`
- a `platform:board` pair — `greenhouse:airbnb`, `lever:palantir`, `ashby:ramp`, `workable:<account>`, `personio:<company>`

URLs and `platform:board` pairs are fastest because they skip platform detection.

## FAQ

**Is there an official Greenhouse / Lever / Ashby jobs API?** Each platform publishes a public job-board feed per company. The APIs used here read those feeds for you, auto-detect which platform a company uses, and normalise all eight platforms into one schema.

**Can I get jobs as CSV or Excel?** Yes — see `greenhouse_jobs_to_csv.py`, or export any run from the Apify console.

**Does it collect personal data?** No. Only job postings that companies publish on their own careers pages.

## License

MIT — use the examples however you like.
