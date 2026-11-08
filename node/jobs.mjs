// Get every open job from Greenhouse / Lever / Ashby (and 5 more) career pages in Node.js.
// Usage: npm i apify-client && APIFY_TOKEN=... node jobs.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('cape-data-labs/company-career-jobs-api').call({
    companies: ['Stripe', 'https://jobs.lever.co/palantir', 'ashby:ramp'],
    workplaceTypes: ['remote', 'hybrid'],
    includeDescription: false,
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const job of items) {
    console.log(`${job.company} | ${job.title} | ${job.location ?? 'n/a'} | ${job.url}`);
}
console.log(`${items.length} jobs`);
