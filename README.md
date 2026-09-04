# GA4 BigQuery (AI-powered) Analytics Server

An **AI-powered analytics server** that helps assistants analyze GA4 ecommerce data in BigQuery through **safe, predefined tools**.

Under the hood, this is implemented as an **MCP server** so compatible AI assistants can call vetted analytics tools (instead of running arbitrary queries).

This repository also includes a reproducible [GA4 ecommerce case study](ANALYSIS.md) and its six numbered [SQL queries](sql/).

![GA4 ecommerce funnel reach](charts/funnel-reach.png)

## Portfolio highlights (from the case study)

Using the public GA4 obfuscated ecommerce sample (2020-11-01 → 2021-01-31):

- Funnel reach (user event reach): **View item → Purchase: 7.21%** (4,419 / 61,252)
- Biggest reach loss: **View item → Add to cart** (20.48% of viewers reached cart)
- Top acquisition sources by revenue (first-user source): **Google organic ($95,775)** and **Direct ($79,650)**

> Note: This is **obfuscated sample data** and may contain placeholder/inconsistent values. Use the analysis patterns and approach, not the raw numbers, for business decisions.

## What to review first (recruiters / interviewers)

1. Read the narrative: [ANALYSIS.md](ANALYSIS.md)
2. Run the numbered queries: [sql/](sql/) (01 → 06)
3. View visuals used in the write-up: [charts/](charts/)

## Features

- Ecommerce overview: events, users, purchases, and revenue
- Daily performance trends
- Top products by revenue
- Traffic acquisition by source and medium
- Checkout funnel counts
- Parameterized queries and strict date validation

The default dataset is `bigquery-public-data.ga4_obfuscated_sample_ecommerce`, covering 2020-11-01
through 2021-01-31. It is obfuscated sample data and may contain placeholder or
internally inconsistent values.

## Prerequisites

- Python 3.11+
- A Google Cloud project with the BigQuery API enabled
- Application Default Credentials

```powershell
gcloud auth application-default login
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
