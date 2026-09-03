-- Compare first-user acquisition sources by users, purchasers, and revenue.
SELECT
  COALESCE(traffic_source.source, '(direct)') AS source,
  COALESCE(traffic_source.medium, '(none)') AS medium,
  COUNT(DISTINCT user_pseudo_id) AS users,
  COUNT(DISTINCT IF(event_name = 'purchase', user_pseudo_id, NULL))
    AS purchasers,
  ROUND(
    100 * COUNT(DISTINCT IF(event_name = 'purchase', user_pseudo_id, NULL))
    / COUNT(DISTINCT user_pseudo_id),
    2
  ) AS user_conversion_percent,
  ROUND(
    SUM(IF(event_name = 'purchase', ecommerce.purchase_revenue_in_usd, 0)),
    2
  ) AS revenue_usd
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
GROUP BY source, medium
ORDER BY revenue_usd DESC
LIMIT 10;

