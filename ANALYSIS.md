# GA4 Ecommerce Analysis

## Objective

Explore customer behavior and ecommerce performance in the public Google
Merchandise Store GA4 export, identify meaningful funnel and channel patterns,
and demonstrate practical BigQuery SQL.

## Dataset

The analysis uses Google's obfuscated GA4 ecommerce sample:
`bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`.

| Metric | Result |
| --- | ---: |
| Date range | 2020-11-01 to 2021-01-31 |
| Events | 4,295,584 |
| Anonymous users | 270,154 |
| Event types | 17 |

The data is obfuscated and can contain placeholders or inconsistencies. Results
cannot be compared directly with the Google Analytics demo account.

## Findings

### Event distribution

`page_view` is the largest event category at 31.44%, followed by
`user_engagement` at 24.65% and `scroll` at 11.48%. Together, page views and
engagement account for 56.09% of recorded events. Only 71 `view_item_list`
events appear, which suggests incomplete or unusual list-view tracking.

### Ecommerce funnel reach

![GA4 ecommerce funnel reach](charts/funnel-reach.png)

| Step | Users | Share of product viewers |
| --- | ---: | ---: |
| View item | 61,252 | 100.00% |
| Add to cart | 12,545 | 20.48% |
| Begin checkout | 9,715 | 15.86% |
| Add shipping information | 9,714 | 15.86% |
| Add payment information | 5,751 | 9.39% |
| Purchase | 4,419 | 7.21% |

The largest reach losses occur before add-to-cart and between shipping and
payment. Checkout and shipping counts are almost identical, which may reflect
the site's implementation. These figures measure users who triggered each
event; they are not a strictly ordered, session-scoped funnel.

### Device conversion

| Device | Product viewers | Cart users | Purchasers | Viewer-to-purchase |
| --- | ---: | ---: | ---: | ---: |
| Desktop | 36,323 | 7,384 | 2,541 | 7.00% |
| Mobile | 24,810 | 5,142 | 1,851 | 7.46% |
| Tablet | 1,443 | 276 | 97 | 6.72% |

Conversion is similar across device types. Mobile has the highest observed
rate, while tablet has the smallest sample. This descriptive difference should
not be treated as conclusive without statistical testing.

### Product performance

The Google Zip Hoodie F/C generated the most item revenue ($13,788), while
Super G Unisex Joggers sold the most units (308). Hoodies, sweatshirts, fleece,
and jackets dominate the top ten, a pattern consistent with the
November-through-January sample period.

### Traffic acquisition

Google organic produced the most recorded revenue ($95,775), followed by
direct traffic ($79,650). Referral traffic from the merchandise store domain
reported a 2.18% user conversion rate. An obfuscated `(data deleted)` segment
reported 3.79%, but its hidden identity makes it unsuitable for a channel
recommendation. Source fields represent first-user acquisition, not necessarily
the source associated with the purchase session.

## Recommendations

1. Investigate the large product-view-to-cart loss with product-page and
   add-to-cart UX analysis.
2. Examine the shipping-to-payment transition for friction or instrumentation
   gaps.
3. Preserve the strong organic search contribution while assessing whether
   paid search can improve its comparatively low observed conversion.
4. Audit `view_item_list` tracking before using product-list analysis.
5. Validate these descriptive findings with current, unobfuscated production
   data before making business decisions.

## Reproduce the analysis

Run the numbered queries in [`sql/`](sql/) in ascending order using BigQuery.
Check the bytes-processed estimate before each run. The MCP server provides
related tools for repeatable conversational analysis with a default 2 GiB
per-query safety cap.
